import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class DrillInterface:
    """
    Represents a drill arguments and return value types.
    """

    arguments: tuple[str]
    return_type: str


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class DrillDependencies:
    """
    Represents a drills system and python dependencies.
    """

    system: set[str]
    python: set[str]


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
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
