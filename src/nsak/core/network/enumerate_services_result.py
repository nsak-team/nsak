from dataclasses import dataclass

from tabulate import TableFormat, tabulate

from nsak.core.scenario import ScenarioResult


@dataclass(frozen=True, kw_only=True)
class EnumerateServicesResult(ScenarioResult):
    """
    Represents the results of the enumerate services drill.
    """

    # Service name ->
    results: dict[str, list[str]]

    def as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return a human- and AI-readable table of all enumerated services.
        """
        headers = [
            "IP",
            "Port",
            "Finding",
        ]
        rows = []

        for key, findings in self.results.items():
            for finding in findings:
                ip, port = key.split(":", 1)
                row = [
                    ip,
                    port,
                    finding,
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
