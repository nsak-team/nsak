from typing import Any

import click
from click import shell_completion  # type: ignore [attr-defined]

from nsak.core import Drill, DrillManager, config
from nsak.core.drill.drill_manager import DrillArgumentParsingError

from .utils import resource_list_table

drill_group = click.Group("drill")


def complete_drill_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """
    Autocomplete for drill name in arguments.
    """
    drills = DrillManager.list()
    drill_names = {drill.path.name for drill in drills}
    return [
        drill_name for drill_name in drill_names if drill_name.startswith(incomplete)
    ]


@drill_group.command("list")
def list_drills() -> None:
    """
    List all drills.
    """
    drills = DrillManager.list()
    table = resource_list_table(drills)
    click.echo(table)


@drill_group.group("execute")
def execute() -> None:
    """
    Execute subcommand group.
    """
    pass


def create_drill_command(drill: Drill) -> click.Command:
    """
    Create a specific Drill command.

    :param drill:
    :return:
    """

    @click.command(
        name=drill.id,
        help=drill.description,
        short_help=drill.description,
    )
    def cmd(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """
        Generated drill specific command.

        :param args:
        :param kwargs:
        :return:
        """
        try:
            DrillManager.execute(drill, *args, **kwargs)
        except DrillArgumentParsingError as e:
            click.echo(e)

    for name, argument in drill.interface.arguments.items():
        kwargs = dict(
            default=argument.default,
            prompt=name,
        )
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


for _drill in DrillManager.list():
    execute.add_command(create_drill_command(_drill))


@drill_group.command("clear")
@click.argument("name", shell_complete=complete_drill_name)  # type: ignore [call-arg]
def clean_up(name: str) -> None:
    """
    Clear the drill cmd.

    :param name:
    :return:
    """
    drill = DrillManager.get(name)
    DrillManager.clean_up(drill)
