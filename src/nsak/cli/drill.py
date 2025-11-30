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
