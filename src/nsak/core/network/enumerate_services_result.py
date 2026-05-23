import logging
from dataclasses import dataclass

from tabulate import TableFormat, tabulate

from nsak.core.scenario.scenario_result import ScenarioResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EnumerateServicesResultEntry:
    """
    Represents the entry of the enumerate services result.
    """

    ip: str
    port: str
    findings: str


@dataclass(frozen=True, kw_only=True)
class EnumerateServicesResult(ScenarioResult):
    """
    Represents the results of the enumerate services drill.
    """

    results: list[EnumerateServicesResultEntry]

    @property
    def is_successful(self) -> bool:
        """
        Return true if there are rows.
        """
        return bool(self.results)

    def as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return a human- and AI-readable table of all enumerated services.
        """
        headers = [
            "IP",
            "Port",
            "Findings",
        ]
        rows = []

        for entry in self.results:
            row = [
                entry.ip,
                entry.port,
                entry.findings,
            ]
            rows.append(row)

        if not rows:
            return "No results for enumerate services."

        return tabulate(rows, headers=headers, tablefmt=table_format)

    def display(self) -> str:
        """
        Display the result of the enumerate services drill.
        """
        lines = [
            "### Enumerate Discovery Result ###",
            "",
            self.as_table(),
            "",
        ]

        return "\n".join(lines)

    def as_markdown(self) -> str:
        """
        Return the result of the enumerate services drill as Markdown.
        """
        return self.as_table()
