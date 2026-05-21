from dataclasses import dataclass

from nsak.core.scenario import AIScenarioResult
from nsak.core.scenario_results.reconnaissance_scenario_result import (
    ReconnaissanceScenarioResult,
)


@dataclass(frozen=True, kw_only=True)
class AIReconnaissanceScenarioResult(ReconnaissanceScenarioResult, AIScenarioResult):
    """
    Represents the results of the AI reconnaissance scenario.
    """

    ai_assessment: str

    def display(self) -> str:
        """
        Display the result of the reconnaissance scenario.
        """
        lines = [
            "### Reconnaissance Scenario Result ###",
            "",
            self.network_discovery_table.display(),
            "",
            self.enumerate_services_result.display(),
            "",
            self.ai_assessment,
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
            "## Network Discovery Result Map",
            "",
            self.network_discovery_table.as_markdown(),
            "",
            "## Enumerate Services Result",
            "",
            self.enumerate_services_result.as_markdown(),
            "",
            "## AI Assessment",
            "",
            self.ai_assessment,
        ]

        return "\n".join(lines)
