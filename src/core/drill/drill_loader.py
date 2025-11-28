from pathlib import Path
from typing import Any

import yaml

from src.core.config import LIBRARY_PATHS
from src.core.drill.drill import Drill


class InvalidDrillError(Exception):
    """
    Exception raised when a drill is invalid.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        self.original_exception = original_exception
        super().__init__(message)


class DrillNotFoundError(Exception):
    """
    Exception raised when a drill is not found.
    """

    def __init__(self, name: str, search_paths: set[Path]) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.search_paths = search_paths
        message = (
            f"Drill '{name}' not found in any of the following paths: {search_paths}"
        )
        super().__init__(message)


class MultipleDrillsFoundError(Exception):
    """
    Exception raised when multiple drills with the same folder name are found.
    """

    def __init__(self, name: str, results: set[Path], search_paths: set[Path]) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.results = results
        self.search_paths = search_paths
        message = f"Multiple Drills with '{name}' found: {', '.join({str(result) for result in results})}"
        super().__init__(message)


class DrillLoader:
    """
    Finds and loads drills from the library paths.
    """

    def __init__(self) -> None:
        """
        Setup drill loader.
        """
        self._search_paths = {path / "drills" for path in LIBRARY_PATHS}

    def _search(self, name: str) -> set[Path]:
        """
        Search for drills.
        """
        results: set[Path] = set()
        for path in self._search_paths:
            candidate = path / name
            if candidate.exists():
                results.add(candidate)

        return results

    def _find(self, name: str) -> Path:
        """
        Find a drill by its folder name.
        """
        results = self._search(name)
        match len(results):
            case 0:
                raise DrillNotFoundError(name, self._search_paths)
            case 1:
                return results.pop()
            case _:
                raise MultipleDrillsFoundError(name, results, self._search_paths)

    @staticmethod
    def _load(path: Path) -> dict[str, Any]:
        """
        Load drill from a YAML file into a dict.
        """
        drill_yaml = path / "drill.yaml"
        if not drill_yaml.exists():
            message = "Drill must contain a drill.yaml file."
            raise InvalidDrillError(message)
        with open(drill_yaml, "r") as file:
            data = yaml.safe_load(file)
        if not isinstance(data, dict):
            message = "Loading a drill.yaml file must return a dictionary."
            raise InvalidDrillError(message)
        return data

    @staticmethod
    def _create(data: dict[str, Any]) -> Drill:
        """
        Creates a Drill object from a dict containing the drill's metadata.
        """
        try:
            return Drill(**data)
        except TypeError as e:
            message = "Loaded Drill data is invalid."
            raise InvalidDrillError(message, e) from e

    def load(self, name: str) -> Drill:
        """
        Load a drill by its folder name and return a Drill object.
        """
        result = self._find(name)
        data = self._load(result)
        return self._create(data)
