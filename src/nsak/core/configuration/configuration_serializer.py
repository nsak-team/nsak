from __future__ import annotations

import dataclasses
import types as builtin_types
import typing
from dataclasses import MISSING, fields
from enum import Enum
from typing import Any, Callable, get_type_hints

from nsak.core.configuration.configuration import Configuration


class DeserializationError(Exception):
    """
    Thrown for errors during the deserialization process.
    """

    pass


def unwrap_optional(tp: Any) -> tuple[Any, bool]:  # noqa: ANN401
    """
    Return (inner_type, is_optional).
    """
    origin = typing.get_origin(tp)
    if origin is typing.Union:
        args = typing.get_args(tp)
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0], type(None) in args

    if isinstance(tp, builtin_types.UnionType):
        non_none = [a for a in tp.__args__ if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0], type(None) in tp.__args__

    return tp, False


def resolved_hints(cls: type) -> dict[str, Any]:
    """
    Return resolved type hints for cls.

    Uses get_type_hints() rather than field.type directly,
    so that 'from __future__ import annotations' string annotations are resolved.
    """
    return get_type_hints(cls)


def bool_deserializer(_type: type, value: Any) -> bool:  # noqa: ANN401
    """
    Deserialize a boolean from various representations.
    """
    type_map: dict[Any, bool] = {
        False: False,
        # 0: False, -> hashes to same as False
        "0": False,
        "no": False,
        "false": False,
        True: True,
        # 1: True, -> hashes to same as True
        "1": True,
        "yes": True,
        "true": True,
    }
    normalized = value.lower() if isinstance(value, str) else value
    result = type_map.get(normalized)
    if result is None:
        valid = ", ".join(str(k) for k in type_map)
        message = f"Invalid boolean value '{value}'. Valid options: {valid}."
        raise DeserializationError(message)
    return result


def enum_deserializer(_type: type[Enum], value: Any) -> Enum:  # noqa: ANN401
    """
    Deserialize an Enum from its primitive value (int stored in YAML) or its name (string from CLI / human input).
    """
    if isinstance(value, _type):
        return value
    # Prefer value-based lookup (int from YAML)
    try:
        return _type(value)
    except ValueError:
        pass
    # Fall back to name-based lookup (string from CLI)
    if isinstance(value, str):
        try:
            return _type[value.upper()]
        except KeyError:
            pass
        # Handle string-encoded integers (e.g. "0", "1") written by old representer
        try:
            return _type(int(value))
        except (ValueError, KeyError):
            pass
    names = ", ".join(e.name for e in _type)
    values = ", ".join(str(e.value) for e in _type)
    message = f"Invalid value '{value}' for {_type.__name__}. Valid names: {names}. Valid values: {values}."
    raise DeserializationError(message)


def device_deserializer(_type: type, value: Any) -> Any:  # noqa: ANN401
    """
    Deserialize a Device by loading it from DeviceManager.

    Accepts a device id/name string or a serialized device dict (in which case the 'id' key is used).
    """
    from nsak.core.device.device_manager import DeviceManager

    if value is None:
        return DeviceManager.get_default()
    if dataclasses.is_dataclass(value):
        return value  # already a Device instance
    if isinstance(value, dict):
        value = value.get("id") or value.get("name")
    return DeviceManager.get(str(value))


def container_info_deserializer(_type: type, _value: Any) -> Any:  # noqa: ANN401
    """
    ContainerInfo must always be derived from the live runtime environment.
    """
    from nsak.core.configuration.container_info import ContainerInfo

    return ContainerInfo.load()


def dataclass_deserializer(_type: type, data: dict[str, Any]) -> dict[str, Any]:
    """
    Generically deserialize a dict into a kwargs dict for constructing _type.
    """
    if not isinstance(data, dict):
        message = f"Expected dict for {_type.__name__}, got {type(data).__name__}."
        raise DeserializationError(message)

    hints = resolved_hints(_type)
    result: dict[str, Any] = {}

    for field in fields(_type):
        raw_type = hints.get(field.name, field.type)
        inner_type, is_opt = unwrap_optional(raw_type)
        is_required = (
            field.default is MISSING and field.default_factory is MISSING and field.init
        )

        if field.name not in data:
            if is_required and not is_opt:
                message = f"Required field '{field.name}' missing for {_type.__name__}."
                raise DeserializationError(message)
            # Absent optional / defaulted fields: let the dataclass use its default
            continue

        value = data[field.name]

        if value is None:
            if not is_opt:
                message = f"Field '{field.name}' of {_type.__name__} cannot be None."
                raise DeserializationError(message)
            result[field.name] = None
            continue

        result[field.name] = deserialize_value(inner_type, value)
    return result


_DESERIALIZER_MAP: dict[type, Callable[[type, Any], Any]] | None = None


