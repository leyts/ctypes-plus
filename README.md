# ctypes-plus

![PyPI - Version](https://img.shields.io/pypi/v/ctypes-plus)
![PyPI - License](https://img.shields.io/pypi/l/ctypes-plus)

A dataclass-like interface for ctypes data types.

> [!WARNING]
> This package is under development. The API is subject to breaking changes.

## Installation

```shell
pip install ctypes-plus
```

## Usage

Decorate an annotated class with `@structure` or `@union`. Each annotation
becomes a `_fields_` entry, and the result is a `ctypes.Structure` /
`ctypes.Union` subclass usable anywhere ctypes is expected.

```python
from ctypes_plus import structure, union
from ctypes_plus.types import CharP, Double, Int32, UInt64

@structure
class LogEvent:
    event_id: Int32
    timestamp: UInt64
    message: CharP

@union
class Number:
    as_int: Int32
    as_double: Double

event = LogEvent(event_id=2, timestamp=1234, message=b"foo")
print(event)  # LogEvent(event_id=2, timestamp=1234, message=b'foo')
```

### Typed fields

`ctypes_plus.types` provides `Annotated` types that map a native Python type
to its ctypes type, so construction and attribute access type-check cleanly.

Plain ctypes types (`a: c_int`), your own `Annotated[..., ctype]` aliases and
`type` aliases of either are all accepted too.

### Introspection

```python
>>> from ctypes_plus import asdict, fields
>>> fields(LogEvent)
(Field(name='event_id', type=<class 'ctypes.c_int'>), ...)
>>> asdict(event)
{'event_id': 2, 'timestamp': 1234, 'message': b'foo'}
```

`fields` accepts a class or instance — including hand-written ctypes types —
and returns a tuple of `Field(name, type)` records. `asdict` takes an instance
and returns its fields as a dict.

## Licence

[MIT](LICENCE)
