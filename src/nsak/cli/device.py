import json
from typing import Any

import click
from tabulate import tabulate

from nsak.core import DeviceManager

device_group = click.Group("device")


def complete_device_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """
    Autocomplete for device name in arguments.
    """
    devices = DeviceManager.list()
    device_names = {device.path.name for device in devices}
    return [
        device_name
        for device_name in device_names
        if device_name.startswith(incomplete)
    ]


@device_group.command("list")
def list_devices() -> None:
    """
    List all devices.
    """
    devices = DeviceManager.list()
    columns: list[str] = ["id", "name", "path"]
    data: list[list[Any]] = []

    for device in devices:
        row = []
        for column in columns:
            row.append(getattr(device, column))
        data.append(row)

    table = tabulate(
        data, headers=[column.upper() for column in columns], tablefmt="plain"
    )
    click.echo(table)


@device_group.command("show")
@click.argument("name", shell_complete=complete_device_name)  # type: ignore [call-arg]
def show_device(name: str) -> None:
    """
    Show the device details.
    """
    device = DeviceManager.get(name)
    if device.configuration is not None:
        click.echo(json.dumps(device.configuration.raw, indent=2))


@device_group.command("load")
@click.argument("name", shell_complete=complete_device_name)  # type: ignore [call-arg]
def load_device(name: str) -> None:
    """
    Load a device config.
    """
    device = DeviceManager.load(name)
    click.echo(f"Successfully loaded device config: {name}")
    if device.configuration is not None:
        click.echo(json.dumps(device.configuration.raw, indent=2))


@device_group.command("loaded")
def loaded_device() -> None:
    """
    Get the active device.
    """
    device = DeviceManager.get_loaded()
    if device is None:
        click.echo("No device loaded.")
    else:
        click.echo(f"Loaded device: {device.name} (id = {device.id})")
        if device.configuration is not None:
            click.echo(json.dumps(device.configuration.raw, indent=2))


@device_group.command("unload")
def unload_device() -> None:
    """
    Get the active device.
    """
    DeviceManager.unload()
    click.echo("Device unloaded.")
