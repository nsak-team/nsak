import click

from .ai_agent import ai_agent_group
from .benchmark import benchmark_group
from .config import config_group
from .device import device_group
from .drill import drill_group
from .environment import environment_group
from .scenario import kill_all_scenarios, scenario_group


@click.group()
def cli() -> None:
    """
    CLI root.
    """
    # Load the configuration for initialization
    from nsak.core import config  # noqa


cli.add_command(scenario_group)
cli.add_command(drill_group)
cli.add_command(device_group)
cli.add_command(environment_group)
cli.add_command(ai_agent_group)
cli.add_command(config_group)
cli.add_command(benchmark_group)
cli.add_command(kill_all_scenarios, name="killswitch")
