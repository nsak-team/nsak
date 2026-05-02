import dataclasses
from collections.abc import Callable
from pydoc import locate
from typing import Any

import click
from click import shell_completion  # type: ignore [attr-defined]

from nsak.core import Scenario, ScenarioManager, config
from nsak.core.scenario.scenario_manager import (
    ScenarioArgumentParsingError,
    ScenarioLifecycleError,
)

from .utils import resource_list_table

scenario_group = click.Group("scenario")


def complete_scenario_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """
    Autocomplete for scenario name in arguments.
    """
    scenarios = ScenarioManager.list()
    scenario_names = {scenario.path.name for scenario in scenarios}
    return [
        scenario_name
        for scenario_name in scenario_names
        if scenario_name.startswith(incomplete)
    ]


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


def create_scenario_command(
    scenario: Scenario, method: Callable[..., Any]
) -> click.Command:
    """
    Create a specific Scenario execute command.
    """

    @click.command(
        name=scenario.id,
        help=scenario.description,
        short_help=scenario.description,
    )
    def cmd(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        try:
            method(scenario, *args, **kwargs)
        except ScenarioArgumentParsingError as e:
            click.echo(e)

    for name, argument in scenario.interface.arguments.items():
        kwargs: dict[str, Any] = {"type": locate(argument.type)}
        if argument.default is dataclasses.MISSING:
            kwargs["prompt"] = name
        else:
            kwargs["default"] = argument.default
        if name == "interface":
            try:
                choices = list(config.device.target_ethernets.keys())
                kwargs["shell_complete"] = lambda ctx, param, incomplete: [
                    shell_completion.CompletionItem(c)
                    for c in choices  # noqa: B023
                    if c.startswith(incomplete)
                ]
            except (AttributeError, TypeError) as e:
                click.echo(e)
                pass

        cmd = click.option(f"--{name}", **kwargs)(cmd)
    return cmd


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
