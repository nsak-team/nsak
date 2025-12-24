import functools
import logging
from pathlib import Path
from typing import Any

import yaml

from nsak.core.config import LIBRARY_PATHS
from nsak.core.drill.drill import Drill, DrillDependencies, DrillInterface

logger = logging.getLogger(__name__)


class InvalidDrillError(Exception):
    """
    Exception raised when a drill is invalid.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        self.original_exception = original_exception
        super().__init__(original_exception or message)


class DrillNotFoundError(Exception):
    """
    Exception raised when a drill is not found.
    """

    def __init__(self, name: str, search_paths: set[Path] | None = None) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.search_paths = search_paths
        if search_paths is None:
            message = f"Drill '{name}' not found."
        else:
            message = f"Drill '{name}' not found in any of the following paths: {search_paths}"
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

    @staticmethod
    @functools.cache
    def get_search_paths() -> set[Path]:
        """
        Returns the paths to search for drills.
        """
        return {path / "drills" for path in LIBRARY_PATHS}

    @classmethod
    def _search(cls, name: str) -> set[Path]:
        """
        Search for drills.
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
        Find a drill by its folder name.
        """
        results = cls._search(name)
        match len(results):
            case 0:
                raise DrillNotFoundError(name, cls.get_search_paths())
            case 1:
                return results.pop()
            case _:
                raise MultipleDrillsFoundError(name, results, cls.get_search_paths())

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
    def _create(data: dict[str, Any], path: Path) -> Drill:
        """
        Creates a Drill object from a dict containing the drill's metadata.
        """
        try:
            return Drill(
                id=str(data["metadata"]["id"]),
                name=str(data["metadata"]["name"]),
                description=str(
                    data["metadata"]["description"]
                    if "description" in data["metadata"]
                    else None
                ),
                path=path,
                author=str(data["metadata"]["author"]),
                repository=str(data["metadata"]["repository"]),
                dependencies=DrillDependencies(
                    system=set(data["dependencies"]["system"]),
                    python=set(data["dependencies"]["python"]),
                ),
                interface=DrillInterface(
                    arguments=tuple(data["interface"]["arguments"]),
                    return_type=str(data["interface"]["return_type"]),
                ),
            )
        except TypeError as e:
            message = "Loaded Drill data is invalid."
            raise InvalidDrillError(message, e) from e

    @classmethod
    def load(cls, name: str) -> Drill:
        """
        Load a drill by its folder name and return a Drill object.
        """
        path = cls._find(name)
        data = cls._load(path)
        return cls._create(data, path)

    @classmethod
    def load_all(cls) -> list[Drill]:
        """
        Load all drills and return a set of Drill objects.
        """
        all_drills: list[Drill] = list()
        for search_path in cls.get_search_paths():
            for path in search_path.iterdir():
                if not path.is_dir():
                    continue
                try:
                    data = cls._load(path)
                    drill = cls._create(data, path)
                    all_drills.append(drill)
                except InvalidDrillError as e:
                    message = f"Skipping invalid drill '{path.name}'"
                    logger.debug(message, exc_info=e)

        return all_drills
