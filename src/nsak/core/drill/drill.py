import dataclasses


@dataclasses.dataclass(frozen=True)
class DrillInterface:
    arguments: list[type]
    return_value: type


@dataclasses.dataclass(frozen=True)
class DrillDependencies:
    system: list[str]
    python: list[str]


@dataclasses.dataclass(frozen=True)
class Drill:
    id: str
    name: str
    author: str
    repository: str
    dependencies: DrillDependencies
    interface: DrillInterface
