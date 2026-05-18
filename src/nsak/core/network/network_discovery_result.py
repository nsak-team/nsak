import dataclasses

from tabulate import TableFormat, tabulate

from nsak.core.network.network_service import NetworkService
from nsak.core.network.types import IPAddress
from nsak.core.scenario import ScenarioResult

from .configuration import EthernetConfiguration


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkDiscoveryResult:
    """
    Represents the results of a network discovery for a single network interface.
    """

    network_interface: EthernetConfiguration
    network_services: list[NetworkService]

    @property
    def ips(self) -> list[IPAddress]:
        """
        Return all IP addresses of the network interface and all network services.
        """
        return [
            endpoint.ip
            for service in self.network_services
            for endpoint in service.endpoints
            if endpoint.ip is not None
        ]

    @property
    def target_ips(self) -> list[IPAddress]:
        """
        Return all IP addresses that are not part of the network interface's IP address range.
        """
        return [ip for ip in self.ips if ip not in self.network_interface.ips]

    def display(self) -> str:
        """
        Return a human-readable representation of a network discovery result.

        Recursively resolves all display methods of the services and wraps them with a start and an end.
        """
        lines = [f"# Services on iface {self.network_interface.name}:"]

        for service in self.network_services:
            lines.append(service.display())
        if not self.network_services:
            lines.append("No services.")

        return "\n".join(lines)


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkDiscoveryResultMap(ScenarioResult):
    """
    Represents the results of a network discovery.
    """

    results: dict[str, NetworkDiscoveryResult]

    def display(self) -> str:
        """
        Return a human-readable representation of a network discovery result map.

        Recursively resolves all display methods of the results and wraps them with a start and an end.
        """
        lines = ["", "### Network Discovery Results: ###", ""]

        for result in self.results.values():
            lines.append(result.display())
        if not self.results:
            lines.append("No interfaces.")

        lines.extend(["", "### -------------------------- ###", ""])
        return "\n".join(lines)

    def as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return a human- and AI-readable table of all discovered network services.

        Each row represents one endpoint with its associated service metadata.
        """
        headers = [
            "Interface",
            "MAC",
            "IP",
            "Port",
            "Protocol",
            "State",
            "Service",
            "Product",
            "Version",
        ]
        rows = []

        for iface_name, result in self.results.items():
            for service in result.network_services:
                for endpoint in service.endpoints:
                    rows.append(
                        [
                            iface_name,
                            endpoint.mac or "",
                            str(endpoint.ip) if endpoint.ip is not None else "",
                            str(endpoint.port) if endpoint.port is not None else "",
                            endpoint.protocol or "",
                            service.state or "",
                            service.name or "",
                            service.product or "",
                            service.version or "",
                        ]
                    )

        if not rows:
            return "No network services discovered."

        return tabulate(rows, headers=headers, tablefmt=table_format)

    def as_markdown(self) -> str:
        """
        Return the network discovery result as Markdown.
        """
        return self.as_table()
