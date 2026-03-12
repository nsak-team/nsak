import importlib.util
import inspect
import logging
import sys
from typing import Any

from nsak.core.resource import ResourceManager

from .drill import Drill
from .drill_loader import DrillLoader

logger = logging.getLogger(__name__)


class DrillManager(ResourceManager[Drill]):
    """
    A collection of methods to manage drills.
    """

    ResourceLoaderClass = DrillLoader

    @classmethod
    def execute(cls, drill: Drill | str, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """
        Load the drills entrypoint and execute it.
        """
        if isinstance(drill, str):
            drill = cls.get(drill)

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

        sig = inspect.signature(run_fn)

        # if a drill has **kwargs pass everything
        # TODO design this part to pass arguments to a drill
        if any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        ):
            return run_fn(*args, **kwargs)

        # pass only expected keyword parameters
        allowed = set(sig.parameters.keys())
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed}

        return run_fn(*args, **filtered_kwargs)

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
