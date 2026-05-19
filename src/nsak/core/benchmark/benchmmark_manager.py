import subprocess
from typing import Any

from nsak.core import Scenario, ScenarioManager
from nsak.core.benchmark import BenchmarkRun
from nsak.core.benchmark.benchmark_summary import BenchmarkSummary


class BenchmarkManager:
    """
    Manager class for benchmark runs.
    """

    @classmethod
    def run(
        cls,
        scenario: Scenario,
        setup_name: str,
        run_count: int = 10,
        **kwargs: dict[str, Any],
    ) -> int:
        """
        Run a benchmark via container.
        """
        _args = ScenarioManager.build_run_args(scenario, **kwargs)
        args = _args[:10]
        args.extend(
            [
                "--entrypoint",
                "nsak",
                _args[10],  # image name
                "benchmark",
                "execute",
                scenario.path.name,
                setup_name,
                str(run_count),
                *_args[12:],  # scenario kwargs
            ]
        )

        completed_process = subprocess.run(args)  # noqa: S603
        return completed_process.returncode

    @classmethod
    def execute(
        cls,
        scenario: Scenario,
        setup_name: str,
        run_count: int = 10,
        **kwargs: dict[str, Any],
    ) -> BenchmarkSummary:
        """
        Execute a benchmark.
        """
        benchmark_run = BenchmarkRun(scenario, setup_name, scenario_kwargs=kwargs)
        return benchmark_run.execute(run_count)
