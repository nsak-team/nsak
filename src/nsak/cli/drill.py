import click

from nsak.core import DrillManager

drill_group = click.Group("drill")


@drill_group.command("list")
def list_drills() -> None:
    """
    List all drills.
    """
    drills = DrillManager.list()
    for drill in drills:
        click.echo(drill.name)


@drill_group.command("execute")
@click.argument("name")
def execute_drill(name: str) -> None:
    """
    Execute the drill script.

    :param name: The name of the drill for which you want to execute the script.
    :return:
    """
    scenario = DrillManager.get(name)
    DrillManager.execute(scenario)
