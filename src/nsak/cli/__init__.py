import click

from nsak import core

from .device import device_group
from .drill import drill_group
from .environment import environment_group
from .scenario import scenario_group


@click.group()
def cli() -> None:
    """
    CLI root.
    """
    core.setup()


cli.add_command(scenario_group)
cli.add_command(drill_group)
cli.add_command(device_group)
cli.add_command(environment_group)
