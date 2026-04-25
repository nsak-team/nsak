import sys
from ipaddress import IPv4Address
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from drill import parse_nmap_result  # noqa: E402


NMAP_OUTPUT_WITH_MAC = """\
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-01 12:00 UTC
Nmap scan report for 192.168.1.1
Host is up (0.00034s latency).
MAC Address: AA:BB:CC:DD:EE:FF (Cisco)

Nmap scan report for 192.168.1.2
Host is up (0.00020s latency).
MAC Address: 11:22:33:44:55:66 (Unknown)

Nmap done: 256 IP addresses (2 hosts up) scanned in 2.50 seconds
"""

NMAP_OUTPUT_WITHOUT_MAC = """\
Nmap scan report for 10.0.2.1
Host is up (0.00034s latency).

Nmap scan report for 10.0.2.2
Host is up (0.00020s latency).
"""

NMAP_OUTPUT_WITH_HOSTNAME = """\
Nmap scan report for router.local (192.168.1.254)
Host is up.
MAC Address: DE:AD:BE:EF:00:01 (Vendor Inc)
"""


def test_parse_nmap_result_with_mac() -> None:
    results = parse_nmap_result(NMAP_OUTPUT_WITH_MAC)

    assert len(results) == 2
    assert results[0].ip == IPv4Address("192.168.1.1")
    assert results[0].mac == "AA:BB:CC:DD:EE:FF"
    assert results[1].ip == IPv4Address("192.168.1.2")
    assert results[1].mac == "11:22:33:44:55:66"


def test_parse_nmap_result_without_mac() -> None:
    results = parse_nmap_result(NMAP_OUTPUT_WITHOUT_MAC)

    assert len(results) == 2
    assert results[0].ip == IPv4Address("10.0.2.1")
    assert results[0].mac == ""
    assert results[1].ip == IPv4Address("10.0.2.2")
    assert results[1].mac == ""


def test_parse_nmap_result_with_hostname() -> None:
    results = parse_nmap_result(NMAP_OUTPUT_WITH_HOSTNAME)

    assert len(results) == 1
    assert results[0].ip == IPv4Address("192.168.1.254")
    assert results[0].mac == "DE:AD:BE:EF:00:01"


def test_parse_nmap_result_empty() -> None:
    results = parse_nmap_result("")

    assert results == []
