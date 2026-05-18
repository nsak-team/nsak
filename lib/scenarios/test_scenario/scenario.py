"""
scenario entrypoint for drill POC.
"""

import logging
from nsak.core import DrillManager

logger = logging.getLogger(__name__)

from dataclasses import dataclass

from nsak.core.scenario import ScenarioResult


@dataclass(frozen=True, kw_only=True)
class TestScenarioResult(ScenarioResult):
    """
    Represents the results of the test scenario.
    """
    value: str

    def display(self) -> str:
        """
        Display the result of the test scenario.
        """
        lines = [
            "### Test Scenario Result ###",
            "",
            self.value,
            "",
        ]

        return "\n".join(lines)

    def as_markdown(self) -> str:
        """
        Return the result of the test scenario as Markdown.
        """
        lines = [
            "# Test Scenario Result",
            "",
            "```bash",
            self.value,
            "```",
            "",
        ]

        return "\n".join(lines)


def run() -> TestScenarioResult:
    """
    Example Scenario, which runs the Hello World Drill.
    """
    drill = DrillManager.get("hello_world")
    value = DrillManager.execute(drill)
    result = TestScenarioResult(value=value)
    logger.info(result.display())
    return result


if __name__ == "__main__":
    run()
