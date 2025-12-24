import dataclasses
from typing import Literal

from nsak.core.network.types import IPAddress


@dataclasses.dataclass(kw_only=True)
class NetworkServiceEndpoint:
    """
    Represents an endpoint of a network service.

    It should be possible to convert an endpoint to a `sockets.socket`.
    """

    mac: str | None = None
    ip: IPAddress | None = None
    port: int | None = None
    protocol: Literal["tcp", "udp"] | None = None
    extra_info: str | None = None

    def display(self) -> str:
        """


        :return:
        """
        return f"{self.mac} {self.ip}:{self.port} / {self.protocol}"


@dataclasses.dataclass(kw_only=True)
class NetworkService:
    """
    Represents a network service, which can be served by multiple endpoints.

    The fields are inspired by the results provided by nmap.
    """

    endpoints: list[NetworkServiceEndpoint]
    state: str | None = None  # e.g. open / closed / filtered
    name: str | None = None  # e.g. http, ssh
    product: str | None = None  # e.g. Apache
    version: str | None = None
    extra_info: str | None = None

    def display(self) -> str:
        """


        :return:
        """
        lines = [self.name or "Unknown service"]

        for endpoint in self.endpoints:
            lines.append(endpoint.display())
        if not self.endpoints:
            lines.append("No endpoints.")

        return "\n".join(lines)
