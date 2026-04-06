from __future__ import annotations

import dataclasses


@dataclasses.dataclass(kw_only=True)
class AiConfiguration:
    """
    Configuration for the AI agent backend.
    """

    model: str
    base_url: str
