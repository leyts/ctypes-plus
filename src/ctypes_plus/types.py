"""Native-typed field aliases."""

from ctypes import (
    c_bool,
    c_char_p,
    c_double,
    c_float,
    c_int,
    c_int8,
    c_int16,
    c_int32,
    c_int64,
    c_uint,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_wchar_p,
)
from typing import Annotated

type Int = Annotated[int, c_int]
type Int8 = Annotated[int, c_int8]
type Int16 = Annotated[int, c_int16]
type Int32 = Annotated[int, c_int32]
type Int64 = Annotated[int, c_int64]
type UInt = Annotated[int, c_uint]
type UInt8 = Annotated[int, c_uint8]
type UInt16 = Annotated[int, c_uint16]
type UInt32 = Annotated[int, c_uint32]
type UInt64 = Annotated[int, c_uint64]
type Float = Annotated[float, c_float]
type Double = Annotated[float, c_double]
type Bool = Annotated[bool, c_bool]
type CharP = Annotated[bytes, c_char_p]
type WCharP = Annotated[str, c_wchar_p]

__all__ = [
    "Bool",
    "CharP",
    "Double",
    "Float",
    "Int",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "UInt",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "WCharP",
]
