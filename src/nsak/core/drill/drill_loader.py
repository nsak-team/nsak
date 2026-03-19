from pathlib import Path
from typing import Any

from nsak.core.drill.drill import Drill, DrillDependencies, DrillInterface
from nsak.core.resource import ResourceLoader


class DrillLoader(ResourceLoader[Drill]):
    """
    Finds and loads drills from the library paths.
    """

    ResourceClass = Drill

    @classmethod
    def _to_resource(cls, data: dict[str, Any], path: Path) -> Drill:
        """
        Creates a Drill object from a dict containing the drill's metadata.
        """
        return Drill(
            id=str(data["metadata"]["id"]),
            name=str(data["metadata"]["name"]),
            description=str(
                data["metadata"]["description"]
                if "description" in data["metadata"]
                else None
            ),
            path=path,
            author=str(data["metadata"]["author"]),
            repository=str(data["metadata"]["repository"]),
            dependencies=DrillDependencies(
                system=set(data["dependencies"]["system"]),
                python=set(data["dependencies"]["python"]),
            ),
            interface=DrillInterface(
                arguments=tuple(data["interface"]["arguments"]),
                return_type=str(data["interface"]["return_type"]),
            ),
        )
