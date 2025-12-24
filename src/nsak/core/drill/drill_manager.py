import importlib.util
import sys
from typing import Any, List

from nsak.core.drill import Drill, DrillLoader
from nsak.core.drill.drill_loader import DrillNotFoundError


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
        if spec is None:
            raise DrillNotFoundError(drill.name)
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise DrillNotFoundError(drill.name)
        sys.modules[module_name] = module
        if spec.loader is None:
            raise DrillNotFoundError(drill.name)
        spec.loader.exec_module(module)
        return module.run(*args, **kwargs)
