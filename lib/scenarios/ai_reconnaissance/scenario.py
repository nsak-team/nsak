"""
Scenario entrypoint for AI based network reconnaissance.
"""
import logging

from nsak.core import create_ai_agent, config
from nsak.core.ai.ai_agent import AiAgent
from nsak.core.network.reconnaissance_scenario_result import AIReconnaissanceScenarioResult

logger = logging.getLogger(__name__)

network_discovery_prompt_template = """
Run nmap to discover all interfaces on the given interface: %(interface)s

Steps:
1. Discover all subnets, hosts and services
2. Return the result as markdown based on the following example template:

| Interface   | MAC               | IP           |   Port | Protocol   | State   | Service            | Product                              | Version                 |
|:------------|:------------------|:-------------|-------:|:-----------|:--------|:-------------------|:-------------------------------------|:------------------------|
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |     53 | tcp        | open    | domain             | NLnet Labs NSD                       |                         |
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |     80 | tcp        | open    | http               | FRITZ!Box http config                |                         |
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |    443 | tcp        | open    | ssl/http           | FRITZ!Box http config                |                         |

"""

enumerate_services_prompt_template = """
Network discovery result:
%(network_discovery_result)s

Run service-specific nmap NSE scripts on all discovered services.

Steps:
1. Enumerate all services based on the result of the network discovery result
2. Return the result as markdown based on the following example template:

| IP           |   Port | Findings                                                     |
|:-------------|-------:|:-------------------------------------------------------------|
| 10.10.10.1   |     53 | dns-brute:                                                   |
|              |        | DNS Brute-force hostnames:                                   |
|              |        | dns.fritz.box - 1.0.0.1                                      |
|              |        | dns.fritz.box - 1.1.1.1                                      |
| 10.10.10.1   |     80 | http-title: FRITZ!Box                                        |
|              |        | http-headers:                                                |
|              |        | Connection: close                                            |
|              |        | Content-Length: 2148                                         |

"""

assessment_prompt_template = """
Network discovery result:
%(network_discovery_result)s

Enumerate services result:
%(enumerate_services_result)s

Steps:
1. Create an assessment based on the discovery and enumerate services result
2. Return the result as markdown
"""

async def network_discovery(
    interface: str,
    interactive: bool = False,
) -> tuple[str, AiAgent]:
    """
    Run an agent which returns a NetworkDiscoveryResultMap.
    """
    prompt = network_discovery_prompt_template % {"interface": interface}

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(interactive)
    result = await agent.ainvoke(prompt)
    response = result.get("messages", [])[-1].content

    return response, agent


async def enumerate_services(
    network_discovery_result_map: str,
    interactive: bool = False,
) -> tuple[str, AiAgent]:
    """
    Run an agent which returns a EnumerateServicesResult.
    """
    prompt = enumerate_services_prompt_template % {"network_discovery_result": network_discovery_result_map}

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(interactive)

    result = await agent.ainvoke(prompt)
    response = result.get("messages", [])[-1].content

    return response, agent

async def assessment(
    network_discovery_result_map: str,
    enumerate_services_result: str,
    interactive: bool = False,
) -> tuple[str, AiAgent]:
    """
    Run an agent which returns a EnumerateServicesResult.
    """
    prompt = assessment_prompt_template % {
        "network_discovery_result": network_discovery_result_map,
        "enumerate_services_result": enumerate_services_result,
    }

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(interactive)

    result = await agent.ainvoke(prompt)
    response = result.get("messages", [])[-1].content

    return response, agent


async def run(interface: str, interactive: bool = False) -> AIReconnaissanceScenarioResult | None:
    """
    Scenario, which conducts AI-based network reconnaissance.

    :return: None
    """

    logger.info("Starting scenario: AI Reconnaissance")

    if config.ai is None:
        raise ValueError("config.ai must be configured!")

    network_discovery_result_map, network_discovery_agent = await network_discovery(interface, interactive)

    enumerate_services_result, enumerate_services_agent = await enumerate_services(network_discovery_result_map, interactive)

    assessment_result, assessment_agent = await assessment(network_discovery_result_map, enumerate_services_result, interactive)

    prompt_tokens = 0
    completion_tokens = 0
    tools_called: dict[str, list[str]] = {}

    for agent in [network_discovery_agent, enumerate_services_agent, assessment_agent]:
        agent: AiAgent
        prompt_tokens += agent.usage.prompt_tokens
        completion_tokens += agent.usage.completion_tokens
        for tool, calls in agent.track_tool_call_middleware.tools_called.items():
            tools_called.setdefault(tool, [])
            tools_called[tool] += calls

    ai_reconnaissance_scenario_result = AIReconnaissanceScenarioResult(
        network_discovery_result_map=network_discovery_result_map,
        enumerate_services_result=enumerate_services_result,
        ai_assessment=assessment_result,
        provider=config.ai.provider,
        model=config.ai.model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        tools_called=tools_called,
    )

    return ai_reconnaissance_scenario_result
