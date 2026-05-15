from __future__ import annotations

import base64
import dataclasses


@dataclasses.dataclass(kw_only=True)
class DrawioMCPConfiguration:
    """
    Configuration for accessing the drawio mcp server.
    """

    url: str
    username: str
    password: str

    @property
    def basic_auth(self) -> str:
        """
        Return the credentials prepared for usage with basic auth.
        """
        credentials = ":".join([self.username, self.password])
        return base64.b64encode(credentials.encode()).decode()