def _get_deserializer_map() -> dict[type, Callable[[type, Any], Any]]:
    """
    Get the deserializer map lazily to avoid circular imports.
    """
    global _DESERIALIZER_MAP
    if _DESERIALIZER_MAP is None:
        from nsak.core.configuration.container_info import ContainerInfo
        from nsak.core.device.device import Device

        _DESERIALIZER_MAP = {
            bool: bool_deserializer,
            Device: device_deserializer,
            ContainerInfo: container_info_deserializer,
        }
    return _DESERIALIZER_MAP


def deserialize_value(_type: type, value: Any) -> Any:  # noqa: ANN401
    """
    Deserialize value to _type.

    Resolution order:
      1. Exact type match in the deserializer map
      2. Enum subclass  ->  enum_deserializer
      3. Dataclass      ->  dataclass_deserializer (generic, recursive)
      4. Direct coercion _type(value) for primitives (int, str, …)
    """
    deserializer = _get_deserializer_map().get(_type)
    if deserializer is not None:
        return deserializer(_type, value)

    if isinstance(_type, type) and issubclass(_type, Enum):
        return enum_deserializer(_type, value)

    if dataclasses.is_dataclass(_type):
        kwargs = dataclass_deserializer(_type, value)
        return _type(**kwargs)

    if isinstance(value, _type):
        return value

    try:
        return _type(value)  # type: ignore [call-arg]
    except (TypeError, ValueError) as exc:
        message = (
            f"Cannot coerce '{value}' ({type(value).__name__}) to {_type.__name__}."
        )
        raise DeserializationError(message) from exc


_SERIALIZER_MAP: dict[type, Callable[[Any], Any]] | None = None


def _get_serializer_map() -> dict[type, Callable[[Any], Any]]:
    """
    Get the serializer lazily to avoid circular imports.
    """
    global _SERIALIZER_MAP
    if _SERIALIZER_MAP is None:
        from nsak.core.configuration.container_info import ContainerInfo
        from nsak.core.device.device import Device

        _SERIALIZER_MAP = {
            # Device is persisted by id only; full object is reloaded on deserialize
            Device: lambda d: d.id if d is not None else None,
            # ContainerInfo is runtime-only and never persisted
            ContainerInfo: lambda _: None,
        }
    if _SERIALIZER_MAP is None:
        message = "_SERIALIZER_MAP is undefined!"
        raise ValueError(message)
    return _SERIALIZER_MAP


def serialize_value(_type: type, value: Any) -> Any:  # noqa: ANN401
    """
    Serialize value of _type to a YAML-compatible primitive / dict.

    Resolution order:
      1. None passthrough
      2. Exact type match in the serializer map
      3. Enum subclass  ->  .value  (primitive)
      4. Dataclass      ->  recursive dict
      5. Primitive passthrough
    """
    if value is None:
        return None

    serializer = _get_serializer_map().get(_type)
    if serializer is not None:
        return serializer(value)

    if isinstance(_type, type) and issubclass(_type, Enum):
        return value.value

    if dataclasses.is_dataclass(_type) and dataclasses.is_dataclass(value):
        return _serialize_dataclass(value)

    return value


def _serialize_dataclass(obj: Any) -> dict[str, Any]:  # noqa: ANN401
    """
    Serialize a dataclass instance to a YAML-compatible dict, applying the serializer map rules recursively.

    Entries whose serialized value is None are omitted.
    """
    hints = resolved_hints(type(obj))
    result: dict[str, Any] = {}

    for field in fields(obj):
        raw_type = hints.get(field.name, field.type)
        inner_type, _ = unwrap_optional(raw_type)
        value = getattr(obj, field.name)
        serialized = serialize_value(inner_type, value)
        if serialized is not None:
            result[field.name] = serialized

    return result


class ConfigurationSerializer:
    """
    Serializer and Deserializer for Configuration objects.

    serialize:   Configuration -> YAML-compatible dict
    deserialize: YAML-compatible dict -> Configuration
    """

    @classmethod
    def serialize(cls, configuration: Configuration) -> dict[str, Any]:
        """
        Serialize a Configuration to a YAML-compatible dict.

        Special rules applied automatically via the serializer map:
        - Device      -> persisted as its id (string)
        - ContainerInfo -> omitted (runtime-only)
        - Enum        -> persisted as primitive value
        """
        return _serialize_dataclass(configuration)

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Configuration:
        """
        Deserialize a YAML-loaded dict into a Configuration object.

        Special rules applied automatically via the deserializer map:
        - bool        -> accepts 0/1, "true"/"false", "yes"/"no"
        - Device      -> loaded from DeviceManager by id
        - ContainerInfo -> always loaded fresh from the runtime environment
        - EmailConfiguration -> loaded via EmailConfiguration.create()
        - Enum        -> resolved by value (int) or name (string)
        """
        kwargs = dataclass_deserializer(Configuration, data)
        return Configuration(**kwargs)
