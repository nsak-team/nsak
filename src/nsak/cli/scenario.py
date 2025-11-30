import click

scenario_group = click.Group("scenario")


@scenario_group.command("list")
def list_scenarios() -> None:
    """
    List all scenarios.
    """
    pass
