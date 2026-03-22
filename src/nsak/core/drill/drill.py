import dataclasses
from pathlib import Path
from typing import Any

from nsak.core.resource import (
    InvalidResourceError,
    MultipleResourcesFoundError,
    Resource,
    ResourceError,
    ResourceNotFoundError,
)


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class DrillArgument:
    """
    Represents a specific drill argument.
    """

    type: str
    default: Any


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class DrillInterface:
    """
    Represents drill arguments and return value types.
    """

    arguments: dict[str, DrillArgument]
    return_type: str


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class DrillDependencies:
    """
    Represents a drills system and python dependencies.
    """

    system: set[str]
    python: set[str]


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Drill(Resource):
    """
    Represents a drill.
    """

    NAME = "drill"
    KEY = "drills"

    id: str
    name: str
    description: str
    path: Path
    author: str
    repository: str
    dependencies: DrillDependencies
    interface: DrillInterface


class DrillError(ResourceError):
    """
    Base class for drill errors.
    """

    ResourceType = Drill


class InvalidDrillError(InvalidResourceError, DrillError):
    """
    Exception raised when a drill is invalid.
    """


class DrillNotFoundError(ResourceNotFoundError, DrillError):
    """
    Exception raised when a drill is not found.
    """


class MultipleDrillsFoundError(MultipleResourcesFoundError, DrillError):
    """
    Exception raised when multiple drills with the same folder name are found.
    """


# Avoids circularity issues
Drill.ResourceError = DrillError
Drill.InvalidResourceError = InvalidDrillError
Drill.ResourceNotFoundError = DrillNotFoundError
Drill.MultipleResourcesFoundError = MultipleDrillsFoundError
