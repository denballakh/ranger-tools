from __future__ import annotations
from typing import Any, Type, TypeVar, Iterable, final, Final

import sys
from abc import abstractmethod, ABC
# from functools import wraps

from ..io import Buffer

__all__ = [
    'PrintableMixin',
    'DataMixin',
    'UniqueMixin',
]

T = TypeVar('T')

class Mixin(ABC):
    __slots__ = ()


class PrintableMixin(Mixin):
    __slots__ = ()

    __repr_fmt__: str = "{typename}({kwargs})"
    __repr_sep__: tuple[str, str] = "=", ", "
    __str_fmt__: str = "<{typename}: {kwargs}>"
    __str_sep__: tuple[str, str] = "=", " "

    def __get_kwargs_strings(self) -> list[tuple[str, Any]]:
        kwarg_pairs: list[tuple[str, Any]] = []

        if (d := getattr(self, '__dict__', None)) is not None:
            for k, v in d.items():
                if not k.startswith('_'):
                    kwarg_pairs.append((k, v))

        elif (slots := getattr(self, '__slots__', None)) is not None:
            for k in slots:
                v = getattr(self, k, None)
                if not k.startswith('_'):
                    kwarg_pairs.append((k, v))

        return kwarg_pairs

    def __format(self, kwargs: list[tuple[str, Any]], fmt: str, sep: tuple[str, str]) -> str:
        return fmt.format(
            typename=type(self).__name__,
            kwargs=sep[1].join([k + sep[0] + repr(v) for k, v in kwargs]),
        )

    def __str__(self) -> str:
        return self.__format(self.__get_kwargs_strings(), self.__str_fmt__, self.__str_sep__)

    def __repr__(self) -> str:
        return self.__format(self.__get_kwargs_strings(), self.__repr_fmt__, self.__repr_sep__)


DMT = TypeVar('DMT', bound='DataMixin')
class DataMixin(Mixin):
    __slots__ = ()

    @classmethod
    @abstractmethod
    def from_buffer(cls: Type[DMT], buf: Buffer) -> DMT:
        raise NotImplementedError(f'Method {cls.__name__}.from_buffer is abstract')

    @classmethod
    def from_bytes(cls: Type[DMT], data: bytes) -> DMT:
        buf = Buffer(data)
        return cls.from_buffer(buf)

    @classmethod
    def from_file(cls: Type[DMT], path: str) -> DMT:
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    @abstractmethod
    def to_buffer(self: DMT, buf: Buffer):
        raise NotImplementedError(f'Method {type(self).__name__}.to_buffer is abstract.')

    def to_bytes(self: DMT) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return buf.to_bytes()

    def to_file(self: DMT, path: str) -> None:
        with open(path, 'wb') as file:
            file.write(self.to_bytes())


class UniqueMixin(Mixin):
    __slots__ = ()

    def __eq__(self, other) -> bool:
        if isinstance(other, UniqueMixin):
            return self is other
        return NotImplemented

    def __ne__(self, other) -> bool:
        if isinstance(other, UniqueMixin):
            return self is not other
        return NotImplemented

    def __hash__(self) -> int:
        return id(self)


class InPlaceModMixin(Mixin):
    __slots__ = ()

    @abstractmethod
    def update_inplace(self, other):
        raise NotImplementedError(f'Method {type(self).__name__}.update_inplace is abstract.')

    def __imatmul__(self, other):
        self.update_inplace(other)
        return self


class IterableStream:
    def __init__(self) -> None:
        self.data: list[Any] = []

    def __lshift__(self, other: Iterable | Any):
        if hasattr(other, '__iter__'):
            self.data.extend(list(other))
        else:
            self.data.append(other)
        return self


class ImmutableMixin(Mixin):
    @final
    def __setattr__(self, name: str, value: Any) -> None: raise TypeError
    @final
    def __delattr__(self, name: str) -> None: raise TypeError

    @final
    def __setitem__(self, index: Any, value: Any) -> None: raise TypeError
    @final
    def __delitem__(self, index: Any) -> None: raise TypeError

    @final
    def __iadd__(self, other: Any) -> Any: return self + other
    @final
    def __isub__(self, other: Any) -> Any: return self - other
    @final
    def __imul__(self, other: Any) -> Any: return self * other
    @final
    def __imod__(self, other: Any) -> Any: return self % other
    @final
    def __ifloordiv__(self, other: Any) -> Any: return self // other
    @final
    def __itruediv__(self, other: Any) -> Any: return self / other
    @final
    def __ipow__(self, other: Any) -> Any: return self ** other
    @final
    def __imatmul__(self, other: Any) -> Any: return self @ other

    @final
    def __iand__(self, other: Any) -> Any: return self & other
    @final
    def __ior__(self, other: Any) -> Any: return self | other
    @final
    def __ixor__(self, other: Any) -> Any: return self ^ other
    @final
    def __ilshift__(self, other: Any) -> Any: return self << other
    @final
    def __irshift__(self, other: Any) -> Any: return self >> other


class OptimizedImmutableMixin(Mixin):
    __slots__ = ()

    @abstractmethod
    def update_inplace(self: T, other: T) -> None:
        pass

    @abstractmethod
    def copy(self: T) -> T:
        pass

    def __imatmul__(self, other):
        # print(sys.getrefcount(self))
        if sys.getrefcount(self) == 4:
            obj = self
            # print('+ ok')
        else:
            obj = type(self)(self) # copying
            # print('- copying')
        obj.update_inplace(other)
        return obj

