import logging
import re
import subprocess

from nsak.core.network import NetworkDiscoveryResultMap
from nsak.core.network.enumerate_services_result import EnumerateServicesResult, EnumerateServicesResultEntry

logger = logging.getLogger(__name__)

_NSE_LINE = re.compile(r"^\|[_ ]?\s*(.*)")  # nmap NSE output: "| text" or "|_ text"

# Known services get targeted scripts; everything else falls back to "banner"
# (banner grabs the initial TCP response — gives software name + version for any unknown service)
_SERVICE_SCRIPTS: dict[str, list[str]] = {
    "http":         ["http-title", "http-headers", "http-robots.txt"],
    "https":        ["http-title", "http-headers", "http-robots.txt"],
    "http-alt":     ["http-title", "http-headers", "http-robots.txt"],
    "domain":       ["dns-zone-transfer", "dns-brute"],
    "smtp":         ["smtp-commands", "smtp-enum-users"],
    "smtps":        ["smtp-commands"],
    "ftp":          ["ftp-anon", "ftp-ls"],
    "netbios-ssn":  ["smb-security-mode", "smb2-security-mode"],
    "microsoft-ds": ["smb-security-mode", "smb2-security-mode"],
    "ldap":         ["ldap-rootdse"],
    "ldapssl":      ["ldap-rootdse"],
}


def _parse_nse_output(stdout: str) -> list[str]:
    """
    Extract script result lines from nmap stdout.

    :param stdout: Raw nmap output.
    :return: Parsed output lines with pipe prefixes stripped.
    """
    findings = []
    for line in stdout.splitlines():
        m = _NSE_LINE.match(line.strip())
        if m:
            text = m.group(1).strip()
            if text:
                findings.append(text)
    return findings


def run(discovery_result: NetworkDiscoveryResultMap) -> EnumerateServicesResult:
    """
    Run service-specific nmap NSE scripts on all discovered services.

    :param discovery_result: Port-scan result from the port_scan drill.
    :return: Mapping of "ip:port" to a list of finding strings.
    """
    results: list[EnumerateServicesResultEntry] = []

    for iface_name, result in discovery_result.results.items():
        for service in result.network_services:
            scripts = _SERVICE_SCRIPTS.get(service.name or "", ["banner"])

            for endpoint in service.endpoints:
                if endpoint.ip is None or endpoint.port is None:
                    continue

                key = f"{endpoint.ip}:{endpoint.port}"
                logger.debug("Running NSE %s on %s (%s)", ",".join(scripts), key, iface_name)

                proc = subprocess.run(
                    [
                        "nmap", "--script", ",".join(scripts),
                        "-p", str(endpoint.port),
                        "-sT", "-Pn", "--host-timeout", "30s",
                        str(endpoint.ip),
                    ],
                    capture_output=True, text=True,
                )

                findings = _parse_nse_output(proc.stdout)
                if findings:
                    entry = EnumerateServicesResultEntry(
                        ip=endpoint.ip,
                        port=endpoint.port,
                        findings="\n".join(findings)
                    )
                    results.append(entry)
                    logger.debug("Found %d findings on %s", len(findings), key)

    return EnumerateServicesResult(results=results)
