import logging
import re
import subprocess
from typing import Literal

from nsak.core.network import NetworkDiscoveryResultMap, NetworkService, NetworkServiceEndpoint

logger = logging.getLogger(__name__)

# matches: "22/tcp open  ssh     OpenSSH 8.9p1"
_PORT_LINE = re.compile(r"^(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)") #compile regex once in obj (p,prot,name,version,


def parse_nmap(stdout: str) -> list[tuple[int, Literal["tcp", "udp"], str, str]]:
    """Extract open ports from nmap stdout as (port, protocol, name, version) tuples.

    :param stdout: Raw nmap output text.
    :return: List of (port, protocol, service name, version) tuples for open ports.
    """
    results = []
    # compare the output with the regex and skip if output does not match | group(0)=whole line, group(1)=port...)
    for line in stdout.splitlines():
        match = _PORT_LINE.match(line.strip())
        if match:
            port = int(match.group(1))
            protocol = match.group(2)
            name = match.group(3)
            version = match.group(4).strip()
            results.append((port, protocol, name, version))
    return results


def run(discovery_result: NetworkDiscoveryResultMap) -> NetworkDiscoveryResultMap:
    """Run nmap service scan on all target IPs and append open ports to the discovery result.

    :param discovery_result: Existing host discovery result containing target IPs per interface.
    :return: The same result map, with open port/service information.
    """
    for iface_name, result in discovery_result.results.items():
        mac_by_ip = {
            endpoint.ip: endpoint.mac
            for service in result.network_services
            for endpoint in service.endpoints
            if endpoint.ip is not None and endpoint.mac
        }
        for ip in result.target_ips:
            logger.debug("Scanning ports on %s (%s)", ip, iface_name)
            proc = subprocess.run(
                ["nmap", "-sV", "--open", str(ip)],
                capture_output=True, text=True, check=True
            )
            ports = parse_nmap(proc.stdout)
            logger.debug("Found %d open ports on %s", len(ports), ip)
            for port, protocol, name, version in ports:
                service = NetworkService(
                    endpoints=[NetworkServiceEndpoint(ip=ip, mac=mac_by_ip.get(ip), port=port, protocol=protocol)],
                    state="open",
                    name=name,
                    version=version or None,
                )
                result.network_services.append(service)
    return discovery_result
