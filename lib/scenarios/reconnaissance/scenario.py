"""
Scenario entrypoint for Reconnaissance .
"""
import logging
from dataclasses import dataclass

from scapy.arch import get_if_addr

from nsak.core import DrillManager
from nsak.core.network import NetworkDiscoveryResultMap
from nsak.core.network.enumerate_services_result import EnumerateServicesResult
from nsak.core.scenario import ScenarioResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ReconnaissanceScenarioResult(ScenarioResult):
    """
    Represents the results of the test scenario.
    """
    network_discovery_result_map: NetworkDiscoveryResultMap
    enumerate_services_result: EnumerateServicesResult

    def display(self) -> str:
        """
        Display the result of the test scenario.
        """
        lines = [
            "### Reconnaissance Scenario Result ###",
            "",
            self.network_discovery_result_map.display(),
            "",
            self.enumerate_services_result.display(),
            "",
        ]

        return "\n".join(lines)

    def as_markdown(self) -> str:
        """
        Return the result of the test scenario as Markdown.
        """
        lines = [
            "# Test Scenario Result",
            "",
            "## Network Discovery Result Map",
            "",
            self.network_discovery_result_map.as_markdown(),
            "",
            "## Enumerate Services Result",
            "",
            self.enumerate_services_result.as_markdown(),
        ]

        return "\n".join(lines)


def run(interface: str | None = None, subnet: str | None = None) -> ReconnaissanceScenarioResult:
    """
    Scenario, which runs Reconnaissance attack.
    1. If no interface is specified, scan all active physical interfaces
    2. If no interface is specified, scan all active physical interfaces
    3. Discover network on ifc and subnet
    :return: None
    """
    if interface is None:
        discovered = DrillManager.execute("discover_network_interfaces")
        interfaces_to_scan = [iface.name for iface in discovered]
    else:
        interfaces_to_scan = [interface]

    all_results = {}
    for iface_name in interfaces_to_scan:
        if get_if_addr(iface_name) in ("0.0.0.0", ""):
            DrillManager.execute("dhcp_request", interface=iface_name)

        network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
            "discover_hosts",
            interface=iface_name,
            subnet=subnet,
        )
        all_results.update(network_discovery_result_map.results)

    network_discovery_result_map = NetworkDiscoveryResultMap(results=all_results)
    DrillManager.execute("port_scan", discovery_result=network_discovery_result_map)
    enumerate_services_result: EnumerateServicesResult = DrillManager.execute(
        "enumerate_services", discovery_result=network_discovery_result_map
    )

    result = ReconnaissanceScenarioResult(
        network_discovery_result_map=network_discovery_result_map,
        enumerate_services_result=enumerate_services_result
    )
    logger.info(result.display())
    return result
