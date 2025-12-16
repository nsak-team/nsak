import functools
import logging
from pathlib import Path
from typing import Any

import yaml

from nsak.core.config import LIBRARY_PATHS
from nsak.core.scenario.scenario import (
    Scenario,
    ScenarioDependencies,
    ScenarioInterface,
)

logger = logging.getLogger(__name__)


class InvalidScenarioError(Exception):
    """
    Exception raised when a scenario is invalid.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        self.original_exception = original_exception
        super().__init__(original_exception or message)


class ScenarioNotFoundError(Exception):
    """
    Exception raised when a scenario is not found.
    """

    def __init__(self, name: str, search_paths: set[Path] | None = None) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.search_paths = search_paths
        message = (
            f"Scenario '{name}' not found in any of the following paths: {search_paths}"
        )
        super().__init__(message)


class MultipleScenariosFoundError(Exception):
    """
    Exception raised when multiple scenarios with the same folder name are found.
    """

    def __init__(self, name: str, results: set[Path], search_paths: set[Path]) -> None:
        """
        Adds the name and search paths to the exception and sets a default message.
        """
        self.name = name
        self.results = results
        self.search_paths = search_paths
        message = f"Multiple Scenarios with '{name}' found: {', '.join({str(result) for result in results})}"
        super().__init__(message)


class ScenarioLoader:
    """
    Finds and loads scenarios from the library paths.
    """

    @staticmethod
    @functools.cache
    def get_search_paths() -> set[Path]:
        """
        Returns the paths to search for scenarios.
        """
        return {path / "scenarios" for path in LIBRARY_PATHS}

    @classmethod
    def _search(cls, name: str) -> set[Path]:
        """
        Search for scenarios.
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
        Find a scenario by its folder name.
        """
        results = cls._search(name)
        match len(results):
            case 0:
                raise ScenarioNotFoundError(name, cls.get_search_paths())
            case 1:
                return results.pop()
            case _:
                raise MultipleScenariosFoundError(name, results, cls.get_search_paths())

    @staticmethod
    def _load(path: Path) -> dict[str, Any]:
        """
        Load a scenario from a YAML file into a dict.
        """
        scenario_yaml = path / "scenario.yaml"
        if not scenario_yaml.exists():
            message = "Scenario must contain a scenario.yaml file."
            raise InvalidScenarioError(message)
        with open(scenario_yaml, "r") as file:
            data = yaml.safe_load(file)
        if not isinstance(data, dict):
            message = "Loading a scenario.yaml file must return a dictionary."
            raise InvalidScenarioError(message)
        return data

    @staticmethod
    def _create(data: dict[str, Any], path: Path) -> Scenario:
        """
        Creates a Scenario object from a dict containing the scenario's metadata.
        """
        try:
            return Scenario(
                id=str(data["metadata"]["id"]),
                name=str(data["metadata"]["name"]),
                description=str(data["metadata"]["description"]),
                path=path,
                author=str(data["metadata"]["author"]),
                repository=str(data["metadata"]["repository"]),
                drills=set(data["drills"]),
                dependencies=ScenarioDependencies(
                    system=set(data["dependencies"]["system"]),
                    python=set(data["dependencies"]["python"]),
                ),
                interface=ScenarioInterface(
                    arguments=tuple(data["interface"]["arguments"]),
                    return_type=str(data["interface"]["return_type"]),
                ),
            )
        except TypeError as e:
            message = "Loaded Scenario data is invalid."
            raise InvalidScenarioError(message, e) from e

    @classmethod
    def load(cls, name: str) -> Scenario:
        """
        Load a scenario by its folder name and return a Scenario object.
        """
        path = cls._find(name)
        data = cls._load(path)
        return cls._create(data, path)

    @classmethod
    def load_all(cls) -> list[Scenario]:
        """
        Load all scenarios and return a set of Scenario objects.
        """
        all_scenarios: list[Scenario] = list()
        for search_path in cls.get_search_paths():
            for path in search_path.iterdir():
                if not path.is_dir():
                    continue
                try:
                    data = cls._load(path)
                    scenario = cls._create(data, path)
                    all_scenarios.append(scenario)
                except InvalidScenarioError as e:
                    message = f"Skipping invalid scenario '{path.name}'"
                    logger.debug(message, exc_info=e)

        return all_scenarios
