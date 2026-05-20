import time
from copy import copy
from pathlib import Path
from typing import Any, cast

from nsak.core import Scenario, ScenarioManager, config
from nsak.core.benchmark.benchmark_result import BenchmarkResult
from nsak.core.benchmark.benchmark_summary import BenchmarkSummary
from nsak.core.scenario import ScenarioResult
from nsak.core.settings import BENCHMARK_PATH


class BenchmarkRun:
    """
    Harness for benchmarking scenarios.
    """

    def __init__(
        self,
        scenario: Scenario,
        setup_name: str,
        scenario_kwargs: dict[str, Any],
    ) -> None:
        """
        Initialize a benchmark run.
        """
        # Copy the current run_id, as it will be reset later on
        self.benchmark_uuid = copy(config.run_uuid)
        self.benchmark_timestamp = config.now()

        self.setup_name = setup_name
        self.scenario = scenario
        self.scenario_kwargs = scenario_kwargs

        self.work_path = self._setup_work_path()

    def execute(
        self,
        run_count: int = 10,
    ) -> BenchmarkSummary:
        """
        Execute a benchmark run.
        """
        benchmark_results: list[BenchmarkResult] = []

        for index in range(1, run_count + 1):
            # Reset the run_uuid so each run can be identified
            run_uuid = config.reset_run_uuid()

            duration_start = time.perf_counter()
            try:
                scenario_result = ScenarioManager.execute(
                    self.scenario, **self.scenario_kwargs
                )
                scenario_result = cast(ScenarioResult, scenario_result)
            except Exception as e:
                scenario_result = e
            duration_end = time.perf_counter()
            duration: int = int(duration_end - duration_start)

            benchmark_result = BenchmarkResult(
                index=index,
                benchmark_uuid=self.benchmark_uuid,
                run_uuid=run_uuid,
                timestamp=config.now(),
                scenario=self.scenario.name,
                setup=self.setup_name,
                duration_seconds=duration,
                scenario_result=scenario_result,
                file_path=self._get_result_file_path(index),
            )

            benchmark_results.append(benchmark_result)

        return BenchmarkSummary(
            benchmark_uuid=self.benchmark_uuid,
            timestamp=self.benchmark_timestamp,
            scenario=self.scenario.name,
            setup=self.setup_name,
            results=benchmark_results,
            **self._get_ai_metadata(),
            file_path=self._get_summary_file_path(),
            json_file_path=self._get_json_file_path(),
        )

    def _setup_work_path(
        self,
    ) -> Path:
        """
        Set up the work path for storing the result and summary files.
        """
        # The goal is a path like: run/benchmarks/<setup>/<scenario>/<timestamp>-<uuid>/
        directories = [
            self.setup_name,
            self.scenario.path.name,
            f"{self.benchmark_timestamp.strftime('%Y-%m-%d-%H:%M:%S')}",
        ]
        work_path: Path = BENCHMARK_PATH.joinpath(*directories)
        work_path.mkdir(mode=0o777, parents=True, exist_ok=True)
        return work_path

    def _get_result_file_path(self, index: int) -> Path:
        """
        Return the result file path.
        """
        file_name = f"result_{index}.md"
        return self.work_path.joinpath(file_name)

    def _get_summary_file_path(self) -> Path:
        """
        Return the summary file path.
        """
        file_name = "summary.md"
        return self.work_path.joinpath(file_name)

    def _get_json_file_path(self) -> Path:
        """
        Return the summary file path.
        """
        file_name = "summary.json"
        return self.work_path.joinpath(file_name)

    @staticmethod
    def _get_ai_metadata() -> dict[str, str | None]:
        """
        Return the AI metadata if available.
        """
        ai_metadata: dict[str, str | None] = {}

        if config.ai is not None:
            ai_metadata = dict(
                provider=config.ai.provider,
                model=config.ai.model,
            )
        else:
            ai_metadata = dict(
                provider=None,
                model=None,
            )

        return ai_metadata
