"""
Scenario entrypoint for AI based network reconnaissance.
"""
import logging

from nsak.core import create_ai_agent

logger = logging.getLogger(__name__)

def run(prompt: str, interactive: bool = True) -> None:
    """
    Scenario, which runs an AI agent with a custom prompt in an interactive loop.

    After each agent response the operator is prompted for the next instruction.
    Enter an empty line or 'exit' to stop the session.

    :return: None
    """

    logger.info("Starting scenario: AI Agent")

    ai_agent = create_ai_agent(interactive)

    for line in ai_agent.run_interactive(prompt):
        logger.warning(line)
