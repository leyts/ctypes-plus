"""Dataclass-style decorators that build ctypes composite types."""

from ctypes import Structure, Union
from typing import cast, dataclass_transform

from ctypes_plus._build import build


@dataclass_transform()
def structure[T](cls: type[T]) -> type[T]:
    """Turn an annotated class into a ``ctypes.Structure`` subclass.

    Each annotation becomes a ``_fields_`` entry::

        @structure
        class LogEvent:
            event_id: c_int
            message: c_char_p
    """
    return cast("type[T]", build(cls, Structure))


@dataclass_transform()
def union[T](cls: type[T]) -> type[T]:
    """Turn an annotated class into a ``ctypes.Union`` subclass."""
    return cast("type[T]", build(cls, Union))
