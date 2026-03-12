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
