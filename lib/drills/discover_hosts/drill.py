import logging
import dataclasses
import subprocess
from ipaddress import IPv4Address, IPv6Address

from nsak.core import IPAddress
from nsak.core import config
from nsak.core.network import NetworkDiscoveryResultMap, NetworkDiscoveryResult, NetworkService, NetworkServiceEndpoint
from nsak.core.network.configuration import EthernetConfiguration

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True, kw_only=True)
class ARPScanResult:
    ip: IPAddress
    mac: str
    vendor: str


def parse_arp_scan_result(arp_scan_result_output: str) -> list[ARPScanResult]:
    """

    :param arp_scan_result_output:
    :return:
    """

    entries = []
    for line in arp_scan_result_output.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue

        raw_ip, mac = parts[:2]
        try:
            ip = IPv4Address(raw_ip)
        except ValueError:
            ip = IPv6Address(raw_ip)
        vendor = parts[2] if len(parts) == 3 else ""
        entries.append(ARPScanResult(ip=ip, mac=mac, vendor=vendor))

    return entries


def parse_nmap_result(nmap_output: str) -> list[ARPScanResult]:
    """
    Parses the output of `nmap -sn` into a list of ARPScanResults.

    Uses a stateful approach since IP and MAC appear on separate lines per host.
    Hosts without a MAC address (e.g. remote subnets) are included with an empty mac field.
    """
    results = []
    current_ip = None
    current_mac = ""
    current_vendor = ""

    for line in nmap_output.splitlines():
        if line.startswith("Nmap scan report for "):
            if current_ip is not None:
                results.append(ARPScanResult(ip=current_ip, mac=current_mac, vendor=current_vendor))
            rest = line.removeprefix("Nmap scan report for ")
            raw_ip = rest.split("(")[1].rstrip(")") if "(" in rest else rest.strip()
            try:
                current_ip = IPv4Address(raw_ip)
            except ValueError:
                try:
                    current_ip = IPv6Address(raw_ip)
                except ValueError:
                    current_ip = None
            current_mac = ""
            current_vendor = ""
        elif line.startswith("MAC Address:") and current_ip is not None:
            parts = line.split(None, 3)
            current_mac = parts[2] if len(parts) > 2 else ""
            current_vendor = parts[3].strip("()") if len(parts) > 3 else ""

    if current_ip is not None:
        results.append(ARPScanResult(ip=current_ip, mac=current_mac, vendor=current_vendor))

    return results


def discover_hosts(network_interface: EthernetConfiguration) -> NetworkDiscoveryResult:
    hosts: list[NetworkService] = []
    # --localnet: Generates addresses from the interface configuration
    # -x: Only prints results to the output (no headers, etc.)
    completed_process = subprocess.run([
        "/usr/sbin/arp-scan",
        "--interface", network_interface.name,
        "--localnet", "-x",
    ], capture_output=True, text=True, check=True)

    for result in parse_arp_scan_result(completed_process.stdout):
        host = NetworkService(
            endpoints=[
                NetworkServiceEndpoint(
                    ip=result.ip,
                    mac=result.mac,
                    extra_info=result.vendor,
                )
            ]
        )
        hosts.append(host)
        logger.debug("Discovered host: %s (%s) on %s", result.ip, result.mac, network_interface.name)

    logger.debug("Found %d hosts on %s", len(hosts), network_interface.name)
    return NetworkDiscoveryResult(
        network_interface=network_interface,
        network_services=hosts,
    )


def discover_hosts_in_subnet(network_interface: EthernetConfiguration, subnet: str) -> NetworkDiscoveryResult:
    """
    Uses `nmap -sn` to discover hosts in an arbitrary subnet, including remote ones.

    Unlike discover_hosts(), this works across routers (Layer 3).
    MAC addresses are only available if the target subnet is on the same Layer 2 segment.
    The network_interface is used as the egress interface reference for the result.
    """
    hosts: list[NetworkService] = []
    completed_process = subprocess.run(
        ["nmap", "-sn", subnet],
        capture_output=True, text=True, check=True,
    )

    for result in parse_nmap_result(completed_process.stdout):
        host = NetworkService(
            endpoints=[
                NetworkServiceEndpoint(
                    ip=result.ip,
                    mac=result.mac,
                    extra_info=result.vendor,
                )
            ]
        )
        hosts.append(host)
        logger.debug("Discovered host: %s (%s) in subnet %s", result.ip, result.mac, subnet)

    logger.debug("Found %d hosts in subnet %s", len(hosts), subnet)
    return NetworkDiscoveryResult(
        network_interface=network_interface,
        network_services=hosts,
    )


def run(interface: str, subnet: str | None = None) -> NetworkDiscoveryResultMap:
    """
    Discovers hosts on the given interface.

    If subnet is None, uses arp-scan to find hosts on the local network segment.
    If subnet is provided (e.g. "10.0.2.0/24"), uses nmap -sn to scan that subnet instead.
    """
    results = dict()
    ethernet = config.device.get_ethernet(interface)
    try:
        if subnet is not None:
            results[ethernet.name] = discover_hosts_in_subnet(ethernet, subnet)
        else:
            results[ethernet.name] = discover_hosts(ethernet)
    except subprocess.CalledProcessError:
        logger.exception(f"Error while discovering hosts for interface: {ethernet.name}.")
    return NetworkDiscoveryResultMap(results=results)
