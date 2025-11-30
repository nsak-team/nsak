import click

from nsak import core

drill_group = click.Group("drill")


@drill_group.command("list")
def list_drills() -> None:
    """
    List all drills.
    """
    drills = core.list_drills()
    for drill in drills:
        click.echo(drill.name)
