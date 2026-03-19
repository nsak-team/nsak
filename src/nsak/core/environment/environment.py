import dataclasses
from pathlib import Path

from nsak.core.resource import (
    InvalidResourceError,
    MultipleResourcesFoundError,
    Resource,
    ResourceError,
    ResourceNotFoundError,
)


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Environment(Resource):
    """
    Represents an environment.
    """

    id: str
    name: str
    path: Path
    author: str
    repository: str


class EnvironmentError(ResourceError):
    """
    Base class for environment errors.
    """

    ResourceType = Environment


class InvalidEnvironmentError(InvalidResourceError, EnvironmentError):
    """
    Exception raised when an environment is invalid.
    """


class EnvironmentNotFoundError(ResourceNotFoundError, EnvironmentError):
    """
    Exception raised when an environment is not found.
    """


class MultipleEnvironmentsFoundError(MultipleResourcesFoundError, EnvironmentError):
    """
    Exception raised when multiple environments with the same folder name are found.
    """


# Avoids circularity issues
Environment.ResourceError = EnvironmentError
Environment.InvalidResourceError = InvalidEnvironmentError
Environment.ResourceNotFoundError = EnvironmentNotFoundError
Environment.MultipleResourcesFoundError = MultipleEnvironmentsFoundError
