"""
Scenario entrypoint for AI based network reconnaissance.
"""
import json
import logging

from langchain.agents.structured_output import ToolStrategy

from nsak.core import create_ai_agent, config
from nsak.core.ai.ai_agent import AiAgent
from nsak.core.network import EnumerateServicesResult
from nsak.core.network.enumerate_services_result import EnumerateServicesResultEntry
from nsak.core.scenario_results.ai_reconnaissance_scenario_result import AIReconnaissanceScenarioResult
from nsak.core.scenario_results.network_discovery_result import NetworkDiscoveryTable, NetworkDiscoveryRow

logger = logging.getLogger(__name__)

network_discovery_prompt_template = """
Run nmap to discover all interfaces on the given interface: %(interface)s

Steps:
1. Discover all subnets, hosts and services
2. Return the result as structured output: NetworkDiscoveryTable

NetworkDiscoveryTable Example:

| Interface   | MAC               | IP           |   Port | Protocol   | State   | Service            | Product                              | Version                 |
|:------------|:------------------|:-------------|-------:|:-----------|:--------|:-------------------|:-------------------------------------|:------------------------|
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |     53 | tcp        | open    | domain             | NLnet Labs NSD                       |                         |
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |     80 | tcp        | open    | http               | FRITZ!Box http config                |                         |
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |    443 | tcp        | open    | ssl/http           | FRITZ!Box http config                |                         |

"""

enumerate_services_prompt_template = """
Run service-specific nmap NSE scripts on all discovered services.

Steps:
1. Enumerate all services based on the result of the network discovery result
2. Return the result as structured output: EnumerateServicesResult

EnumerateServicesResult Example:

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

Network discovery result:
%(network_discovery_result)s
"""

assessment_prompt_template = """
Steps:
1. Create an assessment based on the discovery and enumerate services result
2. Return the result as markdown

Network discovery result:
%(network_discovery_result)s

Enumerate services result:
%(enumerate_services_result)s
"""

async def network_discovery(
    interface: str,
    interactive: bool = False,
) -> tuple[NetworkDiscoveryTable, AiAgent]:
    """
    Run an agent which returns a NetworkDiscoveryResultMap.
    """
    prompt = network_discovery_prompt_template % {"interface": interface}

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
        response_format=NetworkDiscoveryTable,
    )
    result = await agent.ainvoke(prompt)
    structured_response = result.get("structured_response")

    if structured_response is None:
        response = result.get("messages", [])[-1].content
        logger.warning("The value `result.structured_response` in `network_discovery` was None. Last message was %s (%s)." % (response, type(response)))
        logger.info("Try parsing the last response with `json.loads`.")
        try:
            data = json.loads(response)
            rows = [NetworkDiscoveryRow(**row) for row in data.get("rows")]
            structured_response = NetworkDiscoveryTable(rows=rows)
            logger.info("Successfully parsed the last message with `json.loads`.")
        except Exception as e:
            logger.exception("Error while trying to parse the last message with `json.loads`.", exc_info=e)
            structured_response = NetworkDiscoveryTable(rows=[])

    return structured_response, agent


async def enumerate_services(
    network_discovery_result: str,
    interactive: bool = False,
) -> tuple[EnumerateServicesResult, AiAgent]:
    """
    Run an agent which returns a EnumerateServicesResult.
    """
    prompt = enumerate_services_prompt_template % {"network_discovery_result": network_discovery_result}

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
        response_format=EnumerateServicesResult
    )

    result = await agent.ainvoke(prompt)
    structured_response = result.get("structured_response")

    if structured_response is None:
        response = result.get("messages", [])[-1].content
        logger.warning("The value `result.structured_response` in `enumerate_services` was None. Last message was %s (%s)." % (response, type(response)))
        logger.info("Try parsing the last response with `json.loads`.")
        try:
            data = json.loads(response)
            results = [EnumerateServicesResultEntry(**result) for result in data["results"]]
            structured_response = EnumerateServicesResult(results=results)
            logger.info("Successfully parsed the last message with `json.loads`.")
        except Exception as e:
            logger.exception("Error while trying to parse the last message with `json.loads`.", exc_info=e)
            structured_response = EnumerateServicesResult(results=[])

    return structured_response, agent

async def assessment(
    network_discovery_result: str,
    enumerate_services_result: str,
    interactive: bool = False,
) -> tuple[str, AiAgent]:
    """
    Run an agent which returns a EnumerateServicesResult.
    """
    prompt = assessment_prompt_template % {
        "network_discovery_result": network_discovery_result,
        "enumerate_services_result": enumerate_services_result,
    }

    if interactive:
        prompt += "\n3. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
    )

    result = await agent.ainvoke(prompt)
    response = result.get("messages", [])[-1].content

    return response, agent


async def run(interface: str, interactive: bool = False) -> AIReconnaissanceScenarioResult:
    """
    Scenario, which conducts AI-based network reconnaissance.
    """

    logger.info("Starting scenario: AI Reconnaissance")

    if config.ai is None:
        raise ValueError("config.ai must be configured!")

    network_discovery_table, network_discovery_agent = await network_discovery(
        interface,
        interactive
    )

    enumerate_services_result, enumerate_services_agent = await enumerate_services(
        network_discovery_table.as_table(),
        interactive
    )

    assessment_result, assessment_agent = await assessment(
        network_discovery_table.as_table(),
        enumerate_services_result.as_table(),
        interactive
    )

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
        network_discovery_table=network_discovery_table,
        enumerate_services_result=enumerate_services_result,
        ai_assessment=assessment_result,
        provider=config.ai.provider,
        model=config.ai.model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        tools_called=tools_called,
    )

    return ai_reconnaissance_scenario_result
