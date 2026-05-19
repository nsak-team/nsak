import click

from nsak.cli.utils.create_benchmark_command import create_benchmark_command
from nsak.core import ScenarioManager
from nsak.core.benchmark import BenchmarkManager

benchmark_group = click.Group("benchmark")


@benchmark_group.group("run")
def run() -> None:
    """
    Execute subcommand group.
    """
    pass


@benchmark_group.group("execute")
def execute() -> None:
    """
    Execute subcommand group.
    """
    pass


for _scenario in ScenarioManager.list():
    run.add_command(create_benchmark_command(_scenario, BenchmarkManager.run))
    execute.add_command(create_benchmark_command(_scenario, BenchmarkManager.execute))
