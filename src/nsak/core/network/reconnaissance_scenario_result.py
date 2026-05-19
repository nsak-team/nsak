from dataclasses import dataclass

from nsak.core.scenario import AIScenarioResult
from nsak.core.scenario.scenario_result import ScenarioResult

from .enumerate_services_result import EnumerateServicesResult
from .network_discovery_result import NetworkDiscoveryResultMap


@dataclass(frozen=True, kw_only=True)
class ReconnaissanceScenarioResult(ScenarioResult):
    """
    Represents the results of the reconnaissance scenario.
    """

    network_discovery_result_map: NetworkDiscoveryResultMap
    enumerate_services_result: EnumerateServicesResult

    def display(self) -> str:
        """
        Display the result of the reconnaissance scenario.
        """
        lines = [
            "### Reconnaissance Scenario Result ###",
            "",
            self.network_discovery_result_map.display(),
            "",
            self.enumerate_services_result.display(),
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
            self.network_discovery_result_map.as_markdown(),
            "",
            "## Enumerate Services Result",
            "",
            self.enumerate_services_result.as_markdown(),
        ]

        return "\n".join(lines)


@dataclass(frozen=True, kw_only=True)
class AIReconnaissanceScenarioResult(AIScenarioResult):
    """
    Represents the results of the AI reconnaissance scenario.
    """

    network_discovery_result_map: str
    enumerate_services_result: str
    ai_assessment: str

    def display(self) -> str:
        """
        Display the result of the reconnaissance scenario.
        """
        lines = [
            "### Reconnaissance Scenario Result ###",
            "",
            self.network_discovery_result_map,
            "",
            self.enumerate_services_result,
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
            self.network_discovery_result_map,
            "",
            "## Enumerate Services Result",
            "",
            self.enumerate_services_result,
            "",
            "## AI Assessment",
            "",
            self.ai_assessment,
        ]

        return "\n".join(lines)


@dataclass(frozen=True, kw_only=True)
class AIReconnaissanceStructuredOutputResult(
    ReconnaissanceScenarioResult, AIScenarioResult
):
    """
    Represents the results of the AI reconnaissance scenario with structured output.
    """

    ai_assessment: str

    def display(self) -> str:
        """
        Display the result of the reconnaissance scenario.
        """
        lines = [
            "### Reconnaissance Scenario Result ###",
            "",
            self.network_discovery_result_map.display(),
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
            self.network_discovery_result_map.as_markdown(),
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


@dataclass(frozen=True, kw_only=True)
class AIReconnaissanceStructuredOutputScenarioResult(
    AIReconnaissanceStructuredOutputResult, AIScenarioResult
):
    """
    Represents the results of the AI reconnaissance scenario with structured output.
    """
