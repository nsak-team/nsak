from __future__ import annotations

import dataclasses
from pathlib import Path


class ResourceError(Exception):
    """
    Common base class for all resource related errors.
    """

    ResourceType: type["Resource"]


class InvalidResourceError(ResourceError):
    """
    Exception raised when a resource is invalid.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        self.original_exception = original_exception
        super().__init__(original_exception or message)


class ResourceNotFoundError(ResourceError):
    """
    Exception raised when a resource is not found.
    """

    def __init__(self, name: str, search_paths: set[Path] | None = None) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.search_paths = search_paths
        resource_type_name = self.ResourceType.__name__
        if search_paths is None:
            message = f"{resource_type_name} '{name}' not found."
        else:
            message = f"{resource_type_name} '{name}' not found in any of the following paths: {search_paths}"
        super().__init__(message)


class MultipleResourcesFoundError(ResourceError):
    """
    Exception raised when multiple resources with the same folder name are found.
    """

    def __init__(self, name: str, results: set[Path], search_paths: set[Path]) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.results = results
        self.search_paths = search_paths
        resource_type_name = self.ResourceType.__name__
        message = f"Multiple {resource_type_name}s with '{name}' found: {', '.join({str(result) for result in results})}"
        super().__init__(message)


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Resource:
    """
    Abstract base class for all resources.
    """

    NAME = "resource"
    KEY = "resources"
    ResourceError = ResourceError
    InvalidResourceError = InvalidResourceError
    ResourceNotFoundError = ResourceNotFoundError
    MultipleResourcesFoundError = MultipleResourcesFoundError
