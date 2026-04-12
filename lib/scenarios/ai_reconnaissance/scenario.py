"""
Scenario entrypoint for AI based network reconnaissance.
"""
import logging

from nsak.core import create_ai_agent

logger = logging.getLogger(__name__)

async def run(interface: str, interactive: bool = False) -> None:
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
4. List all subnets, hosts and services and state if they are vulnerable.
5. Use the `human_interaction_hook` tool to allow the operator to execute followup steps.
    """

    # Run agent
    ai_agent = await create_ai_agent(interactive)
    result = ai_agent.run(prompt)

    # Logging
    async for line in result:
        logger.warning(line)
