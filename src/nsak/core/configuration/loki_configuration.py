from __future__ import annotations

import dataclasses


@dataclasses.dataclass(kw_only=True)
class LokiConfiguration:
    """
    Configuration for logging to loki.
    """

    url: str
    username: str
    password: str
