from pathlib import Path
from typing import Any

from nsak.core.environment.environment import Environment
from nsak.core.resource import ResourceLoader


class EnvironmentLoader(ResourceLoader[Environment]):
    """
    Finds and loads environments from the library paths.
    """

    ResourceClass = Environment

    @classmethod
    def _to_resource(cls, data: dict[str, Any], path: Path) -> Environment:
        """
        Creates an Environment object from a dict containing the environment's metadata.
        """
        return Environment(
            id=str(data["metadata"]["id"]),
            name=str(data["metadata"]["name"]),
            path=path,
            author=str(data["metadata"]["author"]),
            repository=str(data["metadata"]["repository"]),
        )
