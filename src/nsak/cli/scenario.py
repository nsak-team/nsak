import click

from nsak.core import ScenarioManager

scenario_group = click.Group("scenario")


@scenario_group.command("list")
def list_scenarios() -> None:
    """
    List all scenarios.
    """
    scenarios = ScenarioManager.list()
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
    scenario = ScenarioManager.get(name)
    ScenarioManager.build(scenario)


@scenario_group.command("run")
@click.option(
    "--name",
    prompt="Scenario name",
    help="Provide the scenario name you want to build.",
)
def run_scenario(name: str) -> None:
    """
    Build the scenario image for deployment.
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.run(scenario)
