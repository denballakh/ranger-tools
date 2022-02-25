from __future__ import annotations
from typing import Any, Callable, Iterator, NoReturn, TypeVar

from math import sin, cos, atan2

__all__ = (
    'Point',
    'MPoint',
    # comparators:
    'xy_cmp',
    'yx_cmp',
    'angle_cmp',
    'dist_cmp',
)

P = TypeVar('P', bound='Point')
MP = TypeVar('MP', bound='MPoint')


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
        # self.__class__.x.__set__(self, x)
        # self.__class__.y.__set__(self, y)

    @classmethod
    def from_angle(cls: type[P], angle: float, magn: float = 1.0, /) -> P:
        return cls(cos(angle) * magn, sin(angle) * magn)

    @classmethod
    def from_complex(cls: type[P], val: complex, /) -> P:
        return cls(val.real, val.imag)

    @classmethod
    def from_tuple(cls: type[P], tup: tuple[float, float], /) -> P:
        return cls(*tup)

    def __str__(self, /) -> str:
        return f'<{self.__class__.__name__}: x={self.x!r}, y={self.y!r}>'

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__}({self.x!r},{self.y!r})'

    # def __setattr__(self, attr: str, value: float | Any, /) -> None:
    #     if attr not in Point.__slots__:
    #         return super().__setattr__(attr, value)
    #     if hasattr(self, attr):
    #         raise AttributeError(attr)
    #     return getattr(self.__class__, attr).__set__(self, value)

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

    # def __getitem__(self, index: int, /) -> float:
    #     if index == 0:
    #         return self.x
    #     if index == 1:
    #         return self.y
    #     raise IndexError(index)

    # def __len__(self, /) -> int:
    #     return 2

    def __reduce__(self: P, /) -> tuple[type[P], tuple[float, float]]:
        return self.__class__, (self.x, self.y)

    def __copy__(self: P, /) -> P:
        return self

    def __deepcopy__(self: P, _: Any, /) -> P:
        return self.__copy__()

    def __complex__(self, /) -> complex:
        return self.x + self.y * 1.0j

    def __abs__(self, /) -> float:
        return self.abs()

    def __neg__(self: P, /) -> P:
        return self.__class__(-self.x, -self.y)

    def __pos__(self: P, /) -> P:
        return self

    def __invert__(self: P, /) -> P:
        return self.__class__(self.y, self.x)

    def __add__(self: P, other: Point, /) -> P:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self: P, other: Point, /) -> P:
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self: P, other: float, /) -> P:
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self: P, other: float, /) -> P:
        return self.__class__(other * self.x, other * self.y)

    def __truediv__(self: P, other: float, /) -> P:
        return self.__class__(self.x / other, self.y / other)

    def __rtruediv__(self: P, other: float, /) -> P:
        return self.__class__(other / self.x, other / self.y)

    def __matmul__(self: P, other: Point, /) -> float:
        return self.x * other.x + self.y * other.y

    def __mod__(self: P, other: float | Point, /) -> P:
        if isinstance(other, Point):
            return self.__class__(self.x % other.x, self.y % other.y)
        if isinstance(other, float):
            return self.__class__(self.x % other, self.y % other)
        return NotImplemented

    def __round__(self: P, ndigits: int = None, /) -> P:
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

    def abs(self, /) -> float:
        return (self.x ** 2.0 + self.y ** 2.0) ** 0.5

    def angle(self, /) -> float:
        return atan2(self.y, self.x)

    def norm(self: P, /) -> P:
        return self / self.abs()

    def rotate(self: P, angle: float, /) -> P:
        return self.__class__.from_angle(self.angle() + angle, self.abs())

    def angle_to(self, other: Point, /) -> float:
        return other.rotate(-self.angle()).angle()

    def dist(self, other: Point, /) -> float:
        return ((self.x - other.x) ** 2.0 + (self.y - other.y) ** 2.0) ** 0.5

    def dist2(self, other: Point, /) -> float:
        return (self.x - other.x) ** 2.0 + (self.y - other.y) ** 2.0

    def to_tuple(self, /) -> tuple[float, float]:
        return (self.x, self.y)


class MPoint(Point):
    """
    Mutable point
    """

    __slots__ = ()

    def __hash__(self, /) -> NoReturn:
        raise TypeError(f'unhashable type: {self.__class__.__name__!r}')

    # __setattr__ = object.__setattr__ # breaks mypyc
    # def __setattr__(self, attr: str, value: Any, /) -> None:
    #     return object.__setattr__(self, attr, value)

    def __iadd__(self: MP, other: Point, /) -> MP:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self: MP, other: Point, /) -> MP:
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self: MP, other: float, /) -> MP:
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self: MP, other: float, /) -> MP:
        self.x /= other
        self.y /= other
        return self

    def __imod__(self: MP, other: float | Point, /) -> MP:
        if isinstance(other, Point):
            self.x %= other.x
            self.y %= other.y
            return self
        if isinstance(other, float):
            self.x %= other
            self.y %= other
            return self
        raise TypeError

    # def __setitem__(self, index: int, value: float, /) -> None:
    #     if index == 0:
    #         self.x = value
    #     if index == 1:
    #         self.y = value
    #     raise IndexError(index)

    def __copy__(self: MP, /) -> MP:
        return self.__class__(self.x, self.y)

    def inorm(self: MP, /) -> MP:
        self /= self.abs()
        return self

    def irotate(self: MP, angle: float, /) -> MP:
        magn = self.abs()
        newang = self.angle() + angle
        self.x = cos(newang) * magn
        self.y = sin(newang) * magn
        return self


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
