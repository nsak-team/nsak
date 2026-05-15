from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any

import click

from nsak.core.configuration.configuration_manager import (
    ConfigFieldInfo,
    ConfigurationManager,
)
from nsak.core.configuration.configuration_serializer import (
    DeserializationError,
    deserialize_value,
)

config_group = click.Group("config")


def _display(key: str, value: Any, indent: int = 0) -> None:  # noqa: ANN401
    """
    Recursively pretty-print a config key/value pair.
    """
    prefix = "  " * indent

    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        value = dataclasses.asdict(value)

    if isinstance(value, dict):
        click.echo(f"{prefix}{key}:")
        for k, v in value.items():
            _display(k, v, indent + 1)
    else:
        click.echo(f"{prefix}{key}: {value}")


def _prompt_field(info: ConfigFieldInfo, current: dict[str, Any], prefix: str) -> Any:  # noqa: ANN401
    """
    Prompt the user for a single field and return the coerced result.

    Applies type-appropriate widgets:
      - Enum   → Choice (name strings, coerced to .value via deserialize_value)
      - bool   → confirm
      - int    → validated integer prompt
      - str    → plain prompt
    """
    rel_key = info.key[len(prefix) :]
    current_val = current.get(rel_key, "")
    label = rel_key

    if isinstance(info.type, type) and issubclass(info.type, Enum):
        choices = [e.name for e in info.type]
        # Stored as int in YAML; display as name
        if isinstance(current_val, int):
            try:
                current_val = info.type(current_val).name
            except ValueError:
                current_val = choices[0]
        entered = click.prompt(
            label,
            default=current_val or choices[0],
            type=click.Choice(choices),
        )
        return deserialize_value(info.type, entered)

    if info.type is bool:
        return click.confirm(label, default=bool(current_val))

    if info.type is int:
        return click.prompt(label, default=current_val or 0, type=int)  # type: ignore [arg-type]

    return click.prompt(label, default=current_val or "")


def _get_leaf_fields(key: str) -> list[ConfigFieldInfo]:
    """
    Return a list of leaf fields.
    """
    prefix = key + "."
    leaf_fields = []

    for field in ConfigurationManager.schema(key):
        if (
            field.settable
            and field.key.startswith(prefix)
            and "." not in field.key[len(prefix) :]
        ):  # direct children only
            leaf_fields.append(field)

    return leaf_fields


def _interactive_section(key: str) -> None:
    """
    Interactively prompt for every settable direct-child leaf field of a config section.
    """
    prefix = key + "."
    leaf_fields = _get_leaf_fields(key)

    if not leaf_fields:
        click.echo(f"No configurable sub-fields found under '{key}'.", err=True)
        return

    try:
        current = ConfigurationManager.get_value(key) or {}
    except KeyError:
        current = {}

    if dataclasses.is_dataclass(current):
        current = dataclasses.asdict(current)  # type: ignore

    current_raw = current if isinstance(current, dict) else {}

    updates: dict[str, Any] = {}
    for field_info in leaf_fields:
        rel_key = field_info.key[len(prefix) :]
        updates[rel_key] = _prompt_field(field_info, current_raw, prefix)

    ConfigurationManager.set_section(key, updates)
    click.echo(f"'{key}' updated.")


@config_group.command("get")
@click.argument("key", required=False)
def get_config(key: str | None) -> None:
    """
    Get one or all runtime config values.

    Examples
    --------
      nsak config get
      nsak config get debug
      nsak config get email
      nsak config get email.encryption
    """
    try:
        result = ConfigurationManager.get_value(key)
    except KeyError as e:
        click.echo(str(e), err=True)
        return

    if key is None:
        for k, v in result.items():
            _display(k, v)
    elif isinstance(result, dict):
        _display(key, result)
    else:
        _display(key.split(".")[-1], result)


@config_group.command("set")
@click.argument("key")
@click.argument("value", required=False)
def set_config(key: str, value: str | None) -> None:
    """
    Set a runtime config value.

    Omit VALUE for a section key (e.g. 'email') to start an interactive
    prompt for all its fields.

    Examples
    --------
      nsak config set debug 1
      nsak config set device <device-id>
      nsak config set email
      nsak config set email.host smtp.example.com
      nsak config set email.encryption TLS
      nsak config set email.port 587
    """
    if value is None:
        if ConfigurationManager.is_section(key):
            _interactive_section(key)
        else:
            message = f"Usage: nsak config set {key} <value>"
            raise click.UsageError(message)
        return

    try:
        ConfigurationManager.set_value(key, value)
        click.echo(f"'{key}' set.")
    except (KeyError, ValueError, DeserializationError) as e:
        click.echo(str(e), err=True)
