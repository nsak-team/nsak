import click

from src.nsak.cli.drill import drill_group
from src.nsak.cli.scenario import scenario_group


@click.group()
def cli() -> None:
    """
    CLI root.
    """
    pass


cli.add_command(scenario_group)
cli.add_command(drill_group)

if __name__ == "__main__":
    cli()
