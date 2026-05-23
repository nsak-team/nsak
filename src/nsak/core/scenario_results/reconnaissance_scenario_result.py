from dataclasses import dataclass

from nsak.core.network.enumerate_services_result import EnumerateServicesResult
from nsak.core.scenario.scenario_result import ScenarioResult
from nsak.core.scenario_results.network_discovery_result import NetworkDiscoveryTable


@dataclass(frozen=True, kw_only=True)
class ReconnaissanceScenarioResult(ScenarioResult):
    """
    Represents the results of the reconnaissance scenario.
    """

    network_discovery_table: NetworkDiscoveryTable
    enumerate_services_result: EnumerateServicesResult

    @property
    def is_successful(self) -> bool:
        """
        Returns true if there are actual results.
        """
        return (
            self.network_discovery_table.is_successful
            and self.enumerate_services_result.is_successful
        )

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
        ]

        return "\n".join(lines)
