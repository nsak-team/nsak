import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class ScenarioInterface:
    """
    Represents a scenarios arguments and return value types.
    """

    arguments: tuple[str]
    return_type: str


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class ScenarioDependencies:
    """
    Represents the scenarios drill, system and python dependencies.
    """

    system: set[str]
    python: set[str]


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Scenario:
    """
    Represents a scenario.
    """

    id: str
    name: str
    description: str | None
    path: Path
    author: str
    repository: str
    drills: set[str]
    dependencies: ScenarioDependencies
    interface: ScenarioInterface
