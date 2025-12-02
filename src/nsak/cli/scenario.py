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
@click.argument("name")
def build_scenario(name: str) -> None:
    """
    Build the scenario image for deployment.

    :param name: The name of the scenario you want to build.
    :return:
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.build(scenario)


@scenario_group.command("run")
@click.argument("name")
def run_scenario(name: str) -> None:
    """
    Run the scenario container.

    :param name: The name of the scenario for which you want to run the container.
    :return:
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.run(scenario)


@scenario_group.command("execute")
@click.argument("name")
def execute_scenario(name: str) -> None:
    """
    Execute the scenario script.

    :param name: The name of the scenario for which you want to execute the script.
    :return:
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.execute(scenario)
