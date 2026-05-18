"""
Scenario entrypoint for AI based network reconnaissance.
"""
import logging

from nsak.core import create_ai_agent

logger = logging.getLogger(__name__)

async def run(prompt: str, interactive: bool = True) -> None:
    """
    Scenario, which runs an AI agent with a custom prompt in an interactive loop.

    After each agent response the operator is prompted for the next instruction.
    Enter an empty line or 'exit' to stop the session.

    :return: None
    """

    logger.info("Starting scenario: AI Agent")

    ai_agent = await create_ai_agent(interactive)
    result = ai_agent.run(prompt, interactive=interactive)

    response_parts: list[str] = []
    async for chunk in result:
        response_parts.append(chunk)
