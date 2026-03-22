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
    def _to_resource(
        cls, id: str, data: dict[str, Any], path: Path | str
    ) -> Environment:
        """
        Creates an Environment object from a dict containing the environment's metadata.
        """
        if isinstance(path, str):
            path = Path(path)

        return Environment(
            id=id,
            name=str(data.get("name") or ""),
            description=str(data.get("description") or ""),
            path=path,
            author=str(data.get("author") or ""),
            repository=str(data.get("repository") or ""),
        )
