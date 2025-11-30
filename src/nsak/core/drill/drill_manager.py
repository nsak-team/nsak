from typing import List

from nsak.core.drill import Drill, DrillLoader


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
