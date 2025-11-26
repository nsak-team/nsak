import click

from src.nsak.cli.scenario_list import scenario_group


@click.group()
def cli():
    """NSAK CLI root."""
    pass


cli.add_command(scenario_group)

if __name__ == "__main__":
    cli()
