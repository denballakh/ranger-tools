"""!
@file
"""
from __future__ import annotations
from typing import (
    Any,
    Callable,
    TypeVar,
    Iterator,
    Container,
    Sequence,
)
from itertools import repeat
from functools import lru_cache

import os
import sys

_T = TypeVar('_T')
_G = TypeVar('_G')

# def sizeof_fmt(num, suffix="B"):
#     for unit in ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]:
#         if abs(num) < 1024.0:
#             if isinstance(num, int):
#                 return f"{num} {unit}{suffix}"
#             return f"{num:3.1f} {unit}{suffix}"
#         num /= 1024.0
#     return f"{num:.1f} {unit}{suffix}"


# def pretty_size(n, pow=0, b=1024, u='B', pre=[''] + [p + 'i' for p in 'KMGTPEZY']):
#     from math import log

#     pow, n = min(int(log(max(n * b ** pow, 1), b)), len(pre) - 1), n * b ** pow
#     return "%%.%if %%s%%s" % abs(pow % (-pow - 1)) % (n / b ** float(pow), pre[pow], u)


# def prettier_size(n, pow=0, b=1024, u='B', pre=[''] + [p + 'i' for p in 'KMGTPEZY']):
#     r, f = min(int(log(max(n * b ** pow, 1), b)), len(pre) - 1), '{:,.%if} %s%s'
#     return (f % (abs(r % (-r - 1)), pre[r], u)).format(n * b ** pow / b ** float(r))


def make_number(num: float, unit: str, n: int) -> str:
    return f'{round_to_n_chars(num, n)} {unit}'


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


def round_to_three_chars(f: float) -> float | int:
    if abs(f) >= 999.5:
        return float('inf')
    if abs(f) >= 9.95:
        return round(f)
    return round(f, 1)


def round_to_n_chars(f: float, n: int) -> float | int:
    for i in range(20, -1, -1):
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
            if getattr(loader, '__name__', None) in {'FrozenImporter', 'BuiltinImporter'}:
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


def identity(x: _T, /) -> _T:
    return x


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
    kwarg_pairs = list[tuple[str, Any]]()
    _missing = object()
    if (__slots__ := getattr(obj, '__slots__', None)) is not None:
        for attr in __slots__:
            value = getattr(obj, attr, _missing)
            if value is not _missing:
                kwarg_pairs.append((attr, value))

    if (__dict__ := getattr(obj, '__dict__', None)) is not None:
        for attr, value in __dict__.items():
            kwarg_pairs.append((attr, value))

    return kwarg_pairs


##
# Clamping to 0, 255
def _clamp(v: float) -> int:
    if v < 0:
        return 0
    if v > 255:
        return 255
    return round(v)


# (1 - k / 2) * k == 1 - (1 - (1 - k / 2)) / k
def darken(k: float) -> Callable[[float], float]:
    assert 0 < k < 2, f'Value for k should be between 0 and 2: k = {k}'

    k /= 2  # For balance to be at 1 instead of 0.5
    _k = 1 - k
    kd = k / _k

    def f(x: float) -> float:
        if x > _k:
            return 1 - (1 - x) / kd
        return x * kd

    return f


def average(
    c1: tuple[float, float, float], c2: tuple[float, float, float], ratio: float = 0.5
) -> tuple[float, float, float]:
    return tuple(y * ratio + x * (1 - ratio) for x, y in zip(c1, c2))  # type: ignore[return-value]


def my_mul(x: float, mn: float, mx: float, mul: float) -> float:
    assert mul >= 0
    if mul < 1:
        result = mn + (x - mn) * mul
    elif mul > 1:
        result = mx - (mx - x) / mul
    else:
        result = x
    return min(max(result, mn), mx)


# FIXME move back to interface colorer
def recolor(
    color: tuple[int, int, int, int] | list[int],
    mask: tuple[int, int, int, int] | list[int] | None,
    red_angle: float,
    green_angle: float,
    blue_angle: float,
    brightness: float,
    lightness: Callable[[float], float],
    gamma: float,
    p_matrix: tuple[list[list[float]], list[list[float]], list[list[float]]],
) -> tuple[float, float, float, float]:
    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    mask = mask or (255, 255, 255, 255)

    r, g, b, a = color
    mr, mg, mb, ma = mask

    # mask = mr, mg, mb

    if mr in _255 and mg in _0 and mb in _0:
        angle = red_angle
        matrix = p_matrix[0]
    elif mr in _0 and mg in _255 and mb in _0:
        angle = green_angle
        matrix = p_matrix[1]
    else:
        angle = blue_angle
        matrix = p_matrix[2]

    # elif mr in _0  and mg in _0 and mb in _255:
    #     pass
    # elif mr in _255  and mg in _255 and mb in _255:
    #     pass
    # else:
    #     pass

    # RGB hue rotation
    result: tuple[float, float, float] = (
        _clamp(color[0] * matrix[0][0] + color[1] * matrix[0][1] + color[2] * matrix[0][2]),
        _clamp(color[0] * matrix[1][0] + color[1] * matrix[1][1] + color[2] * matrix[1][2]),
        _clamp(color[0] * matrix[2][0] + color[1] * matrix[2][1] + color[2] * matrix[2][2]),
    )

    if angle == blue_angle:
        ratio = ma / 255

        if brightness != 0.0 or ratio != 1.0:
            # Linearize RGB from gamma
            result = tuple((channel / 255) ** gamma for channel in result)  # type: ignore[assignment]
            # Apply non-linearity
            result = tuple(lightness(channel) for channel in result)  # type: ignore[assignment]

            if ratio != 1.0:
                original: tuple[float, float, float] = tuple((channel / 255) ** gamma for channel in (r, g, b))  # type: ignore[assignment]
                result = average(original, result, ratio)

            # De-linearize to gamma
            result = tuple(channel ** (1 / gamma) * 255 for channel in result)  # type: ignore[assignment]

    return *result, a


##
# Degree of non-linearity expressed in values `(-∞, +∞)\{0}`. Non-linearity increases when approaching `0`
# Bias is neutral at `1.0`.
# Lowering value shifts bias of the non-linearity towards `0` on the x scale, raising shifts bias towards max
def nonlinear_brightness(dn: float, bias: float = 1.0) -> Callable[[float], float]:
    assert bias > 0, f'Value for bias should be higher than 0: bias = {bias}'
    assert dn != 0, 'Value for dn cannot be equal to 0'

    # To reflect behavior of positive dn values
    if dn < 0:
        dn -= 1

    def f(x: float) -> float:
        return ((1 + dn) * (x ** bias)) / (dn + (x ** bias))

    return f


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


def clamp(v: float, lt: float, gt: float) -> float:
    if v <= lt:
        return lt
    if v >= gt:
        return gt
    return v


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
