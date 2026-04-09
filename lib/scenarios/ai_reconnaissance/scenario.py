"""
Scenario entrypoint for AI based network reconnaissance.
"""
import logging

from nsak.core import ai_agent

logger = logging.getLogger(__name__)

def run(interface: str) -> None:
    """
    Scenario, which conducts AI-based network reconnaissance.

    :return: None
    """

    logger.info("Starting scenario: AI Reconnaissance")

    # Initial prompt
    prompt = f"""
    Goal:
    Discover all subnets, hosts and services on the following interface: {interface}

    Steps:
    1. Use the the `host_configuration` tool to get the IPs and subnets on the interface.
    2. Use the `cli` tool to invoke commands like nmap to scan the subnets for available hosts.
    3. Use the `cli` tool to invoke commands like nmap to scan the host for exposed services.
    3. List all subnets, hosts and services.
    """

    # Run agent
    result = ai_agent.run(prompt)

    # Logging
    for line in result:
        logger.warning(line)

    # Altering
    # alert_system.send_mail()
