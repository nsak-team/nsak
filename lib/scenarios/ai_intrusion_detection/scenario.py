"""
Scenario entrypoint for AI based intrusion detection.
"""
import ipaddress
import logging
import subprocess

from nsak.core import ai_agent, DrillManager
from nsak.core.network import NetworkDiscoveryResultMap

logger = logging.getLogger()

PACKET_COUNT = 200
CAPTURE_DURATION = 60  # seconds


def run(interface: str) -> None:
    """
    Scenario, which listens to network traffic and tries to detect intruders.

    :return: None
    """
    logger.info("Starting scenario: AI Intrusion Detection")

    host_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute("discover_hosts", interface=interface)

    # Capture traffic and extract fields including MAC addresses
    result = subprocess.run(
        [
            "tshark",
            "-i", interface,
            "-c", str(PACKET_COUNT),
            "-a", f"duration:{CAPTURE_DURATION}",
            "-n",
            "-T", "fields",
            "-e", "frame.number",
            "-e", "eth.src",
            "-e", "eth.dst",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "tcp.dstport",
            "-e", "udp.dstport",
            "-e", "frame.protocols",
            "-e", "frame.len",
            "-E", "header=y",
            "-E", "separator=,",
        ],
        capture_output=True,
        text=True,
        timeout=CAPTURE_DURATION + 10,
    )

    csv_summary = result.stdout.strip()

    if not csv_summary:
        logger.info("No relevant traffic captured.")
        return

    prompt = f"""
You are analyzing network traffic for intrusion detection on interface {interface}.

Network Discovery Result Map:
{host_discovery_result_map.as_table()}

Captured packets (CSV):
{csv_summary}

Identify at most 5 suspicious events if any. For each, output:
- src/dst IP and MAC
- protocol
- reason it is suspicious

Identify malicious hosts (MAC and/or IP) if any.

Be concise. Do not repeat packet data.
"""

    for line in ai_agent.run(prompt):
        logger.warning(line)
