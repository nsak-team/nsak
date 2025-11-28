import click

from src import core

scenario_group = click.Group("scenario")


@scenario_group.command("list")
def list_scenarios() -> None:
    """
    List all scenarios.
    """
    scenarios = core.list_scenarios()
    for scenario in scenarios:
        click.echo(scenario.name)
