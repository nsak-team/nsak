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
        click.echo(scenario.path.name)


@scenario_group.command("build")
@click.option(
    "--name",
    prompt="Scenario name",
    help="Provide the scenario name you want to build.",
)
def build_scenario(name: str) -> None:
    """
    Build the scenario image for deployment.
    """
    scenario = core.get_scenario(name)
    core.build_scenario(scenario)
