from __future__ import annotations

import dataclasses
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface
from pathlib import Path, PosixPath
from typing import Any

import yaml
from logging_loki.handlers import LokiHandler
from yaml import SafeDumper, ScalarNode

from nsak.core.settings import CONFIG_FILE, RUN_PATH

from .configuration import Configuration
from .configuration_serializer import (
    ConfigurationSerializer,
    deserialize_value,
    resolved_hints,
    serialize_value,
    unwrap_optional,
)
from .container_info import ContainerInfo
from .email_configuration import EmailEncryptionType

logger = logging.getLogger(__name__)


def represent_as_string(dumper: SafeDumper, data: Any) -> ScalarNode:  # noqa: ANN401
    """
    Used for serializing objects to strings (e.g., IPInterface or PosixPath).
    """
    if isinstance(data, Enum):
        return dumper.represent_str(str(data.value))

    return dumper.represent_str(str(data))


yaml.add_representer(EmailEncryptionType, represent_as_string, Dumper=SafeDumper)
yaml.add_representer(IPv6Interface, represent_as_string, Dumper=SafeDumper)
yaml.add_representer(IPv4Interface, represent_as_string, Dumper=SafeDumper)
yaml.add_representer(PosixPath, represent_as_string, Dumper=SafeDumper)


@dataclass(frozen=True)
class ConfigFieldInfo:
    """
    Describes a single leaf field in the Configuration hierarchy.
    """

    key: str  # dotted path, e.g. "email.host"
    type: type  # resolved Python type
    settable: bool  # False for runtime-only fields


# Top-level fields that cannot be set by the user.
_NON_SETTABLE: frozenset[str] = frozenset({"container"})

# Top-level fields set via a dedicated mechanism (not raw YAML key-value).
_OPAQUE_KEYS: frozenset[str] = frozenset({"device"})


def _load_raw() -> dict[str, Any]:
    """
    Load the raw YAML config dict from CONFIG_FILE, returning {} if missing.
    """
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f) or {}


def _save_raw(data: dict[str, Any]) -> None:
    """
    Persist a raw dict to CONFIG_FILE as YAML, creating RUN_PATH if needed.
    """
    RUN_PATH.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(data, f)


def _get_nested(data: dict[str, Any], keys: list[str]) -> Any:  # noqa: ANN401
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)  # type: ignore[assignment]
    return data


def _set_nested(data: dict[str, Any], keys: list[str], value: Any) -> None:  # noqa: ANN401
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value


def _walk(cls: type, prefix: str = "") -> list[ConfigFieldInfo]:
    """
    Recursively walk a dataclass and return a flat list of ConfigFieldInfo objects.
    """
    hints = resolved_hints(cls)
    result: list[ConfigFieldInfo] = []

    for field in dataclasses.fields(cls):
        dotted = f"{prefix}{field.name}"
        top_key = dotted.split(".")[0]
        settable = top_key not in _NON_SETTABLE
        tp, _ = unwrap_optional(hints.get(field.name, field.type))

        if top_key in _OPAQUE_KEYS:
            result.append(ConfigFieldInfo(key=dotted, type=tp, settable=settable))
            continue

        if dataclasses.is_dataclass(tp):
            result.extend(_walk(tp, prefix=f"{dotted}."))  # type: ignore [arg-type]
            continue

        result.append(ConfigFieldInfo(key=dotted, type=tp, settable=settable))

    return result


def _resolve_type(key_parts: list[str]) -> type:
    """
    Navigate the Configuration hierarchy and return the resolved type for the field at key_parts.
    """
    current_cls: Any = Configuration
    top_key = key_parts[0]

    for part in key_parts:
        if not dataclasses.is_dataclass(current_cls):
            raise KeyError(part)
        hints = resolved_hints(current_cls)  # type: ignore [arg-type]
        if part not in hints:
            raise KeyError(part)
        current_cls, _ = unwrap_optional(hints[part])
        if top_key in _OPAQUE_KEYS:
            break

    return current_cls  # type: ignore [no-any-return]


def _get_log_file(container: ContainerInfo) -> Path:
    now = datetime.now().astimezone()
    now_formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
    logs_path = RUN_PATH / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    if container.name:
        log_filename = f"{now_formatted}_{container.name}.log"
    else:
        log_filename = f"{now_formatted}.log"
    return logs_path / log_filename


