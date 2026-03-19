import click

from nsak.core import ScenarioManager

scenario_group = click.Group("scenario")


def _parse_arguments(raw_args: list[str]) -> dict[str, str]:
    args: dict[str, str | None] = {}
    key = None

    for arg in raw_args:
        if arg.startswith("--"):
            key = arg.lstrip("-")
            args[key] = None
        else:
            if key is None:
                message = f"Unexpected value: {arg}"
                raise click.ClickException(message)
            args[key] = arg
            key = None

    return {key: value for key, value in args.items() if value is not None}


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


@scenario_group.command(
    "run",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
)
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
@click.pass_context
def run_scenario(
    ctx: click.Context,
    name: str,
) -> None:
    """
    Run the scenario container.
    """
    arguments = _parse_arguments(ctx.args)
    scenario = ScenarioManager.get(name)
    ScenarioManager.run(scenario, **arguments)


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
# todo design a way to pass the arguments to the run method of the container
@click.argument("name", shell_complete=complete_scenario_name)  # type: ignore [call-arg]
@click.pass_context
def execute_scenario(ctx: click.Context, name: str) -> None:
    """
    Execute the scenario script.

    :param name: The name of the scenario for which you want to execute the script.
    :param ctx: The click context.
    :return:
    """
    arguments = _parse_arguments(ctx.args)
    scenario = ScenarioManager.get(name)
    ScenarioManager.execute(scenario, **arguments)
