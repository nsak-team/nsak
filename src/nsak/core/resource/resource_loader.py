import functools
import logging
from pathlib import Path
from typing import Any, TypeVar

import yaml

from ..settings import LIBRARY_PATHS
from .resource import Resource

T = TypeVar("T", bound=Resource)

logger = logging.getLogger(__name__)


class ResourceLoader[T]:
    """
    Finds and loads resources from the library paths.
    """

    ResourceClass: type[Resource]

    @classmethod
    @functools.cache
    def get_search_paths(cls) -> set[Path]:
        """
        Returns the paths to search for resources.
        """
        resource_path = cls.ResourceClass.KEY
        return {path / resource_path for path in LIBRARY_PATHS}

    @classmethod
    def _search(cls, name: str) -> set[Path]:
        """
        Search for resources.
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
        Find a resource by its folder name.
        """
        results = cls._search(name)
        match len(results):
            case 0:
                raise cls.ResourceClass.ResourceNotFoundError(
                    name, cls.get_search_paths()
                )
            case 1:
                return results.pop()
            case _:
                raise cls.ResourceClass.MultipleResourcesFoundError(
                    name, results, cls.get_search_paths()
                )

    @classmethod
    def _load(cls, path: Path) -> dict[str, Any]:
        """
        Load resource from a YAML file into a dict.
        """
        resource_type_name = cls.ResourceClass.NAME
        resource_type_id = resource_type_name.lower()
        yaml_file_name = f"{resource_type_id}.yaml"
        resource_yaml_path = path / yaml_file_name
        if not resource_yaml_path.exists():
            message = f"{resource_type_name} must contain a {yaml_file_name} file."
            raise cls.ResourceClass.InvalidResourceError(message)
        with open(resource_yaml_path, "r") as file:
            data = yaml.safe_load(file)
        if not isinstance(data, dict):
            message = f"Loading a {yaml_file_name} file must return a dictionary."
            raise cls.ResourceClass.InvalidResourceError(message)
        return data

    @classmethod
    def _to_resource(cls, id: str, data: dict[str, Any], path: Path) -> T:
        """
        Creates a Resource object from a dict containing the resources' metadata.
        """
        raise NotImplementedError

    @classmethod
    def _safe_to_resource(cls, id: str, data: dict[str, Any], path: Path) -> T:
        """
        Wraps `_to_resource` for generic error handling.
        """
        try:
            return cls._to_resource(id, data, path)
        except TypeError as e:
            resource_type_name = cls.ResourceClass.NAME
            message = f"Loaded {resource_type_name} data is invalid."
            raise cls.ResourceClass.InvalidResourceError(message, e) from e

    @classmethod
    def load(cls, id: str) -> T:
        """
        Load a device by its folder name and return a Device object.
        """
        path = cls._find(id)
        data = cls._load(path)
        resource_data = data[cls.ResourceClass.KEY][id]
        return cls._safe_to_resource(id, resource_data, path)

    @classmethod
    def load_all(cls) -> list[T]:
        """
        Load all devices and return a set of Device objects.
        """
        resource_type_name = cls.ResourceClass.NAME
        all_devices: list[T] = list()
        for search_path in cls.get_search_paths():
            for path in search_path.iterdir():
                if not path.is_dir():
                    continue
                try:
                    data = cls._load(path)
                    resource = cls._safe_to_resource(path.name, data, path)
                    all_devices.append(resource)
                except cls.ResourceClass.InvalidResourceError as e:
                    message = f"Skipping invalid {resource_type_name} '{path.name}'"
                    logger.warning(message, exc_info=e)

        return all_devices
