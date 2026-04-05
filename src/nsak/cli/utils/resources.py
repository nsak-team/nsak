from pathlib import Path
from typing import Any, Sequence

from tabulate import tabulate

from nsak.core.resource import Resource
from nsak.core.settings import BASE_PATH


def resource_list_table(resources: Sequence[Resource]) -> str:
    """
    Helper function to render a list of resources as a text based table.
    """
    columns: list[str] = ["id", "name", "path"]
    data: list[list[Any]] = []

    for resource in resources:
        row = []
        for column in columns:
            if column == "path":
                path: Path = getattr(resource, column)
                row.append(path.relative_to(BASE_PATH))
            else:
                row.append(getattr(resource, column))
        data.append(row)

    table = tabulate(
        data, headers=[column.upper() for column in columns], tablefmt="plain"
    )

    return table
