from dataclasses import dataclass

from tabulate import TableFormat, tabulate

from nsak.core.scenario.scenario_result import ScenarioResult


@dataclass(frozen=True, kw_only=True)
class NetworkDiscoveryRow:
    """
    Simplified network discovery datastructure for AI structured output.
    """

    interface: str
    mac: str
    ip: str
    port: str
    protocol: str
    state: str
    service: str
    product: str
    version: str


@dataclass(frozen=True, kw_only=True)
class NetworkDiscoveryTable(ScenarioResult):
    """
    Simplified network discovery datastructure for AI structured output.
    """

    rows: list[NetworkDiscoveryRow]

    @property
    def is_successful(self) -> bool:
        """
        Return true if there are rows.
        """
        return bool(self.rows)

    def as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return a human- and AI-readable table of all discovered services.
        """
        headers = [
            "Interface",
            "MAC",
            "IP",
            "Port",
            "Protocol",
            "State",
            "Service",
            "Product",
            "Version",
        ]
        rows = []
        for row in self.rows:
            rows.append(
                [
                    row.interface,
                    row.mac,
                    row.ip,
                    row.port,
                    row.protocol,
                    row.state,
                    row.service,
                    row.product,
                    row.version,
                ]
            )

        if not rows:
            return "No network services discovered."

        return tabulate(rows, headers=headers, tablefmt=table_format)

    def display(self) -> str:
        """
        Display the result of the reconnaissance scenario.
        """
        lines = [
            "### AI Network Discovery Table ###",
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
