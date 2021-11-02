from __future__ import annotations

from typing import (
    TypeVar,
    TypeGuard,
    Protocol,
    Generic,
    Any,
    overload,
)
from types import NotImplementedType

import copy


__all__ = [
    'cast',
    'Castable',
    'CastError',
]


T = TypeVar('T')
G = TypeVar('G')


class CastError(Exception):
    pass


class Castable(Generic[T], Protocol):
    __casts_to__: tuple[type, ...]
    __casts_from__: tuple[type, ...]

    @classmethod
    def __cast_from__(cls: type[T], value: G) -> T | NotImplementedType:
        ...

    def __cast_to__(self: G, valuecls: type[T]) -> T | NotImplementedType:
        ...


def _is_castable_cls(cls: type) -> TypeGuard[type[Castable]]:
    return all(
        hasattr(cls, member)
        for member in (
            '__casts_to__',
            '__casts_from__',
            '__cast_to__',
            '__cast_from__',
        )
    )


def _is_castable_value(value) -> TypeGuard[Castable]:
    return _is_castable_cls(type(value))


def _cast(value: G, cls: type[T]) -> T:
    if _is_castable_value(value):
        casts = value.__casts_to__
        if any(issubclass(cls, C) or C in (Any, object, type(value)) for C in casts):
            result = value.__cast_to__(cls)
            if result is not NotImplemented:
                return result

    if _is_castable_cls(cls):
        casts = cls.__casts_from__
        if any(issubclass(type(value), C) or C in (Any, object, cls) for C in casts):
            result = cls.__cast_from__(value)
            if result is not NotImplemented:
                return result

    if cls is type(value):
        try:
            return copy.copy(value)
        except copy.Error:
            pass

    return NotImplemented


# fmt: off
@overload
def cast(value: Any, cls: type[T], /) -> T: ...
@overload
def cast(value: Any, /, *clss: type[T]) -> T: ...

def cast(value: Any, /, *clss: type[T]) -> T:
    if not clss:
        raise CastError('cast() takes at least 1 class in cast chain')

    for cls in clss:
        result = _cast(value, cls)
        if result is NotImplemented:
            raise CastError(f'Cannot cast value {value!r} to class {cls.__qualname__}')
        value = result
    return value
# fmt: on


class M:
    def __repr__(self):
        return f'{type(self).__qualname__}({self.val!r})'

    def __init__(self, val):
        self.val = val

    __casts_to__ = (int,)
    __casts_from__ = (int, object)

    def __cast_to__(self, cls):
        if issubclass(cls, int):
            return cls(self.val)
        if issubclass(cls, M):
            return cls(self.val)
        return NotImplemented

    @classmethod
    def __cast_from__(cls, val):
        if isinstance(val, int):
            return cls(val)
        if isinstance(val, M):
            return cls(val.val)

        return cls(id(val))


def _create_empty_instance(cls: type[T]) -> T | None:
    try:
        return object.__new__(cls)
    except TypeError:
        return None


class DictCast(dict):
    def __repr__(self):
        return f'{type(self).__name__}({repr(dict(self))})'

    __casts_to__ = (object,)
    __casts_from__ = (object,)

    def __cast_to__(self, cls):
        obj = _create_empty_instance(cls)
        if obj is None:
            return NotImplemented

        for key, value in self.items():
            setattr(obj, key, value)
        return obj

    @classmethod
    def __cast_from__(cls, val):
        self = cls()

        if (d := getattr(val, '__dict__', None)) is not None:
            for k, v in d.items():
                self[k] = v

        if (slots := getattr(val, '__slots__', None)) is not None:
            for k in slots:
                v = getattr(self, k, None)
                self[k] = v
        return self
