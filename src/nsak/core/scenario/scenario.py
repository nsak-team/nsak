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
class ScenarioArgument:
    """
    Represents a specific scenario argument.
    """

    type: str
    default: Any


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class ScenarioInterface:
    """
    Represents a scenarios arguments and return value types.
    """

    arguments: dict[str, ScenarioArgument]
    return_type: str


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class ScenarioDependencies:
    """
    Represents the scenarios drill, system and python dependencies.
    """

    system: set[str]
    python: set[str]


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Scenario(Resource):
    """
    Represents a scenario.
    """

    NAME = "scenario"
    KEY = "scenarios"

    id: str
    name: str
    description: str | None
    path: Path
    author: str
    repository: str
    drills: set[str]
    scenarios: set[str]
    environments: set[str]
    dependencies: ScenarioDependencies
    interface: ScenarioInterface


class ScenarioError(ResourceError):
    """
    Base class for scenario errors.
    """

    ResourceType = Scenario


class InvalidScenarioError(InvalidResourceError, ScenarioError):
    """
    Exception raised when a scenario is invalid.
    """


class ScenarioNotFoundError(ResourceNotFoundError, ScenarioError):
    """
    Exception raised when a scenario is not found.
    """


class MultipleScenariosFoundError(MultipleResourcesFoundError, ScenarioError):
    """
    Exception raised when multiple scenarios with the same folder name are found.
    """


# Avoids circularity issues
Scenario.ResourceError = ScenarioError
Scenario.InvalidResourceError = InvalidScenarioError
Scenario.ResourceNotFoundError = ScenarioNotFoundError
Scenario.MultipleResourcesFoundError = MultipleScenariosFoundError
