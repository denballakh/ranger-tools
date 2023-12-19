from __future__ import annotations
from typing import (
    Any,
    Callable,
    ClassVar,
    Iterator,
    NoReturn,
    TypeVar,
    overload,
    Sequence,
)

from math import sin, cos, atan2, hypot, pi

__all__ = (
    'Point',
    'MPoint',
    # comparators:
    'xy_cmp',
    'yx_cmp',
    'angle_cmp',
    'dist_cmp',
)

P = TypeVar('P', bound='_PointCommon')


class _PointCommon(Sequence[float]):
    __slots__ = ('x', 'y')
    __match_args__ = ('x', 'y')

    x: float
    y: float

    def __init__(self, x: float, y: float, /) -> None:
        raise NotImplementedError

    def __str__(self, /) -> str:
        return f'<{self.__class__.__name__}: x={self.x!r}, y={self.y!r}>'

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__}({self.x!r},{self.y!r})'

    def __eq__(self, other: object, /) -> bool:
        """=="""
        if isinstance(other, _PointCommon):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        """!="""
        if isinstance(other, _PointCommon):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __iter__(self, /) -> Iterator[float]:
        yield self.x
        yield self.y

    def __complex__(self, /) -> complex:
        return self.x + self.y * 1j

    def __abs__(self, /) -> float:
        return self.abs()

    def __neg__(self: P, /) -> P:
        """-p"""
        return self.__class__(-self.x, -self.y)

    def __pos__(self: P, /) -> P:
        """+p"""
        return self.__class__(self.x, self.y)

    def __invert__(self: P, /) -> P:
        """~p"""
        return self.__class__(self.y, self.x)

    def __add__(self: P, other: _PointCommon, /) -> P:
        """p1 + p2"""
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self: P, other: _PointCommon, /) -> P:
        """p1 - p2"""
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self: P, other: float, /) -> P:
        """p * x"""
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self: P, other: float, /) -> P:
        """x * p"""
        return self.__class__(other * self.x, other * self.y)

    def __truediv__(self: P, other: float, /) -> P:
        """p / x"""
        return self.__class__(self.x / other, self.y / other)

    def __matmul__(self: P, other: _PointCommon, /) -> float:
        """p1 @ p2"""
        return self.x * other.x + self.y * other.y

    def __mod__(self: P, other: float | _PointCommon, /) -> P:
        """p1 % p2  p % x"""
        if isinstance(other, _PointCommon):
            return self.__class__(self.x % other.x, self.y % other.y)
        if isinstance(other, float):
            return self.__class__(self.x % other, self.y % other)
        return NotImplemented  # type: ignore[unreachable]

    def __round__(self: P, ndigits: int | None = None, /) -> P:
        if ndigits is not None:
            return self.__class__(self.x.__round__(ndigits), self.y.__round__(ndigits))
        else:
            return self.__class__(self.x.__round__(), self.y.__round__())

    def __ceil__(self: P, /) -> P:
        return self.__class__(self.x.__ceil__(), self.y.__ceil__())

    def __floor__(self: P, /) -> P:
        return self.__class__(self.x.__floor__(), self.y.__floor__())

    def __trunc__(self: P, /) -> P:
        return self.__class__(self.x.__trunc__(), self.y.__trunc__())

    def __reduce__(self: P, /) -> tuple[type[P], tuple[float, float]]:
        return self.__class__, (self.x, self.y)

    @classmethod
    def from_angle(cls: type[P], angle: float, magn: float = 1.0, /) -> P:
        return cls(cos(angle) * magn, sin(angle) * magn)

    @classmethod
    def from_complex(cls: type[P], val: complex, /) -> P:
        return cls(val.real, val.imag)

    @classmethod
    def from_tuple(cls: type[P], tup: tuple[float, float], /) -> P:
        return cls(tup[0], tup[1])

    @classmethod
    def from_point(cls: type[P], p: _PointCommon, /) -> P:
        return cls(p.x, p.y)

    def to_tuple(self, /) -> tuple[float, float]:
        return (self.x, self.y)

    def round(self, /) -> tuple[int, int]:
        return (round(self.x), round(self.y))

    def trunc(self, /) -> tuple[int, int]:
        return (int(self.x), int(self.y))

    def abs(self, /) -> float:
        return hypot(self.x, self.y)

    def angle(self, /) -> float:
        return atan2(self.y, self.x)

    def norm(self: P, /) -> P:
        return self / self.abs()

    def rotate(self: P, angle: float, /) -> P:
        return self.__class__.from_angle(self.angle() + angle, self.abs())

    def angle_to(self, other: _PointCommon, /) -> float:
        return (other.angle() - self.angle()) % (2 * pi)
        # return other.rotate(-self.angle()).angle()

    def dist(self, other: _PointCommon, /) -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def dist2(self, other: _PointCommon, /) -> float:
        return (self.x - other.x) ** 2.0 + (self.y - other.y) ** 2.0

    @overload
    def __getitem__(self, index: int) -> float: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[float]: ...
    def __getitem__(self, index: int | slice) -> float | Sequence[float]:
        if isinstance(index, slice):
            raise TypeError(index)
        return self.to_tuple()[index]
    def index(self, value: Any, start: int = 0, stop: int = -1) -> int:
        raise NotImplementedError
    def count(self, value: Any) -> int:
        raise NotImplementedError
    def __contains__(self, value: object) -> bool:
        return value in self.to_tuple()
    def __reversed__(self) -> Iterator[float]:
        return reversed(self.to_tuple())
    def __len__(self) -> int:
        return 2


