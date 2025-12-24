import click

from nsak.core import EnvironmentManager

environment_group = click.Group("environment")


def complete_environment_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """
    Autocomplete for environment name in arguments.
    """
    environments = EnvironmentManager.list()
    environment_names = {environment.path.name for environment in environments}
    return [
        environment_name
        for environment_name in environment_names
        if environment_name.startswith(incomplete)
    ]


def complete_environment_scenario_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """
    Autocomplete for scenario name in arguments.
    """
    environment_name = ctx.params["name"]
    scenarios = EnvironmentManager.list_scenarios(
        EnvironmentManager.get(environment_name)
    )
    scenario_names = {scenario.path.name for scenario in scenarios}
    return [
        scenario_name
        for scenario_name in scenario_names
        if scenario_name.startswith(incomplete)
    ]


@environment_group.command("list")
def list_environments() -> None:
    """
    List all environments.
    """
    environments = EnvironmentManager.list()
    for environment in environments:
        click.echo(environment.name)


@environment_group.command("list_scenarios")
@click.argument("name", shell_complete=complete_environment_name)  # type: ignore [call-arg]
def list_environment_scenarios(name: str) -> None:
    """
    List all scenarios of an environment.
    """
    scenarios = EnvironmentManager.list_scenarios(name)
    for scenario in scenarios:
        click.echo(scenario.path.name)


@environment_group.command("simulate")
@click.argument("name", shell_complete=complete_environment_name)  # type: ignore [call-arg]
@click.argument("scenario_name", shell_complete=complete_environment_scenario_name)  # type: ignore [call-arg]
def simulate_environment(name: str, scenario_name: str) -> None:
    """
    Execute the environment script.

    :param scenario_name: The specific scenario which should be simulated in the environment.
    :param name: The name of the environment you want to simulate.
    :return:
    """
    EnvironmentManager.simulate(name, scenario_name)
