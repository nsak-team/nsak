"""
Scenario entrypoint for AI based network reconnaissance with structured output.

This currently works only with frontier models.
"""

import logging
from dataclasses import dataclass

from nsak.core import create_ai_agent, config, AiAgent
from nsak.core.scenario import AIScenarioResult

logger = logging.getLogger(__name__)

reconnaissance_prompt_template = """
Steps:
1. Retrieve the network configuration with the `host_configuration` tool.
2. Discover all subnets, hosts and services with nmap on the following interface: %(interface)s
3. Enumerate all services based on the result of the network discovery result with service-specific nmap NSE scripts
4. Return a markdown formated assessment of your findings

"""

@dataclass(frozen=True, kw_only=True)
class AIScenarioUnstructuredResult(AIScenarioResult):
    """
    Adhoc result type.
    """
    ai_assessment: str

    @property
    def is_successful(self) -> bool:
        """
        Returns true if the result is considered successful.
        """
        return bool(self.ai_assessment)


    def display(self) -> str:
        """
        Returns a human-readable representation of the result, usually for stdout.
        """
        lines = [
            "### AI Scenario Unstructured Result ###",
            "",
            f"{self.ai_assessment}",
            "",
        ]

        return "\n".join(lines)

    def as_markdown(self) -> str:
        """
        Returns a Markdown representation of the result, usually for storing in a file.
        """
        return self.ai_assessment

async def run_reconnaissance_agent(
    interface: str,
    interactive: bool = False,
) -> tuple[str, AiAgent]:
    """
    Run an agent which returns a AIScenarioUnstructuredResult.
    """
    prompt = reconnaissance_prompt_template % {"interface": interface}

    if interactive:
        prompt += "\n5. Use the `human_interaction_hook` tool to allow the operator to execute followup steps."

    agent = await create_ai_agent(
        interactive,
    )
    result = await agent.ainvoke(prompt)
    response = result.get("messages", [])[-1].content

    return response, agent


async def run(interface: str, interactive: bool = False) -> AIScenarioUnstructuredResult:
    """
    Scenario, which conducts AI-based network reconnaissance.
    """

    logger.info("Starting scenario: AI Reconnaissance Unstructured Output")

    if config.ai is None:
        raise ValueError("config.ai must be configured!")

    result, agent = await run_reconnaissance_agent(
        interface,
        interactive
    )

    ai_reconnaissance_scenario_result = AIScenarioUnstructuredResult(
        ai_assessment=result,
        provider=config.ai.provider,
        model=config.ai.model,
        prompt_tokens=agent.usage.prompt_tokens,
        completion_tokens=agent.usage.completion_tokens,
        tools_called=agent.track_tool_call_middleware.tools_called,
    )

    return ai_reconnaissance_scenario_result