# direct setters for attributes to prevent AttributeError on immutable instances
_set_x: Callable[[_PointCommon, float], None] = _PointCommon.x.__set__  # type: ignore[attr-defined, misc]
_set_y: Callable[[_PointCommon, float], None] = _PointCommon.y.__set__  # type: ignore[attr-defined, misc]


class Point(_PointCommon):
    """
    Immutable
    """

    __slots__ = ()

    p00: ClassVar[Point]
    p10: ClassVar[Point]
    p01: ClassVar[Point]
    p11: ClassVar[Point]

    def __init__(self, x: float, y: float, /) -> None:
        _set_x(self, x)
        _set_y(self, y)

    def __hash__(self, /) -> int:
        return hash((self.x, self.y))

    def __copy__(self: P, /) -> P:
        return self

    def __pos__(self: P, /) -> P:
        return self

    def __setattr__(self, attr: str, val: Any) -> None:
        if hasattr(self, attr):
            raise AttributeError(
                f'{self.__class__.__name__!r} object attribute {attr!r} is read-only'
            )
        else:
            raise AttributeError(f'{self.__class__.__name__} object has no attribute {attr!r}')


Point.p00 = Point(0, 0)
Point.p10 = Point(1, 0)
Point.p01 = Point(0, 1)
Point.p11 = Point(1, 1)


class MPoint(_PointCommon):
    """
    Mutable
    """

    __slots__ = ()

    __hash__ = None  # type: ignore[assignment]

    def __init__(self, x: float, y: float, /) -> None:
        self.x = x
        self.y = y

    def __copy__(self: P, /) -> P:
        return self.__class__(self.x, self.y)

    def __iadd__(self: P, other: _PointCommon, /) -> P:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self: P, other: _PointCommon, /) -> P:
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self: P, other: float, /) -> P:
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self: P, other: float, /) -> P:
        self.x /= other
        self.y /= other
        return self

    def __imod__(self: P, other: float | _PointCommon, /) -> P:
        if isinstance(other, _PointCommon):
            self.x %= other.x
            self.y %= other.y
            return self
        if isinstance(other, float):
            self.x %= other
            self.y %= other
            return self
        raise TypeError

    def inorm(self: P, /) -> P:
        self /= self.abs()
        return self

    def irotate(self: P, angle: float, /) -> P:
        magn = self.abs()
        newang = self.angle() + angle
        self.x = cos(newang) * magn
        self.y = sin(newang) * magn
        return self


# comparators:
def xy_cmp(p: _PointCommon, /) -> tuple[float, float]:
    return (p.x, p.y)


def yx_cmp(p: _PointCommon, /) -> tuple[float, float]:
    return (p.y, p.x)


def angle_cmp(p: _PointCommon, /) -> tuple[float, float]:
    return (p.angle(), p.abs())


def dist_cmp(p: _PointCommon | None = None, /) -> Callable[[_PointCommon], float]:
    if p is None:
        return _PointCommon.abs  # compare by dist from origin
    else:
        return p.dist  # compare by dist from p


# x: Sequence[float] = Point(0, 0)
