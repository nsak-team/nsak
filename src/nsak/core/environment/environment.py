import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Environment:
    """
    Represents an environment.
    """

    id: str
    name: str
    path: Path
    author: str
    repository: str
