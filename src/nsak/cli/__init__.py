import click

from nsak import core

from .drill import drill_group
from .scenario import scenario_group


@click.group()
def cli() -> None:
    """
    CLI root.
    """
    core.setup()


cli.add_command(scenario_group)
cli.add_command(drill_group)
