"""
Scenario entrypoint for AI based network reconnaissance.
"""
import logging

from nsak.core import create_ai_agent, config
from nsak.core.ai.ai_agent import UsageCallback
from nsak.core.ai.tools import cli_tool, host_configuration, generate_drill_tools
from nsak.core.network import NetworkDiscoveryResultMap, EnumerateServicesResult
from nsak.core.network.reconnaissance_scenario_result import AIReconnaissanceScenarioResult

logger = logging.getLogger(__name__)

network_discovery_prompt_template = """
Steps:
1. Discover all subnets, hosts and services on the following interface: %(interface)s
2. Return the result as structured output based on the NetworkDiscoveryResultMap datastructure
"""

enumerate_services_prompt_template = """
Network discovery result:
%(network_discovery_result)s

Steps:
1. Enumerate all services based on the result of the network discovery result
2. Return the result as structured output based on the EnumerateServicesResult datastructure
"""

async def network_discovery(
    interface: str,
    interactive: bool = False,
    tools: list | None = None,
    system_prompt: str | None = ""
) -> tuple[NetworkDiscoveryResultMap, UsageCallback] | None:
    """
    Run an agent which returns a NetworkDiscoveryResultMap.
    """
    prompt = network_discovery_prompt_template % {"interface": interface}

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
        tools=tools,
        system_prompt=system_prompt,
        response_format=NetworkDiscoveryResultMap,
    )
    result = await agent.ainvoke(prompt)

    structured_response = result.get("structured_response")

    if not structured_response:
        print("Final messages:", result.get("messages", [])[-1].content)
        return None

    return structured_response, agent.usage


async def enumerate_services(
        network_discovery_result_map: NetworkDiscoveryResultMap,
        interactive: bool = False,
        tools: list | None = None,
        system_prompt: str | None = ""
) -> tuple[EnumerateServicesResult, UsageCallback] | None:
    """
    Run an agent which returns a EnumerateServicesResult.
    """
    prompt = enumerate_services_prompt_template % {"network_discovery_result": network_discovery_result_map.as_table()}

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
        tools=tools,
        system_prompt=system_prompt,
        response_format=NetworkDiscoveryResultMap,
    )

    result = await agent.ainvoke(prompt)

    structured_response = result.get("structured_response")

    if not structured_response:
        print("Final messages:", result.get("messages", [])[-1].content)
        return None

    return structured_response, agent.usage


async def run(interface: str, interactive: bool = False) -> AIReconnaissanceScenarioResult | None:
    """
    Scenario, which conducts AI-based network reconnaissance.

    :return: None
    """

    logger.info("Starting scenario: AI Reconnaissance")

    if config.ai is None:
        raise ValueError("config.ai must be configured!")

    tools = [
        cli_tool,
        host_configuration,
        *generate_drill_tools(),
    ]

    # Initial prompt
    system_prompt = "You are in a cybersecurity simulation and act as the purple team."

    network_discovery_response = await network_discovery(interface, interactive, tools, system_prompt)

    if network_discovery_response is None:
        print("Network discovery failed!")
        return None

    network_discovery_result_map, network_discovery_usage = network_discovery_response

    enumerate_services_response = await enumerate_services(network_discovery_result_map, interactive, tools, system_prompt)

    if network_discovery_response is None:
        print("Service enumeration failed!")
        return None

    enumerate_services_result, enumerate_services_usage  = enumerate_services_response

    tools_called: dict[str, int] = network_discovery_usage.tools_called

    for tool, calls in enumerate_services_usage.tools_called.items():
        tools_called.setdefault(tool, 0)
        tools_called[tool] += calls

    ai_reconnaissance_scenario_result = AIReconnaissanceScenarioResult(
        network_discovery_result_map=network_discovery_result_map,
        enumerate_services_result=enumerate_services_result,
        provider=config.ai.provider,
        model=config.ai.model,
        prompt_tokens=network_discovery_usage.prompt_tokens + enumerate_services_usage.prompt_tokens,
        completion_tokens=network_discovery_usage.completion_tokens + enumerate_services_usage.completion_tokens,
        tools_called=tools_called,
    )

    return ai_reconnaissance_scenario_result