class ConfigurationManager:
    """
    Manager for all runtime configuration operations.
    """

    _loki_handler: LokiHandler | None = None

    @classmethod
    def update_loki_handler(cls, config: Configuration) -> None:
        """
        Update the LokiHandler with the currently running scenario.
        """
        if cls._loki_handler is None:
            return None

        cls._loki_handler.emitter.tags["nsak_run_scenario"] = config.running_scenario
        return None

    @classmethod
    def _setup_logging(cls, config: Configuration) -> None:
        """
        Setup logging.
        """
        log_file = _get_log_file(config.container)
        handlers: list[logging.Handler] = [
            logging.StreamHandler(),
            logging.FileHandler(log_file),
        ]

        if config.loki is not None:
            cls._loki_handler = LokiHandler(
                url=config.loki.url,
                tags={
                    "job": "nsak",
                    "nsak_container_id": config.container.id,
                    "nsak_run_uuid": config.run_uuid,
                    "nsak_run_name": config.container.name,
                    "nsak_run_scenario": config.running_scenario,
                    "nsak_run_datetime": config.datetime,
                },
                auth=(config.loki.username, config.loki.password),
                version="1",
            )
            if cls._loki_handler is None:
                message = "_loki_handler is undefined!"
                raise ValueError(message)
            handlers.append(cls._loki_handler)

        logging.basicConfig(
            level=logging.DEBUG if config.debug else logging.INFO,
            handlers=handlers,
        )
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    @classmethod
    def load(cls) -> Configuration:
        """
        Load the configuration from CONFIG_FILE.

        Falls back to a default Configuration() when the file is absent or cannot be deserialized.
        Also initialises logging.
        """
        try:
            data = _load_raw()
            config = ConfigurationSerializer.deserialize(data)
        except (FileNotFoundError, TypeError):
            config = Configuration()
            cls.save(config)

        cls._setup_logging(config)

        return config

    @classmethod
    def save(cls, config: Configuration) -> None:
        """
        Persist the given Configuration to CONFIG_FILE.
        """
        _save_raw(ConfigurationSerializer.serialize(config))

    @classmethod
    def schema(cls, key: str | None = None) -> list[ConfigFieldInfo]:
        """
        Return ConfigFieldInfo for all (or a subset of) Configuration fields.
        """
        all_fields = _walk(Configuration)
        if key is None:
            return all_fields
        prefix = key + "."
        return [f for f in all_fields if f.key == key or f.key.startswith(prefix)]

    @classmethod
    def is_section(cls, key: str) -> bool:
        """
        Return True if key resolves to a nested dataclass section.
        """
        try:
            tp = _resolve_type(key.split("."))
            return dataclasses.is_dataclass(tp)
        except KeyError:
            return False

    @classmethod
    def get_value(cls, key: str | None = None) -> Any:  # noqa: ANN401
        """
        Return the current config value for the given dotted key path.
        """
        from nsak.core.configuration import config

        serialized = ConfigurationSerializer.serialize(config)
        serialized.pop("container", None)

        if key is None:
            return serialized

        parts = key.split(".")
        try:
            _resolve_type(parts)
        except KeyError as e:
            message = f"Unknown config key: '{key}'."
            raise KeyError(message) from e

        return _get_nested(serialized, parts)

    @classmethod
    def set_value(cls, key: str, raw: str) -> None:
        """
        Set a config field by dotted key path.
        """
        parts = key.split(".")
        top_key = parts[0]

        if top_key in _NON_SETTABLE:
            message = f"'{top_key}' is a runtime-only field and cannot be set."
            raise ValueError(message)

        if top_key == "device" and len(parts) == 1:
            from nsak.core.device.device_manager import DeviceManager

            DeviceManager.load(raw)
            return

        try:
            target_type = _resolve_type(parts)
        except KeyError as e:
            message = f"Unknown config key: '{key}'."
            raise KeyError(message) from e

        if dataclasses.is_dataclass(target_type):
            message = f"'{key}' is a section. Set sub-fields individually, e.g. 'nsak config set {key}.<field> <value>'."
            raise ValueError(message)

        coerced = deserialize_value(target_type, raw)
        stored = serialize_value(target_type, coerced)
        data = _load_raw()
        _set_nested(data, parts, stored)
        _save_raw(data)

    @classmethod
    def set_section(cls, key: str, values: dict[str, Any]) -> None:
        """
        Write a dict of pre-coerced values into the config section at key.
        """
        data = _load_raw()
        _set_nested(data, key.split("."), values)
        _save_raw(data)
