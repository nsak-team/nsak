import functools
import logging
from pathlib import Path
from typing import Any

import yaml

from nsak.core.config import LIBRARY_PATHS
from nsak.core.environment.environment import Environment

logger = logging.getLogger(__name__)


class InvalidEnvironmentError(Exception):
    """
    Exception raised when a environment is invalid.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        self.original_exception = original_exception
        super().__init__(original_exception or message)


class EnvironmentNotFoundError(Exception):
    """
    Exception raised when an environment is not found.
    """

    def __init__(self, name: str, search_paths: set[Path] | None = None) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.search_paths = search_paths
        if search_paths is None:
            message = f"Environment '{name}' not found."
        else:
            message = f"Environment '{name}' not found in any of the following paths: {search_paths}"
        super().__init__(message)


class MultipleEnvironmentsFoundError(Exception):
    """
    Exception raised when multiple environments with the same folder name are found.
    """

    def __init__(self, name: str, results: set[Path], search_paths: set[Path]) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.results = results
        self.search_paths = search_paths
        message = f"Multiple Environments with '{name}' found: {', '.join({str(result) for result in results})}"
        super().__init__(message)


class EnvironmentLoader:
    """
    Finds and loads environments from the library paths.
    """

    @staticmethod
    @functools.cache
    def get_search_paths() -> set[Path]:
        """
        Returns the paths to search for environments.
        """
        return {path / "environments" for path in LIBRARY_PATHS}

    @classmethod
    def _search(cls, name: str) -> set[Path]:
        """
        Search for environments.
        """
        results: set[Path] = set()
        for path in cls.get_search_paths():
            candidate = path / name
            if candidate.exists():
                results.add(candidate)

        return results

    @classmethod
    def _find(cls, name: str) -> Path:
        """
        Find an environment by its folder name.
        """
        results = cls._search(name)
        match len(results):
            case 0:
                raise EnvironmentNotFoundError(name, cls.get_search_paths())
            case 1:
                return results.pop()
            case _:
                raise MultipleEnvironmentsFoundError(
                    name, results, cls.get_search_paths()
                )

    @staticmethod
    def _load(path: Path) -> dict[str, Any]:
        """
        Load environment from a YAML file into a dict.
        """
        environment_yaml = path / "environment.yaml"
        if not environment_yaml.exists():
            message = "Environment must contain a environment.yaml file."
            raise InvalidEnvironmentError(message)
        with open(environment_yaml, "r") as file:
            data = yaml.safe_load(file)
        if not isinstance(data, dict):
            message = "Loading a environment.yaml file must return a dictionary."
            raise InvalidEnvironmentError(message)
        return data

    @staticmethod
    def _create(data: dict[str, Any], path: Path) -> Environment:
        """
        Creates an Environment object from a dict containing the environment's metadata.
        """
        try:
            return Environment(
                id=str(data["metadata"]["id"]),
                name=str(data["metadata"]["name"]),
                path=path,
                author=str(data["metadata"]["author"]),
                repository=str(data["metadata"]["repository"]),
            )
        except TypeError as e:
            message = "Loaded Environment data is invalid."
            raise InvalidEnvironmentError(message, e) from e

    @classmethod
    def load(cls, name: str) -> Environment:
        """
        Load an environment by its folder name and return a Environment object.
        """
        path = cls._find(name)
        data = cls._load(path)
        return cls._create(data, path)

    @classmethod
    def load_all(cls) -> list[Environment]:
        """
        Load all environments and return a set of Environment objects.
        """
        all_environments: list[Environment] = list()
        for search_path in cls.get_search_paths():
            for path in search_path.iterdir():
                if not path.is_dir():
                    continue
                try:
                    data = cls._load(path)
                    environment = cls._create(data, path)
                    all_environments.append(environment)
                except InvalidEnvironmentError as e:
                    message = f"Skipping invalid environment '{path.name}'"
                    logger.debug(message, exc_info=e)

        return all_environments
