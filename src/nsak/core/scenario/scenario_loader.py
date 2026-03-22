from pathlib import Path
from typing import Any

from nsak.core.resource import ResourceLoader
from nsak.core.scenario.scenario import (
    Scenario,
    ScenarioArgument,
    ScenarioDependencies,
    ScenarioInterface,
)


class ScenarioLoader(ResourceLoader[Scenario]):
    """
    Finds and loads scenarios from the library paths.
    """

    ResourceClass = Scenario

    @classmethod
    def _to_resource(cls, id: str, data: dict[str, Any], path: Path | str) -> Scenario:
        """
        Creates a Scenario object from a dict containing the scenario's metadata.
        """
        if isinstance(path, str):
            path = Path(path)

        interface = data.get("interface") or {}
        arguments = interface.get("arguments") or {}
        dependencies = data.get("dependencies") or {}
        system = set(dependencies.get("system") or [])
        python = set(dependencies.get("python") or [])

        return Scenario(
            id=id,
            name=str(data.get("name") or ""),
            description=str(data.get("description") or ""),
            path=path,
            author=str(data.get("author") or ""),
            repository=str(data.get("repository") or ""),
            drills=set(data.get("drills") or []),
            scenarios=set(),  # Not implemented yet
            environments=set(data.get("environments") or []),
            dependencies=ScenarioDependencies(
                system=system,
                python=python,
            ),
            interface=ScenarioInterface(
                arguments={
                    name: ScenarioArgument(
                        type=argument.get("type"),
                        default=argument.get("default", None),
                    )
                    for name, argument in arguments.items()
                },
                return_type=str(interface.get("return_type") or ""),
            ),
        )
