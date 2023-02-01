from __future__ import annotations
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    Hashable,
    Literal,
    NoReturn,
    Protocol,
    TypeGuard,
    TypeVar,
    Iterator,
    overload,
)

import sys
import gc
from pathlib import Path
import warnings
from collections import defaultdict
from functools import lru_cache
import random


_T = TypeVar('_T')
_G = TypeVar('_G')


class LessComparable(Protocol):
    def __lt__(self: _T, other: _T) -> bool:
        ...


_TLC = TypeVar('_TLC', bound=LessComparable)


class TypedEqual:
    __slots__ = ('obj',)
    obj: Any

    def __init__(self, obj: Any) -> None:
        self.obj = obj

    def __eq__(self, obj: Any) -> bool:
        return type(obj) is type(self.obj) and (self.obj is obj or self.obj == obj)

    def __ne__(self, obj: Any) -> bool:
        return type(obj) is not type(self.obj) or self.obj is not obj and self.obj != obj

    def __hash__(self) -> int:
        return hash(self.obj)

    def __repr__(self) -> str:
        return f'<typed equality wrapper: {self.obj!r}>'


class IdentityEqual:
    __slots__ = ('obj',)
    obj: Any

    def __init__(self, obj: Any) -> None:
        self.obj = obj

    def __eq__(self, obj: Any) -> bool:
        return obj is self.obj

    def __ne__(self, obj: Any) -> bool:
        return obj is not self.obj

    def __hash__(self) -> int:
        return hash(self.obj)

    def __repr__(self) -> str:
        return f'<identity equality wrapper: {self.obj!r}>'


class Truthy(Protocol):
    def __bool__(self) -> Literal[True]:
        ...


class Falsy(Protocol):
    def __bool__(self) -> Literal[False]:
        ...


def debug_level() -> Literal[0, 1, 2]:
    """docstring for internal use"""
    if __debug__:
        return 0
    if debug_level.__doc__ is not None:
        return 1
    return 2


def typed_memory_usage() -> dict[type, int]:
    gc.collect()
    objs = gc.get_objects()
    d: defaultdict[type, int] = defaultdict(int)
    for x in objs:
        d[type(x)] += sys.getsizeof(x)
    return dict(sorted(d.items(), key=lambda pair: -pair[1]))


def _get_mappingproxy_dict(mp: MappingProxyType[_T, _G], /) -> dict[_T, _G]:
    """!
    >>> from types import MappingProxyType as mp
    >>> d = {}
    >>> p = mp(d)
    >>> _get_mappingproxy_dict(p) is d
    True
    """
    referents = gc.get_referents(mp)
    if len(referents) != 1:
        raise RuntimeError('Mapping proxy refers to several objects', mp, referents)
    dct = referents[0]
    assert isinstance(dct, dict)
    return dct


# fmt: off
@overload
def assert_(condition: Truthy, msg: Any = None) -> None: ...
@overload
def assert_(condition: Falsy, msg: Any = None) -> NoReturn: ...
@overload
def assert_(condition: Any, msg: Any = None) -> None | NoReturn: ...
# fmt: on
def assert_(condition: Any, msg: Any = None) -> None:
    if not condition:
        if msg is not None:
            raise AssertionError(msg)
        raise AssertionError


def raise_(
    exc: BaseException | type[BaseException] | None = None,
    from_: BaseException | type[BaseException] | None = None,
) -> NoReturn:
    if exc is not None:
        raise exc from from_
    raise


def hashable(obj: object) -> TypeGuard[Hashable]:
    try:
        hash(obj)
    except TypeError:
        return False
    else:
        return True


def noop(*_: Any, **__: Any) -> None:
    pass


def call(c: Callable[[], _T], /) -> _T:
    return c()


def identity(x: _T, /) -> _T:
    return x


def probability(
    f: float, /, *, __uniform: Callable[[float, float], float] = random.uniform
) -> bool:
    return __uniform(0.0, 1.0) < f


def minmax(a: _TLC, b: _TLC, /) -> tuple[_TLC, _TLC]:
    if a < b:
        return a, b
    return b, a


def clamp(v: _TLC, lt: _TLC, gt: _TLC, /) -> _TLC:
    if v < lt:
        return lt
    if gt < v:
        return gt
    return v


# def fmt_file_size(size: float) -> tuple[float, str]:
#     if not size:
#         return size, '  '
#     sign = [-1, 1][size > 0]
#     size = abs(size)

#     units = {
#         +0: 'B ',
#         +1: 'KB',
#         +2: 'MB',
#         +3: 'GB',
#         +4: 'TB',
#     }

#     unit_p = 0

#     while size >= 1000.0 and unit_p + 1 in units:
#         size /= 1000.0
#         unit_p += 1

#     while size < 1.0 and unit_p - 1 in units:
#         size *= 1000.0
#         unit_p -= 1

#     return size * sign, units[unit_p]


def fmt_time(time: float) -> tuple[float, str]:
    if not time:
        return time, '  '
    sign = [-1, 1][time > 0]
    time = abs(time)

    units = {
        -5: 'fs',
        -4: 'ps',
        -3: 'ns',
        -2: 'μs',
        -1: 'ms',
        +0: 's ',
    }

    unit_p = 0

    while time >= 999.5 and unit_p + 1 in units:
        time /= 1000.0
        unit_p += 1

    while time < 0.995 and unit_p - 1 in units:
        time *= 1000.0
        unit_p -= 1

    return time * sign, units[unit_p]


