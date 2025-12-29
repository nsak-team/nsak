import dataclasses

from nsak.core.config import MANAGEMENT_NETWORKS
from nsak.core.network.network_interface import NetworkInterface
from nsak.core.network.network_service import NetworkService
from nsak.core.network.types import IPAddress


def in_management_networks(ip: IPAddress) -> bool:
    """
    Check if an IP address is part of a management network.

    :param ip:
    :return:
    """
    for management_network in MANAGEMENT_NETWORKS:
        if ip in management_network:
            return True
    return False


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkDiscoveryResult:
    """
    Represents the results of a network discovery for a single network interface.
    """

    network_interface: NetworkInterface
    network_services: list[NetworkService]

    @property
    def ips(self) -> list[IPAddress]:
        """
        Return all IP addresses of the network interface and all network services.

        :return:
        """
        return [
            endpoint.ip
            for service in self.network_services
            for endpoint in service.endpoints
            if endpoint.ip is not None and not in_management_networks(endpoint.ip)
        ]

    @property
    def target_ips(self) -> list[IPAddress]:
        """
        Return all IP addresses that are not part of the network interface's IP address range.

        :return:
        """
        return [ip for ip in self.ips if ip not in self.network_interface.nsak_ips]

    def display(self) -> str:
        """


        :return:
        """
        lines = [f"# Services on iface {self.network_interface.name}:"]

        for service in self.network_services:
            lines.append(service.display())
        if not self.network_services:
            lines.append("No services.")

        return "\n".join(lines)


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkDiscoveryResultMap:
    """
    Represents the results of a network discovery.
    """

    results: dict[str, NetworkDiscoveryResult]

    def display(self) -> str:
        """

        :return:
        """
        lines = ["", "### Network Discovery Results: ###", ""]

        for result in self.results.values():
            lines.append(result.display())
        if not self.results:
            lines.append("No interfaces.")

        lines.extend(["", "### -------------------------- ###", ""])
        return "\n".join(lines)
