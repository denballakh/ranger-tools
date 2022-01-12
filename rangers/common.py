from __future__ import annotations
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    Iterable,
    Protocol,
    TypeVar,
    Iterator,
    Container,
    Sequence,
)

import sys
import gc
import os

from functools import lru_cache
import random



_T = TypeVar('_T')
_G = TypeVar('_G')


class LessComparable(Protocol):
    def __lt__(self: _T, other: _T) -> bool:
        ...


_TLC = TypeVar('_TLC', bound=LessComparable)


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
        raise RuntimeError('Mapping proxy referents to several objects', mp, referents)
    return referents[0]


def noop(*_: Any, **__: Any) -> None:
    pass


def identity(x: _T, /) -> _T:
    return x


def probability(f: float, /, *, __uniform: Callable[[float, float], float] = random.uniform) -> bool:
    return __uniform(0.0, 1.0) < f


def minmax(a: _TLC, b: _TLC) -> tuple[_TLC, _TLC]:
    if a < b:
        return a, b
    return b, a


def clamp(v: _TLC, lt: _TLC, gt: _TLC) -> _TLC:
    if v < lt:
        return lt
    if gt < v:
        return gt
    return v


def fmt_file_size(size: float) -> tuple[float, str]:
    if not size:
        return size, '  '
    sign = [-1, 1][size > 0]
    size = abs(size)

    units = {
        +0: 'B ',
        +1: 'KB',
        +2: 'MB',
        +3: 'GB',
        +4: 'TB',
    }

    unit_p = 0

    while size >= 1000.0 and unit_p + 1 in units:
        size /= 1000.0
        unit_p += 1

    while size < 1.0 and unit_p - 1 in units:
        size *= 1000.0
        unit_p -= 1

    return size * sign, units[unit_p]


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


def make_number(num: float, unit: str, n: int) -> str:
    return f'{round_to_n_chars(num, n)} {unit}'


def round_to_three_chars(f: float) -> float | int:
    if abs(f) >= 999.5:
        return float('inf')
    if abs(f) >= 9.95:
        return round(f)
    return round(f, 1)


def round_to_n_chars(f: float, n: int) -> float | int:
    for i in reversed(range(21)):
        if len(str(round(f, i))) <= n:
            return round(f, i)
    return round(f)


def rand31pm(seed: int) -> Iterator[int]:
    while True:
        hi: int
        lo: int
        hi, lo = divmod(seed, 0x1F31D)
        seed = lo * 0x41A7 - hi * 0xB14
        if seed < 1:
            seed += 0x7FFFFFFF
        yield seed - 1


def is_dunder(s: str) -> bool:
    """
    __x__
    """
    return s.startswith('__') and s.endswith('__')


def is_sunder(s: str) -> bool:
    """
    _x_
    """
    return s.startswith('_') and s.endswith('_') and not s.startswith('__') and not s.endswith('__')


def is_private(s: str) -> bool:
    """
    _x
    """
    return s.startswith('_') and not s.startswith('__')


def is_mangled(s: str) -> bool:
    """
    _cls__x
    """
    return is_private(s) and not s.endswith('_') and '__' in s


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
        # print(*[getattr(cls, attr, None).__class__.__name__ for attr in dir(cls)])
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

    except:
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


def recursive_subclasses(cls: type, /) -> list[type]:
    subclasses = cls.__subclasses__()
    result: set[type] = set(subclasses)
    for c in subclasses:
        result |= set(recursive_subclasses(c))
    return list(result)


def create_empty_instance(cls: type[_T], /) -> _T | None:
    try:
        return cls()
    except:
        pass

    try:
        return object.__new__(cls)
    except:
        pass

    return None


def get_attributes(obj: object, /) -> list[tuple[str, object]]:
    cls = type(obj)
    kwarg_pairs: list[tuple[str, Any]] = []

    for attr_list_attr in {
        '__slots__',  # classes with slots
        '__mypyc_attrs__',  # compiled mypyc classes
        '__attrs_attrs__',  # attrs classes
    }:
        if (attr_list := getattr(obj, attr_list_attr, None)) is not None:
            for attr in attr_list:
                if hasattr(obj, attr):
                    kwarg_pairs.append((attr, getattr(obj, attr)))

    if (__dict__ := getattr(obj, '__dict__', None)) is not None:
        for attr, value in __dict__.items():
            kwarg_pairs.append((attr, value))

    return kwarg_pairs


def check_dir(path: str) -> None:
    path = path.replace('\\', '/').replace('//', '/')
    splitted = path.split('/')[:-1]
    splitted = [name.strip('/') for name in splitted]
    splitted = [name for name in splitted if name != '']
    splitted = [name + '/' for name in splitted]
    res = './'
    for item in splitted:
        res += item
        if not os.path.isdir(res):
            try:
                os.mkdir(res)
            except FileExistsError:
                pass


_tree_walker_def_cond: Callable[[str], bool] = lambda x: True


def tree_walker(
    path: str,
    cond: Callable[[str], bool] = _tree_walker_def_cond,
    exts: Sequence[str] = (),
    root: bool = False,
) -> tuple[list[str], list[str]]:
    if exts is not None and cond is not _tree_walker_def_cond:
        raise TypeError

    if cond is _tree_walker_def_cond:
        if exts:
            cond = lambda s: any(s.endswith(x) for x in exts)

    files = list[str]()
    dirs = list[str]()
    iterator = (
        os.walk(path)
        if not root
        else [
            (
                '',
                [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(x)],
                [os.path.join(path, x) for x in os.listdir(path) if os.path.isfile(x)],
            )
        ]
    )

    for prefix, dirs_, files_ in iterator:
        for file in files_:
            fullfile = os.path.join(prefix, file)
            if cond(fullfile):
                files.append(fullfile)

        for dir_ in dirs_:
            fulldir = os.path.join(prefix, dir_)
            if cond(fulldir):
                dirs.append(fulldir)

    return files, dirs


def file_rebase(file: str, base: str, new_base: str) -> str:
    return file.replace(base, new_base, 1)


def change_ext(file: str, before: str, after: str) -> str:
    return file[::-1].replace(before[::-1], after[::-1], 1)[::-1]


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
