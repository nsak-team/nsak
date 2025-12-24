import importlib.util
import inspect
import sys
from typing import Any, List

from nsak.core.drill import Drill, DrillLoader
from nsak.core.drill.drill_loader import DrillNotFoundError, InvalidDrillError


class DrillManager:
    """
    A collection of methods to manage drills.
    """

    @classmethod
    def list(cls) -> List[Drill]:
        """
        Lists all drills.
        """
        return DrillLoader.load_all()

    @classmethod
    def get(cls, name: str) -> Drill:
        """
        Get a drill by name.
        """
        return DrillLoader.load(name)

    @classmethod
    def execute(cls, drill: Drill, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """
        Load the drills entrypoint and execute it.
        """
        module_name = drill.path.name
        spec = importlib.util.spec_from_file_location(
            module_name, drill.path / "drill.py"
        )
        if spec is None or spec.loader is None:
            raise DrillNotFoundError(drill.name)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        run_fn = getattr(module, "run", None)
        if run_fn is None or not callable(run_fn):
            msg = f"Drill '{drill.name}' has no callable run()"
            raise InvalidDrillError(msg)

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
            raise DrillNotFoundError(drill.name)
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise DrillNotFoundError(drill.name)
        sys.modules[module_name] = module
        if spec.loader is None:
            raise DrillNotFoundError(drill.name)
        spec.loader.exec_module(module)

        cleanup_fn = getattr(module, "cleanup", None)
        if not callable(cleanup_fn):
            raise InvalidDrillError(drill.name)

        cleanup_fn()
