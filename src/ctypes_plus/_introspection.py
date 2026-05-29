"""Introspection and conversion helpers."""

from ctypes import Structure, Union
from typing import NamedTuple, TypeIs

# Imported at runtime so `Field`'s annotation stays resolvable for callers
# of `get_type_hints(Field)`.
from ctypes_plus._build import _CData  # noqa: TC001


class Field(NamedTuple):
    """A single ctypes field: its ``name`` and ctypes ``type``."""

    name: str
    type: type[_CData]


def _is_struct_or_union(obj: object) -> TypeIs[Structure | Union]:
    """Return ``True`` if ``obj`` is a ctypes Structure or Union instance."""
    return isinstance(obj, (Structure, Union))


def _struct_or_union_class(obj: object) -> type[Structure | Union]:
    """Resolve a ctypes Structure/Union class or instance to its class.

    Raises ``TypeError`` if ``obj`` is neither.
    """
    cls = obj if isinstance(obj, type) else type(obj)
    if not issubclass(cls, (Structure, Union)):
        msg = f"{obj!r} is not a ctypes Structure or Union"
        raise TypeError(msg)
    return cls


def fields(obj: object) -> tuple[Field, ...]:
    """Return the ``Field`` records of a ctypes Structure/Union.

    Accepts either the class itself or an instance of it. Raises ``TypeError``
    if ``obj`` is not (an instance of) a ctypes Structure or Union.
    """
    cls = _struct_or_union_class(obj)
    return tuple(Field(name, ctype) for name, ctype, *_ in cls._fields_)


def asdict(obj: object) -> dict[str, object]:
    """Return a ctypes Structure/Union instance's fields as a plain dict.

    Values are taken straight from attribute access (ctypes converts simple
    types to native Python objects). Raises ``TypeError`` if ``obj`` is not a
    ctypes Structure or Union instance.
    """
    if not _is_struct_or_union(obj):
        msg = (
            "asdict() should be called on a ctypes Structure or Union"
            f" instance, not {obj!r}"
        )
        raise TypeError(msg)
    return {name: getattr(obj, name) for name, *_ in type(obj)._fields_}
