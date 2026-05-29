"""Tests for the public API."""

from ctypes import (
    Structure,
    Union,
    c_char_p,
    c_double,
    c_int,
    c_int32,
    c_uint64,
    sizeof,
)
from typing import Annotated

import pytest

from ctypes_plus import Field, asdict, fields, structure, union
from ctypes_plus.types import CharP, Double, Int32, UInt64

type MyInt = Annotated[int, c_int]
type MyIntAlias = MyInt  # Alias of an alias


@structure
class LogEvent:
    event_id: Int32
    timestamp: UInt64
    message: CharP


@union
class Number:
    as_int: Int32
    as_double: Double


def test_structure_produces_structure_subclass() -> None:
    assert issubclass(LogEvent, Structure)
    assert LogEvent._fields_ == [
        ("event_id", c_int32),
        ("timestamp", c_uint64),
        ("message", c_char_p),
    ]
    # A real ctypes type usable with `sizeof`.
    assert sizeof(LogEvent) > 0


def test_native_construction_needs_no_ignore() -> None:
    by_kwargs = LogEvent(event_id=1, timestamp=99, message=b"foo")
    by_pos = LogEvent(1, 99, b"foo")
    assert by_kwargs.event_id == by_pos.event_id == 1
    assert by_kwargs.timestamp == 99
    assert by_kwargs.message == b"foo"


def test_union_overlaps_storage() -> None:
    assert issubclass(Number, Union)
    assert sizeof(Number) == sizeof(c_double)
    n = Number(as_int=7)
    assert n.as_int == 7


def test_asdict_returns_native_values() -> None:
    event = LogEvent(event_id=2, timestamp=1234, message=b"foo")
    assert asdict(event) == {
        "event_id": 2,
        "timestamp": 1234,
        "message": b"foo",
    }


def test_fields_reports_ctypes_types() -> None:
    assert fields(LogEvent) == (
        Field("event_id", c_int32),
        Field("timestamp", c_uint64),
        Field("message", c_char_p),
    )
    assert fields(Number) == (
        Field("as_int", c_int32),
        Field("as_double", c_double),
    )


def test_repr() -> None:
    event = LogEvent(event_id=2, timestamp=1234, message=b"foo")
    assert (
        repr(event) == "LogEvent(event_id=2, timestamp=1234, message=b'foo')"
    )


def test_repr_not_overridden_when_user_defined() -> None:
    @structure
    class Custom:
        x: Int32

        def __repr__(self) -> str:
            return "custom!"

    assert repr(Custom(1)) == "custom!"


def test_plain_ctypes_annotations_still_supported() -> None:
    # Backward compat: raw ctypes types work (native values need an ignore).
    @structure
    class Raw:
        a: c_int

    assert fields(Raw) == (Field("a", c_int),)
    assert asdict(Raw(5)) == {"a": 5}  # type: ignore[bad-argument-type]


def test_user_type_aliases_are_unwrapped() -> None:
    @structure
    class S:
        a: MyInt
        b: MyIntAlias

    assert fields(S) == (Field("a", c_int), Field("b", c_int))
    # Native values, no ignore: the aliases resolve to `int`.
    assert asdict(S(1, 2)) == {"a": 1, "b": 2}


def test_works_on_handwritten_ctypes_type() -> None:
    class Point(Structure):
        _fields_ = (
            ("x", c_int),
            ("y", c_int),
        )

    assert fields(Point) == (Field("x", c_int), Field("y", c_int))
    assert asdict(Point(3, 4)) == {"x": 3, "y": 4}


def test_type_errors_on_plain_objects() -> None:
    with pytest.raises(TypeError):
        asdict(42)
    with pytest.raises(TypeError):
        fields(42)


def test_handwritten_ctypes_inherited_fields_are_reported() -> None:
    class Point(Structure):
        _fields_ = (
            ("x", c_int),
            ("y", c_int),
        )

    class Point3D(Point):
        _fields_ = (("z", c_int),)

    point = Point3D(1, 2, 3)

    assert fields(Point3D) == (
        Field("x", c_int),
        Field("y", c_int),
        Field("z", c_int),
    )
    assert asdict(point) == {"x": 1, "y": 2, "z": 3}
