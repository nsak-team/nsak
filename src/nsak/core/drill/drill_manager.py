import importlib.util
import logging
import sys
from typing import Any

from nsak.core.resource import ResourceManager

from .drill import Drill
from .drill_loader import DrillLoader

logger = logging.getLogger(__name__)


class ArgumentParsingError(ValueError):
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
                raise ArgumentParsingError(message)
            value = kwargs.get(name) or argument.default
            if type(value).__name__ not in argument.type:
                message = f"Invalid type {type(value)} for argument {name}, expected {argument.type}."
                raise ArgumentParsingError(message)
            arguments[name] = value
        return arguments

    @classmethod
    def execute(cls, drill: Drill | str, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """
        Load the drills entrypoint and execute it.
        """
        if isinstance(drill, str):
            drill = cls.get(drill)

        arguments = cls._parse_arguments(drill, **kwargs)

        module_name = drill.path.name
        spec = importlib.util.spec_from_file_location(
            module_name, drill.path / "drill.py"
        )
        if spec is None or spec.loader is None:
            raise Drill.ResourceNotFoundError(drill.name)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        run_fn = getattr(module, "run", None)
        if run_fn is None or not callable(run_fn):
            msg = f"Drill '{drill.name}' has no callable run()"
            raise Drill.InvalidResourceError(msg)

        logger.warning("EXEC DRILL: %s", drill.name)

        return run_fn(**arguments)

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
