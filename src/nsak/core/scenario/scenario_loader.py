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
    def _to_resource(cls, data: dict[str, Any], path: Path) -> Scenario:
        """
        Creates a Scenario object from a dict containing the scenario's metadata.
        """
        arguments = data["interface"].get("arguments", {}) or {}

        return Scenario(
            id=str(data["metadata"]["id"]),
            name=str(data["metadata"]["name"]),
            description=str(data["metadata"]["description"])
            if "description" in data["metadata"]
            else None,
            path=path,
            author=str(data["metadata"]["author"]),
            repository=str(data["metadata"]["repository"]),
            drills=set(data["drills"]),
            scenarios=set(),  # Not implemented yet
            environments=set(data.get("environments") or []),
            dependencies=ScenarioDependencies(
                system=set(data["dependencies"]["system"]),
                python=set(data["dependencies"]["python"]),
            ),
            interface=ScenarioInterface(
                arguments={
                    name: ScenarioArgument(
                        type=argument["type"],
                        default=argument.get("default", None),
                    )
                    for name, argument in arguments.items()
                },
                return_type=str(data["interface"]["return_type"]),
            ),
        )
