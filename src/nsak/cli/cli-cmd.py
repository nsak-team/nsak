from pathlib import Path
import click

BASE_PATH = Path(__file__).resolve().parent
SCENARIOS = BASE_PATH / "scenarios"
DRILL = BASE_PATH / "drills"


@click.group()
def cli():
    pass


@cli.group()
def drills():
    """Drill related cmds"""
    pass


@drills.command("list")
def list_drills():
    """
    list all drill drills list
    Basic implementation which checks the folder structure right now
    todo: improve to take the drills from yaml
    """
    for path in DRILL.iterdir():
        click.echo(path.name)


if __name__ == '__main__':
    cli()
