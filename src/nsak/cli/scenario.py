import click

from nsak.core import ScenarioManager
from nsak.core.scenario.scenario_manager import (
    ScenarioLifecycleError,
)

from .utils import complete_scenario_name, resource_list_table
from .utils.create_scenario_command import create_scenario_command

scenario_group = click.Group("scenario")


@scenario_group.command("list")
def list_scenarios() -> None:
    """
    List all scenarios.
    """
    scenarios = ScenarioManager.list()
    table = resource_list_table(scenarios)
    click.echo(table)


@scenario_group.command("build")
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
def build_scenario(name: str) -> None:
    """
    Build the scenario image for deployment.

    :param name: The name of the scenario you want to build.
    :return:
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.build(scenario)


@scenario_group.group("run")
def run() -> None:
    """
    Execute subcommand group.
    """
    pass


@scenario_group.group("execute")
def execute() -> None:
    """
    Execute subcommand group.
    """
    pass


@scenario_group.command("stop")
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
def stop_scenario(name: str) -> None:
    """
    Stop a running scenario container.

    :param name: The name of the scenario you want to stop.
    :return:
    """
    scenario = ScenarioManager.get(name)
    try:
        ScenarioManager.stop(scenario)
        click.echo(f"Scenario '{name}' stopped.")
    except ScenarioLifecycleError as e:
        click.echo(e, err=True)


@scenario_group.command("kill")
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
def kill_scenario(name: str) -> None:
    """
    Forcefully kill a running scenario container (SIGKILL, last resort).

    :param name: The name of the scenario you want to kill.
    :return:
    """
    scenario = ScenarioManager.get(name)
    try:
        ScenarioManager.kill(scenario)
        click.echo(f"Scenario '{name}' killed.")
    except ScenarioLifecycleError as e:
        click.echo(e, err=True)


@scenario_group.command("killswitch")
def kill_all_scenarios() -> None:
    """
    Forcefully kill all running scenario containers (SIGKILL, last resort).
    """
    try:
        ScenarioManager.kill_all()
        click.echo("All scenarios killed.")
    except ScenarioLifecycleError as e:
        click.echo(e, err=True)


for _scenario in ScenarioManager.list():
    run.add_command(create_scenario_command(_scenario, ScenarioManager.run))
    execute.add_command(create_scenario_command(_scenario, ScenarioManager.execute))
