import json
import statistics
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import cast

from tabulate import TableFormat, tabulate

from nsak.core.scenario import AIScenarioResult

from .benchmark_result import BenchmarkResult


@dataclass(frozen=True, kw_only=True)
class BenchmarkSummary:
    """
    An aggregated report of a benchmark, consisting of all runs and a summary.
    """

    # Metadata
    benchmark_uuid: uuid.UUID
    scenario: str
    setup: str
    timestamp: datetime

    # AI specific metadata
    model: str | None = field(default=None)
    provider: str | None = field(default=None)

    # Individual results of each benchmark run
    results: list[BenchmarkResult]

    # The file path where the benchmark summary is stored as Markdown, including the scenario result or exception.
    file_path: Path
    json_file_path: Path

    @property
    def mean_duration_seconds(self) -> int:
        """
        Returns the rounded mean duration of the runs.
        """
        durations = [result.duration_seconds for result in self.results]
        return round(statistics.mean(durations))

    @property
    def ai_results(self) -> list[BenchmarkResult[AIScenarioResult]]:
        """
        Filter all results which have a scenario_result of type `AIScenarioResult`.
        """
        ai_results: list[BenchmarkResult[AIScenarioResult]] = []

        for result in self.results:
            if isinstance(result.scenario_result, AIScenarioResult):
                ai_results.append(cast(BenchmarkResult[AIScenarioResult], result))

        return ai_results

    @property
    def mean_prompt_tokens(self) -> int | None:
        """
        Returns the rounded mean number of prompt tokens consumed.
        """
        tokens = [result.scenario_result.prompt_tokens for result in self.ai_results]

        if not tokens:
            return None

        return round(statistics.mean(tokens))

    @property
    def mean_completion_tokens(self) -> int | None:
        """
        Returns the rounded mean number of completion tokens consumed.
        """
        tokens = [
            result.scenario_result.completion_tokens for result in self.ai_results
        ]

        if not tokens:
            return None

        return round(statistics.mean(tokens))

    @property
    def mean_total_tokens(self) -> int | None:
        """
        Returns the rounded mean number of tokens consumed.
        """
        tokens = [result.scenario_result.total_tokens for result in self.ai_results]

        if not tokens:
            return None

        return round(statistics.mean(tokens))

    def metadata_as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return the benchmark metadata as a table.
        """
        rows = [
            ["Benchmark UUID", str(self.benchmark_uuid)],
            ["Scenario", self.scenario],
            ["Setup", self.setup],
            ["Timestamp", self.timestamp.isoformat()],
            ["Mean duration (s)", str(self.mean_duration_seconds)],
        ]

        if self.ai_results:
            rows.extend(
                [
                    ["", ""],
                    ["AI Provider", self.provider or ""],
                    ["AI Model", self.model or ""],
                    ["Mean prompt tokens:", str(self.mean_prompt_tokens) or ""],
                    ["Mean completion tokens", str(self.mean_completion_tokens) or ""],
                    ["Mean total tokens", str(self.mean_total_tokens) or ""],
                ]
            )

        return tabulate(rows, headers=["Key", "Value"], tablefmt=table_format)

    def as_table(self, table_format: str | TableFormat = "pipe") -> str:
        """
        Return a human- and AI-readable table of all results included in the summary.
        """
        headers = [
            "Run Index",
            "Run UUID",
            "Timestamp",
            "Duration (s)",
            "Report path",
            "Prompt tokens",
            "Completion tokens",
            "Total tokens",
        ]
        rows = []

        for result in self.results:
            relative_file_path = result.file_path.relative_to(self.file_path.parent)
            row = [
                result.index,
                result.run_uuid,
                result.timestamp,
                result.duration_seconds,
                "[%(link)s](%(link)s)" % {"link": relative_file_path},
            ]
            if isinstance(result.scenario_result, AIScenarioResult):
                row.append(result.scenario_result.prompt_tokens)
                row.append(result.scenario_result.completion_tokens)
                row.append(result.scenario_result.total_tokens)
            rows.append(row)

        if not rows:
            return "No results available."

        return tabulate(rows, headers=headers, tablefmt=table_format)

    def as_markdown(self) -> str:
        """
        Returns a Markdown representation of the summary, usually for storing in a file.
        """
        lines = [
            f"# Benchmark Summary of Run {self.benchmark_uuid}",
            "",
            self.metadata_as_table(),
            "",
            "--------------------------------------",
            "",
            self.as_table(),
        ]

        return "\n".join(lines)

    def as_dict(self) -> dict[str, str | int | list[int] | None]:
        """
        Return the benchmark summary as a dictionary, e.g. for exporting to json.
        """
        data = {
            "benchmark_uuid": str(self.benchmark_uuid),
            "setup": self.setup,
            "scenario": self.scenario,
            "timestamp": self.timestamp.isoformat(),
            "model": self.model,
            "provider": self.provider,
            "durations": [result.duration_seconds for result in self.results],
            "tokens": None,
            "tool_calls": None,
            "mean_tokens": None,
            "mean_duration": self.mean_duration_seconds,
        }

        if self.ai_results:
            tokens: list[int] = []
            tool_calls: list[int] = []
            for result in self.ai_results:
                tokens.append(result.scenario_result.total_tokens)
                tokens.append(result.scenario_result.total_tools_called)
            data.update(
                {
                    "tokens": tokens,
                    "tool_calls": tool_calls,
                    "mean_tokens": self.mean_total_tokens,
                }
            )

        return data

    def __post_init__(self) -> None:
        """
        Write the result to the given file path as Markdown.
        """
        with self.file_path.open("w+") as file:
            file.write(self.as_markdown())
        with self.json_file_path.open("w+") as json_file:
            json.dump(self.as_dict(), json_file, indent=4)
