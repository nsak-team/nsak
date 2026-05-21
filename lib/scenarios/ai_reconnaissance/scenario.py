"""
Scenario entrypoint for AI based network reconnaissance with structured output.

This currently works only with frontier models.
"""
import json
import logging
from dataclasses import dataclass

from langchain.agents.structured_output import ToolStrategy

from nsak.core import create_ai_agent, config, AiAgent
from nsak.core.network import EnumerateServicesResult
from nsak.core.network.enumerate_services_result import EnumerateServicesResultEntry
from nsak.core.scenario_results.ai_reconnaissance_scenario_result import AIReconnaissanceScenarioResult
from nsak.core.scenario_results.network_discovery_result import NetworkDiscoveryTable, NetworkDiscoveryRow
from nsak.core.scenario_results.reconnaissance_scenario_result import ReconnaissanceScenarioResult

logger = logging.getLogger(__name__)

reconnaissance_prompt_template = """
Steps:
1. Discover all subnets, hosts and services with nmap on the following interface: %(interface)s
2. Enumerate all services based on the result of the network discovery result with service-specific nmap NSE scripts
3. Write a markdown formated assessment of your findings
4. Return the result as structured output: [ReconnaissanceScenarioResult, str]

NetworkDiscoveryTable Example:

| Interface   | MAC               | IP           |   Port | Protocol   | State   | Service            | Product                              | Version                 |
|:------------|:------------------|:-------------|-------:|:-----------|:--------|:-------------------|:-------------------------------------|:------------------------|
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |     53 | tcp        | open    | domain             | NLnet Labs NSD                       |                         |
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |     80 | tcp        | open    | http               | FRITZ!Box http config                |                         |
| wlan0       | 80:23:95:01:fc:83 | 10.10.10.1   |    443 | tcp        | open    | ssl/http           | FRITZ!Box http config                |                         |

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

"""

@dataclass(frozen=True, kw_only=True)
class Result:
    """
    Adhoc result type.
    """
    result: ReconnaissanceScenarioResult
    assessment: str

async def run_reconnaissance_agent(
    interface: str,
    interactive: bool = False,
) -> tuple[Result, AiAgent]:
    """
    Run an agent which returns a NetworkDiscoveryResultMap.
    """
    prompt = reconnaissance_prompt_template % {"interface": interface}

    if interactive:
        prompt += "\n5. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
        response_format=Result,
    )
    result = await agent.ainvoke(prompt)

    structured_response = result.get("structured_response")

    if structured_response is None:
        response = result.get("messages", [])[-1].content
        logger.warning("The value `result.structured_response` in `run_reconnaissance_agent` was None. Last message was %s (%s)." % (response, type(response)))
        logger.info("Try parsing the last response with `json.loads`.")
        try:
            data = json.loads(response)
            rows = [NetworkDiscoveryRow(**row) for row in data["result"]["network_discovery_table"]["rows"]]
            results = [EnumerateServicesResultEntry(**result) for result in data["result"]["enumerate_services_result"]["results"]]
            structured_response = Result(
                result=ReconnaissanceScenarioResult(
                    network_discovery_table=NetworkDiscoveryTable(rows=rows),
                    enumerate_services_result=EnumerateServicesResult(results=results)
                ),
                assessment=data["assessment"]
            )
            logger.info("Successfully parsed the last message with `json.loads`.")
        except Exception as e:
            print(result.get("messages", []))
            logger.exception("Error while trying to parse the last message with `json.loads`.", exc_info=e)
            raise ValueError("Could get structured output from response!")

    return structured_response, agent


async def run(interface: str, interactive: bool = False) -> AIReconnaissanceScenarioResult:
    """
    Scenario, which conducts AI-based network reconnaissance.
    """

    logger.info("Starting scenario: AI Reconnaissance")

    if config.ai is None:
        raise ValueError("config.ai must be configured!")

    result, agent = await run_reconnaissance_agent(
        interface,
        interactive
    )

    ai_reconnaissance_scenario_result = AIReconnaissanceScenarioResult(
        network_discovery_table=result.result.network_discovery_table,
        enumerate_services_result=result.result.enumerate_services_result,
        ai_assessment=result.assessment,
        provider=config.ai.provider,
        model=config.ai.model,
        prompt_tokens=agent.usage.prompt_tokens,
        completion_tokens=agent.usage.completion_tokens,
        tools_called=agent.track_tool_call_middleware.tools_called,
    )

    return ai_reconnaissance_scenario_result
