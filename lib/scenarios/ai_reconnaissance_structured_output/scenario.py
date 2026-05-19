"""
Scenario entrypoint for AI based network reconnaissance with structured output.

This currently works only with frontier models.
"""
import logging

from nsak.core import create_ai_agent, config, AiAgent
from nsak.core.network.reconnaissance_scenario_result import AIReconnaissanceStructuredOutputScenarioResult, AIReconnaissanceStructuredOutputResult

logger = logging.getLogger(__name__)

reconnaissance_prompt_template = """
Steps:
1. Discover all subnets, hosts and services on the following interface: %(interface)s
2. Enumerate all services based on the result of the network discovery result with service-specific nmap NSE scripts
3. Write a markdown formated assessment of your findings
4. Return the result as structured output based on the ReconnaissanceScenarioResult datastructure
"""

async def run_reconnaissance_agent(
    interface: str,
    interactive: bool = False,
) -> tuple[AIReconnaissanceStructuredOutputResult, AiAgent]:
    """
    Run an agent which returns a NetworkDiscoveryResultMap.
    """
    prompt = reconnaissance_prompt_template % {"interface": interface}

    if interactive:
        prompt += "\n5. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
        response_format=AIReconnaissanceStructuredOutputResult,
        # load_additional_tools=True,
    )
    result = await agent.ainvoke(prompt)

    structured_response = result.get("structured_response")

    if not structured_response:
        logger.error("Final messages:", result.get("messages", [])[-1].content)
        raise Exception("Agent for network_discovery failed!", result)

    return structured_response, agent


async def run(interface: str, interactive: bool = False) -> AIReconnaissanceStructuredOutputScenarioResult:
    """
    Scenario, which conducts AI-based network reconnaissance.
    """

    logger.info("Starting scenario: AI Reconnaissance")

    if config.ai is None:
        raise ValueError("config.ai must be configured!")

    result, agent = await run_reconnaissance_agent(interface, interactive)

    ai_reconnaissance_scenario_result = AIReconnaissanceStructuredOutputScenarioResult(
        network_discovery_result_map=result.network_discovery_result_map,
        enumerate_services_result=result.enumerate_services_result,
        ai_assessment=result.ai_assessment,
        provider=config.ai.provider,
        model=config.ai.model,
        prompt_tokens=agent.usage.prompt_tokens,
        completion_tokens=agent.usage.completion_tokens,
        tools_called=agent.track_tool_call_middleware.tools_called,
    )

    return ai_reconnaissance_scenario_result
