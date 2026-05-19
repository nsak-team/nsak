import click

from nsak.core import ScenarioManager


def complete_scenario_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """
    Autocomplete for scenario name in arguments.
    """
    scenarios = ScenarioManager.list()
    scenario_names = {scenario.path.name for scenario in scenarios}
    return [
        scenario_name
        for scenario_name in scenario_names
        if scenario_name.startswith(incomplete)
    ]
