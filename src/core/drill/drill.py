import dataclasses


@dataclasses.dataclass(frozen=True)
class DrillInterface:
    """
    Represents a drill arguments and return value types.
    """

    arguments: list[type]
    return_value: type


@dataclasses.dataclass(frozen=True)
class DrillDependencies:
    """
    Represents a drills system and python dependencies.
    """

    system: list[str]
    python: list[str]


@dataclasses.dataclass(frozen=True)
class Drill:
    """
    Represents a drill.
    """

    id: str
    name: str
    author: str
    repository: str
    dependencies: DrillDependencies
    interface: DrillInterface
