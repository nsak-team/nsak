from __future__ import annotations

import dataclasses


@dataclasses.dataclass(kw_only=True)
class AiConfiguration:
    """
    Configuration for the AI agent backend.
    """

    provider: str
    model: str
    base_url: str
    api_key: str | None = dataclasses.field(default=None)
