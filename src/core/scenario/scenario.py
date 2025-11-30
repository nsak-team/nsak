import dataclasses


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

    drills: set[str]
    system: set[str]
    python: set[str]


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Scenario:
    """
    Represents a scenario.
    """

    id: str
    name: str
    author: str
    repository: str
    dependencies: ScenarioDependencies
    interface: ScenarioInterface
