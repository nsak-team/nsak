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
@click.option(
    "--name",
    prompt="Drill name",
    help="Provide the drill name for the script you want to execute.",
)
def execute_drill(name: str) -> None:
    """
    Execute the drill script.
    """
    scenario = DrillManager.get(name)
    DrillManager.execute(scenario)
