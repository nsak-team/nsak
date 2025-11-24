from pathlib import Path
import click
import yaml
from cloudinit.net import find_interface_name_from_mac

BASE_PATH = Path(__file__).resolve().parent
SCENARIOS = BASE_PATH / "scenarios"
DRILL = BASE_PATH / "drills"

@click.group()
def cli():
    pass

@cli.group()
def scenario():
    """Scenario related cmds"""
    pass

@scenario.command("list")
def list_scenarios():
    """
    list all scenarios with scenario list
    """
    for path in SCENARIOS.iterdir():
        click.echo(path.name)

@cli.group()
def drill():
    """Drill related cmds"""
    pass
@drill.command("list")
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