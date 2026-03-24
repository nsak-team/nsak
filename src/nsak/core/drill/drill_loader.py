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
    def _to_resource(cls, id: str, data: dict[str, Any], path: Path | str) -> Drill:
        """
        Creates a Drill object from a dict containing the drill's metadata.
        """
        if isinstance(path, str):
            path = Path(path)

        interface = data.get("interface") or {}
        arguments = interface.get("arguments") or {}
        dependencies = data.get("dependencies") or {}
        system = set(dependencies.get("system") or [])
        python = set(dependencies.get("python") or [])

        return Drill(
            id=id,
            name=str(data.get("name") or ""),
            description=str(data.get("description") or ""),
            path=path,
            author=str(data.get("author") or ""),
            repository=str(data.get("repository") or ""),
            dependencies=DrillDependencies(
                system=system,
                python=python,
            ),
            interface=DrillInterface(
                arguments={
                    name: DrillArgument(
                        type=argument.get("type"),
                        default=argument.get("default") or None,
                    )
                    for name, argument in arguments.items()
                },
                return_type=str(interface.get("return_type") or ""),
            ),
        )
