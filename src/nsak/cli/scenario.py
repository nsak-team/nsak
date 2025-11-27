from pathlib import Path

import click

BASE_PATH = Path(__file__).resolve().parents[1]
print(BASE_PATH)
SCENARIOS_DIR = BASE_PATH / "core/scenarios"

scenario_group = click.Group("scenario")


@scenario_group.command("list")
def list_scenarios():
    """List all scenarios."""
    if not SCENARIOS_DIR.exists():
        click.echo("No scenarios directory found.")
        return

    for path in sorted(SCENARIOS_DIR.iterdir()):
        if path.is_dir():
            click.echo(path.name)
