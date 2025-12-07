import click

from nsak.core import DrillManager

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
    for drill in drills:
        click.echo(drill.name)


@drill_group.command("execute")
@click.argument("name", shell_complete=complete_drill_name)  # type: ignore [call-arg]
def execute_drill(name: str) -> None:
    """
    Execute the drill script.

    :param name: The name of the drill for which you want to execute the script.
    :return:
    """
    scenario = DrillManager.get(name)
    DrillManager.execute(scenario)
