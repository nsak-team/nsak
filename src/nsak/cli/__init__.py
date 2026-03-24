import click

from .device import device_group
from .drill import drill_group
from .environment import environment_group
from .scenario import scenario_group


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
