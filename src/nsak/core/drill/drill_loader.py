from pathlib import Path
from typing import Any

from nsak.core.drill.drill import (
    Drill,
    DrillArgument,
    DrillDependencies,
    DrillInterface,
)
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
        arguments = data["interface"].get("arguments", {}) or {}

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
                arguments={
                    name: DrillArgument(
                        type=argument["type"],
                        default=argument.get("default", None),
                    )
                    for name, argument in arguments.items()
                },
                return_type=data["interface"]["return_type"],
            ),
        )
