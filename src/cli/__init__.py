import click

from src import core
from src.cli.drill import drill_group
from src.cli.scenario import scenario_group


@click.group()
def cli() -> None:
    """
    CLI root.
    """
    core.setup()


cli.add_command(scenario_group)
cli.add_command(drill_group)

if __name__ == "__main__":
    cli()
