from dataclasses import MISSING
from pydoc import locate
from typing import Any, Callable

import click
from click import shell_completion  # type: ignore [attr-defined]

from nsak.core import Scenario, config
from nsak.core.scenario.scenario_manager import ScenarioArgumentParsingError


def create_benchmark_command(
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
    @click.argument("setup_name")
    @click.argument("run_count", default=10, type=int)
    def cmd(setup_name: str, run_count: int, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        try:
            method(scenario, setup_name, run_count, *args, **kwargs)
        except ScenarioArgumentParsingError as e:
            click.echo(e)

    for name, argument in scenario.interface.arguments.items():
        kwargs: dict[str, Any] = {"type": locate(argument.type)}
        if argument.default is MISSING:
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