# def make_number(num: float, unit: str, n: int) -> str:
#     return f'{round_to_n_chars(num, n)} {unit}'


def round_to_three_chars(f: float) -> float | int:
    if abs(f) >= 999.5:
        return float('inf')
    if abs(f) >= 9.95:
        return round(f)
    return round(f, 1)


# def round_to_n_chars(f: float, n: int) -> float | int:
#     for i in reversed(range(21)):
#         if len(str(round(f, i))) <= n:
#             return round(f, i)
#     return round(f)


def rand31pm(seed: int, /) -> Iterator[int]:
    while True:
        hi, lo = divmod(seed, 0x1F31D)
        seed = lo * 0x41A7 - hi * 0xB14
        if seed < 1:
            seed += 0x7FFFFFFF
        yield seed - 1


def is_compiled(cls: type, unknown: int = -1) -> int:
    """!
    >>> is_compiled(int)
    1
    >>> is_compiled(type('X', (), {}))
    0
    >>> class X: pass
    ...
    >>> is_compiled(X)
    0
    >>> is_compiled(__import__('enum').Enum)
    0
    """

    try:
        if any(
            getattr(cls, attr, None).__class__.__name__ == (lambda: None).__class__.__name__
            for attr in dir(cls)
        ):
            return 0

        if cls.__module__ == '__main__':
            return 0

        if cls.__module__ == 'builtins':
            return 1

        module = sys.modules.get(cls.__module__, None)
        if module is None:
            return unknown

        loader = module.__loader__
        if loader is not None:
            if loader.__class__.__name__ in {'ExtensionFileLoader'}:
                return 1
            if loader.__class__.__name__ in {'SourceFileLoader'}:
                return 0
            if getattr(loader, '__name__', None) in {
                'FrozenImporter',
                'BuiltinImporter',
                'nuitka_module_loader',
            }:
                return 1

        spec = module.__spec__
        if spec is not None and spec.origin is not None:
            if spec.origin.endswith('built-in'):
                return 1
            if spec.origin.endswith('.pyd'):
                return 1
            if spec.origin.endswith('.py'):
                return 0

        return unknown

    except Exception:
        return unknown


@lru_cache
def coerce_child(cls1: type[_T], cls2: type[_G], /) -> type[_T] | type[_G] | None:
    """!
    >>> coerce_child(int, bool)
    <class 'bool'>
    >>> coerce_child(int, object)
    <class 'int'>
    >>> coerce_child(int, str)
    >>>
    """
    if cls1 is cls2:
        return cls1

    if issubclass(cls1, cls2):
        return cls1

    if issubclass(cls2, cls1):
        return cls2

    return None


@lru_cache
def coerce_parent(cls1: type[_T], cls2: type[_G], /) -> type[_T] | type[_G] | None:
    """!
    >>> coerce_parent(int, bool)
    <class 'int'>
    >>> coerce_parent(int, object)
    <class 'object'>
    >>> coerce_parent(int, str)
    >>>
    """
    if cls1 is cls2:
        return cls1

    if issubclass(cls1, cls2):
        return cls2

    if issubclass(cls2, cls1):
        return cls1

    return None


def get_attributes(obj: object, /) -> list[tuple[str, object]]:
    cls = type(obj)
    kwarg_pairs: list[tuple[str, Any]] = []

    for attr_list_attr in (
        '__slots__',  # classes with slots
        '__mypyc_attrs__',  # compiled mypyc classes
        '__attrs_attrs__',  # attrs classes
    ):
        if (attr_list := getattr(cls, attr_list_attr, None)) is not None:
            for attr in attr_list:
                if hasattr(obj, attr):
                    kwarg_pairs.append((attr, getattr(obj, attr)))

    if (__dict__ := getattr(obj, '__dict__', None)) is not None:
        for attr, value in __dict__.items():
            kwarg_pairs.append((attr, value))

    return kwarg_pairs


def convert_ini_to_dict(content: str) -> dict[str, str]:
    result = dict[str, str]()
    for s in content.split('\n'):
        if not s.strip():
            continue
        if '=' not in s:
            continue
        if s.startswith('#'):
            continue

        key, val = s.split('=', 1)
        if key in result:
            result[key] += '\n' + val
        else:
            result[key] = val
    return result


# TODO: move it to gi
def rgb565le_to_rgb888(rgb16: bytes) -> tuple[int, int, int]:
    # Unpack from little endian 2 bytes
    r = rgb16[1] & 0b11111000
    g = (rgb16[0] & 0b11100000) >> 5 | (rgb16[1] & 0b00000111) << 3
    b = rgb16[0] & 0b00011111

    g <<= 2
    b <<= 3

    return r, g, b


def rgb24_to_rgb16(rgb24: tuple[int, int, int]) -> bytes:
    r, g, b = rgb24

    r = round(r / 0xFF * 0x1F) << 11
    g = round(g / 0xFF * 0x3F) << 5
    b = round(b / 0xFF * 0x1F)

    if r | g | b > 0xFFFF:
        raise ValueError

    a, b = divmod(r | g | b, 0x100)

    return bytes([b, a])


def rgb888_to_rgb565le(r: int, g: int, b: int) -> bytes:
    # Essentially reducing green channel bit depth to 5 after reduction for white balance
    g &= 0b11111011

    r = r >> 3 << 11
    g = g >> 2 << 5
    b = b >> 3

    # Pack into little endian 2 bytes
    return bytes([g & 0b11100000 | b, (r | g) >> 8])
