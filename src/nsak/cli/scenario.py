import click

from nsak.core import ScenarioManager

scenario_group = click.Group("scenario")


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


@scenario_group.command("list")
def list_scenarios() -> None:
    """
    List all scenarios.
    """
    scenarios = ScenarioManager.list()
    for scenario in scenarios:
        click.echo(scenario.path.name)


@scenario_group.command("build")
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
def build_scenario(name: str) -> None:
    """
    Build the scenario image for deployment.

    :param name: The name of the scenario you want to build.
    :return:
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.build(scenario)


@scenario_group.command("run")
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
def run_scenario(name: str) -> None:
    """
    Run the scenario container.

    :param name: The name of the scenario for which you want to run the container.
    :return:
    """
    scenario = ScenarioManager.get(name)
    ScenarioManager.run(scenario)


def _parse_args(raw_args: list[str]) -> dict[str, str]:
    args: dict[str, str] = {}

    for item in raw_args:
        if "=" not in item:
            msg = f"Invalid argument '{item}', expected key=value"
            raise click.UsageError(msg)
        key, value = item.split("=", 1)
        args[key] = value

    return args


@scenario_group.command(
    "execute",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
)
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
@click.pass_context
def execute_scenario(ctx: click.Context, name: str) -> None:
    """
    Execute the scenario script.

    :param name: The name of the scenario for which you want to execute the script.
    :param ctx: The click context.
    :return:
    """
    scenario = ScenarioManager.get(name)

    # everything after `--`
    raw_args = ctx.args

    args = _parse_args(raw_args)

    ScenarioManager.execute(scenario, args=args)
