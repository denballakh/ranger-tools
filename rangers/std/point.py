from __future__ import annotations
from typing import Any, Callable, Final, Iterator

from math import sin, cos, atan2

__all__ = (
    'Point',
    # comparators:
    'xy_cmp',
    'yx_cmp',
    'angle_cmp',
    'dist_cmp',
)


class Point:
    """
    2D Point represented as two float
    Immutable: dont change coordinates!
    """

    __slots__ = ('x', 'y')
    __match_args__ = ('x', 'y')

    x: float
    y: float

    def __init__(self, x: float, y: float, /) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_angle(cls, angle: float, magn: float = 1.0, /) -> Point:
        return cls(cos(angle) * magn, sin(angle) * magn)

    @classmethod
    def from_complex(cls, val: complex, /) -> Point:
        return cls(val.real, val.imag)

    @classmethod
    def from_tuple(cls, tup: tuple[float, float], /) -> Point:
        return cls(*tup)

    def __str__(self, /) -> str:
        return f'<{self.__class__.__name__}: x={self.x!r}, y={self.y!r}>'

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__}({self.x!r},{self.y!r})'

    def __hash__(self, /) -> int:
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        if isinstance(other, Point):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __iter__(self, /) -> Iterator[float]:
        yield self.x
        yield self.y

    def __getitem__(self, index: int, /) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError(index)

    def __len__(self, /) -> int:
        return 2

    def __reduce__(self, /) -> tuple[type, tuple[float, float]]:
        return self.__class__, (self.x, self.y)

    def __copy__(self, /) -> Point:
        return self

    def __deepcopy__(self, _: Any, /) -> Point:
        return self

    def __complex__(self, /) -> complex:
        return self.x + self.y * 1.0j

    def __abs__(self, /) -> float:
        return self.abs()

    def __neg__(self, /) -> Point:
        return self.__class__(-self.x, -self.y)

    def __pos__(self, /) -> Point:
        return self

    def __invert__(self, /) -> Point:
        return self.__class__(self.y, self.x)

    def __add__(self, other: Point, /) -> Point:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point, /) -> Point:
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float, /) -> Point:
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self, other: float, /) -> Point:
        return self.__class__(other * self.x, other * self.y)

    def __truediv__(self, other: float, /) -> Point:
        return self.__class__(self.x / other, self.y / other)

    def __rtruediv__(self, other: float, /) -> Point:
        return self.__class__(other / self.x, other / self.y)

    def __matmul__(self, other: Point, /) -> float:
        return self.x * other.x + self.y * other.y

    def __mod__(self, other: float | Point, /) -> Point:
        if isinstance(other, float):
            return self.__class__(self.x % other, self.y % other)
        if isinstance(other, Point):
            return self.__class__(self.x % other.x, self.y % other.y)
        return NotImplemented

    def __round__(self, ndigits: int = None, /) -> Point:
        if ndigits is not None:
            return self.__class__(self.x.__round__(ndigits), self.y.__round__(ndigits))
        else:
            return self.__class__(self.x.__round__(), self.y.__round__())

    def __ceil__(self, /) -> Point:
        return self.__class__(self.x.__ceil__(), self.y.__ceil__())

    def __floor__(self, /) -> Point:
        return self.__class__(self.x.__floor__(), self.y.__floor__())

    def __trunc__(self, /) -> Point:
        return self.__class__(self.x.__trunc__(), self.y.__trunc__())

    def abs(self, /) -> float:
        return (self.x ** 2.0 + self.y ** 2.0) ** 0.5

    def angle(self, /) -> float:
        return atan2(self.y, self.x)

    def norm(self, /) -> Point:
        magn = self.abs()
        return self.__class__(self.x / magn, self.y / magn)

    def rotate(self, angle: float, /) -> Point:
        return self.__class__.from_angle(self.angle() + angle, self.abs())

    def angle_to(self, other: Point, /) -> float:
        return other.rotate(-self.angle()).angle()

    def dist(self, other: Point, /) -> float:
        return ((self.x - other.x) ** 2.0 + (self.y - other.y) ** 2.0) ** 0.5

    def dist2(self, other: Point, /) -> float:
        return (self.x - other.x) ** 2.0 + (self.y - other.y) ** 2.0

    def to_tuple(self, /) -> tuple[float, float]:
        return (self.x, self.y)


# comparators:
def xy_cmp(p: Point, /) -> tuple[float, float]:
    return (p.x, p.y)


def yx_cmp(p: Point, /) -> tuple[float, float]:
    return (p.y, p.x)


def angle_cmp(p: Point, /) -> tuple[float, float]:
    return (p.angle(), p.abs())


def dist_cmp(p: Point = None, /) -> Callable[[Point], float]:
    if p is None:
        return Point.abs  # compare by dist from origin
    else:
        return p.dist  # compare by dist from p
