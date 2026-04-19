import asyncio
import importlib.util
import inspect
import logging
import sys
from typing import Any, Callable

from mypy_extensions import KwArg

from nsak.core.resource import ResourceManager

from .drill import Drill
from .drill_loader import DrillLoader

logger = logging.getLogger(__name__)


class DrillArgumentParsingError(ValueError):
    """
    Exception thrown when argument parsing fails.
    """

    pass


class DrillManager(ResourceManager[Drill]):
    """
    A collection of methods to manage drills.
    """

    ResourceLoaderClass = DrillLoader

    @classmethod
    def _parse_arguments(cls, drill: Drill, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """
        Parse arguments for drill execution.

        :param kwargs:
        :return:
        """
        arguments = {}
        for name, argument in drill.interface.arguments.items():
            if argument.default is None and (
                name not in kwargs or kwargs[name] is None
            ):
                message = f"Required argument {name} is missing."
                raise DrillArgumentParsingError(message)
            value = kwargs.get(name) or argument.default
            if type(value).__name__ not in argument.type:
                message = f"Invalid type {type(value)} for argument {name}, expected {argument.type}."
                raise DrillArgumentParsingError(message)
            arguments[name] = value
        return arguments

    @classmethod
    def get_drill_entrypoint(cls, drill: Drill) -> Callable[[KwArg(Any)], Any]:
        """
        Get the drill entrypoint and return it as a synchronous callable.
        """
        module_name = drill.path.name
        spec = importlib.util.spec_from_file_location(
            module_name, drill.path / "drill.py"
        )
        if spec is None or spec.loader is None:
            raise Drill.ResourceNotFoundError(drill.name)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        entrypoint = getattr(module, "run", None)

        if entrypoint is None:
            message = f"Drill '{drill.name}' has no callable run()"
            raise Drill.InvalidResourceError(message)

        def normalized_entrypoint(**kwargs: Any) -> Any:  # noqa: ANN401
            """
            Normalizes sync and async entrypoints.

            This docstring get's overwritten by the docstring of the original usage as langchain tool.
            """
            info = "EXEC %s SCENARIO: %s"
            logger.info(info)
            if inspect.iscoroutinefunction(entrypoint):
                logger.debug(message, "ASYNC", drill.name)
                return asyncio.run(entrypoint(**kwargs))
            elif inspect.isfunction(entrypoint):
                logger.debug(message, "SYNC", drill.name)
                return entrypoint(**kwargs)

            error = f"Scenario '{drill.name}.run' is not a function or coroutine."
            raise Drill.InvalidResourceError(error)

        normalized_entrypoint.__doc__ = entrypoint.__doc__
        return normalized_entrypoint

    @classmethod
    def execute(cls, drill: Drill | str, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """
        Load the drills entrypoint and execute it.
        """
        if isinstance(drill, str):
            drill = cls.get(drill)

        arguments = cls._parse_arguments(drill, **kwargs)
        entrypoint = cls.get_drill_entrypoint(drill)
        return entrypoint(**arguments)

    @classmethod
    def clean_up(cls, drill: Drill) -> None:
        """
        Clear the drills.

        :param drill:
        :return: None
        """
        module_name = drill.path.name
        spec = importlib.util.spec_from_file_location(
            module_name, drill.path / "drill.py"
        )

        if spec is None:
            raise Drill.ResourceNotFoundError(drill.name)
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise Drill.ResourceNotFoundError(drill.name)
        sys.modules[module_name] = module
        if spec.loader is None:
            raise Drill.ResourceNotFoundError(drill.name)
        spec.loader.exec_module(module)

        cleanup_fn = getattr(module, "cleanup", None)
        if not callable(cleanup_fn):
            raise Drill.InvalidResourceError(drill.name)

        cleanup_fn()
