"""
Scenario entrypoint for AI based intrusion detection.
"""

from nsak.core import ai_agent


def run(interface: str) -> None:
    """
    Scenario, which listens to network traffic and tries to detect intruders.

    :return: None
    """

    # @TODO: This is just the starting idea.
    prompt = "Listen to network traffic via T-Shark and return if you detect an intruder."
    ai_agent.run(prompt)
