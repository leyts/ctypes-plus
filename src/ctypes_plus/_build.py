"""Shared builder for the decorators."""

from annotationlib import get_annotations
from typing import (
    TYPE_CHECKING,
    Annotated,
    TypeAliasType,
    TypeIs,
    get_args,
    get_origin,
)

if TYPE_CHECKING:
    from ctypes import Structure, Union, _CData
else:
    from ctypes import Structure

    # `_CData`, the base of every ctypes type, isn't importable at runtime.
    _CData = Structure.__base__

# Descriptors/attributes that must not be copied into the new ctypes class.
_SKIP = frozenset({"__dict__", "__weakref__", "__annotations__"})


def _unwrap_type_alias(annotation: object) -> object:
    """Return the value behind a type alias."""
    while isinstance(annotation, TypeAliasType):
        annotation = annotation.__value__
    return annotation


def _is_ctypes_type(obj: object) -> TypeIs[type[_CData]]:
    """Return ``True`` if ``obj`` is a ctypes data type."""
    return isinstance(obj, type) and issubclass(obj, _CData)


def _resolve_ctype(annotation: object) -> type[_CData]:
    """Return the ctypes type for a field annotation.

    Accepts a plain ctypes type, or an ``Annotated[native, ctype]`` whose
    metadata carries the ctypes type (see :mod:`ctypes_plus.types`). ``type``
    aliases of either are unwrapped, so user-defined aliases work too.
    """
    annotation = _unwrap_type_alias(annotation)
    if get_origin(annotation) is Annotated:
        for meta in get_args(annotation)[1:]:
            ctype = _unwrap_type_alias(meta)
            if _is_ctypes_type(ctype):
                return ctype
        msg = f"no ctypes type in annotation metadata: {annotation!r}"
        raise TypeError(msg)

    if not _is_ctypes_type(annotation):
        msg = f"unsupported field annotation: {annotation!r}"
        raise TypeError(msg)
    return annotation


def _repr(self: Structure | Union) -> str:
    args = ", ".join(
        f"{name}={getattr(self, name)!r}" for name, *_ in type(self)._fields_
    )
    return f"{type(self).__name__}({args})"


def build(cls: type, base: type[Structure | Union]) -> type:
    """Build a ctypes ``base`` subclass from ``cls``'s annotations.

    Reads the evaluated annotations off ``cls`` and turns each into a
    ``_fields_`` entry, then creates a new subclass of ``base`` (a
    ``ctypes.Structure`` or ``ctypes.Union``) carrying those fields along with
    any methods defined on the original class.
    """
    annotations = get_annotations(cls)
    # The copied `__annotate_func__` lets the new class manage its own
    # `__annotations__` lazily (PEP 749), so we never assign it directly.
    namespace = {
        key: value for key, value in vars(cls).items() if key not in _SKIP
    }
    namespace["_fields_"] = [
        (name, _resolve_ctype(ann)) for name, ann in annotations.items()
    ]
    # Only supply a repr if one wasn't already defined.
    namespace.setdefault("__repr__", _repr)
    return type(cls.__name__, (base,), namespace)
