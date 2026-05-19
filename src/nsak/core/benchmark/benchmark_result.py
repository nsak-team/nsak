import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from tabulate import TableFormat, tabulate

from nsak.core.scenario import AIScenarioResult, ScenarioResult


@dataclass(frozen=True, kw_only=True)
class BenchmarkResult[ScenarioResultType = ScenarioResult | Exception]:
    """
    The result of a single benchmark run.
    """

    # Metadata
    index: int
    benchmark_uuid: uuid.UUID
    run_uuid: uuid.UUID
    scenario: str
    setup: str
    timestamp: datetime

    # Quantitative criteria
    duration_seconds: int

    # Qualitative report or none if the scenario failed
    scenario_result: ScenarioResultType

    # The file path where the benchmark result is stored as Markdown, including the scenario result or exception.
    file_path: Path

    def metadata_as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return the benchmark metadata as a table.
        """
        rows = [
            ["Benchmark UUID", str(self.benchmark_uuid)],
            ["Run index", str(self.index)],
            ["Run UUID", str(self.run_uuid)],
            ["Scenario", self.scenario],
            ["Setup", self.setup],
            ["Timestamp", self.timestamp.isoformat()],
            ["Duration (s)", str(self.duration_seconds)],
        ]

        if isinstance(self.scenario_result, AIScenarioResult):
            tools_called = []
            for tool, calls in self.scenario_result.tools_called.items():
                tools_called.append(f"{tool}: {len(calls)}")
                for call in calls:
                    tools_called.append(f"- {call}")
                tools_called.append("")
            tools_called.append("")

            rows.extend(
                [
                    ["", ""],
                    ["AI Provider", self.scenario_result.provider],
                    ["AI Model", self.scenario_result.model],
                    ["Tools called:", "\n".join(tools_called)],
                    ["Prompt tokens:", str(self.scenario_result.prompt_tokens)],
                    ["Completion tokens", str(self.scenario_result.completion_tokens)],
                    ["Total tokens", str(self.scenario_result.total_tokens)],
                ]
            )

        return tabulate(rows, headers=["Key", "Value"], tablefmt=table_format)

    def as_markdown(self) -> str:
        """
        Returns a Markdown representation of the result, usually for storing in a file.
        """
        lines = [
            f"# Benchmark Result {self.index} from Run {self.benchmark_uuid}",
            "",
            self.metadata_as_table(),
        ]

        if isinstance(self.scenario_result, ScenarioResult):
            content = self.scenario_result.as_markdown()
        else:
            # If the result is an error
            content = str(self.scenario_result)

        lines.extend(
            [
                "",
                "--------------------------------------",
                "",
                content,
            ]
        )

        return "\n".join(lines)

    def __post_init__(self) -> None:
        """
        Write the result to the given file path as Markdown.
        """
        with self.file_path.open("w+") as file:
            file.write(self.as_markdown())
