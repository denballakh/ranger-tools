from __future__ import annotations
from types import FunctionType, MethodType

# from types import GenericAlias
from typing import Any, Callable, Generic, NoReturn, TypeVar

from pprint import pprint

T = TypeVar('T')
CT = TypeVar('CT', bound='constmethod')
OT = TypeVar('OT', bound='usesconstmethod')


class ConstMethodError(TypeError):
    pass


class const:
    __origin__: type[usesconstmethod]

    @classmethod
    def __class_getitem__(cls, origin: type[usesconstmethod]) -> const:
        return cls(origin)

    def __init__(self, origin: type[usesconstmethod]) -> None:
        self.__origin__ = origin

    def __repr__(self) -> str:
        return f'const[{self.__origin__!r}]'

    def __hash__(self) -> int:
        return hash((type(self), self.__origin__))

    def __getattribute__(self, attr: str) -> object:
        if attr in {
            '__origin__',
        }:
            return super().__getattribute__(attr)
        return getattr(self.__origin__, attr)

    def __dir__(self) -> list[str]:
        return dir(self.__origin__)

    def __call__(self, *args: object, **kwargs: object) -> object:
        obj = self.__origin__(*args, **kwargs)
        obj.__const__ = True
        return obj

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, const):
            return NotImplemented

        return self.__origin__ == other.__origin__

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, const):
            return NotImplemented

        return not (self == other)

    def __mro_entries__(self, bases: Any) -> NoReturn:
        raise TypeError

    def __instancecheck__(self, other: object) -> bool:
        if isinstance(other, self.__origin__):
            return getattr(other, '__const__', False)
        return NotImplemented

    def __subclasscheck__(self, other: object) -> bool:
        if isinstance(other, const):
            return issubclass(other.__origin__, self.__origin__)
        return NotImplemented


class usesconstmethod:
    __slots__ = ('__const__',)

    __const__: bool

    def __init_subclass__(cls: type) -> None:
        for attr, value in cls.__dict__.items():
            if isinstance(value, constmethod) and not isinstance(value, nonconstmethod):
                setattr(cls, attr, value.__func__)
                continue

            if not callable(value):
                continue

            if isinstance(value, (classmethod,)):
                continue

            if isinstance(value, type):
                continue

            if attr not in {'__init__', '__new__', '__mro_entries__'}:
                setattr(cls, attr, nonconstmethod(value))


class constmethod:
    __slots__ = ('__func__',)

    # __func__: FunctionType

    def __init__(self, func: FunctionType, /) -> None:
        self.__func__ = func

    def __get__(
        self, obj: OT | None, objcls: type[OT] | None = None, /
    ) -> MethodType | FunctionType:
        return self.__func__.__get__(obj, objcls)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({self.__func__!r})>'


class nonconstmethod(constmethod):
    __slots__ = ()

    def __get__(
        self, obj: OT | None, objcls: type[OT] | None = None, /
    ) -> MethodType | FunctionType:
        if obj is None:
            return self.__func__.__get__(None, objcls)

        if getattr(obj, '__const__', False):
            raise ConstMethodError(
                f'Cannot get non-const method {self.__func__.__name__} of const object {obj}'
            )

        return self.__func__.__get__(obj, objcls)


if __name__ == '__main__':

    class Y:
        def __new__(cls):
            return super().__new__(cls)

        def __init__(self):
            ...

        def __repr__(self):
            return super().__repr__()

        def method(self):
            ...

        @staticmethod
        def staticmeth():
            ...

        @classmethod
        def classmeth(cls):
            ...

        @property
        def prop(self):
            ...

    class X(usesconstmethod):
        def __init__(self, value: int) -> None:
            self.value = value

        @constmethod
        def __str__(self) -> str:
            return f'<X: {self.value}>'

        @classmethod
        def from_int(cls, value: int) -> X:
            return cls(value)

        @constmethod
        def __repr__(self) -> str:
            return f'X({self.value})'

        @constmethod
        def __add__(self, other: X) -> X:
            return X(self.value + other.value)

        def __iadd__(self, other: X) -> X:
            self.value += other.value
            return self

    x = X(0)
    print(x)
    print(x + X(1))
    x += X(2)
    print(x)

    x = const[X](0)
    assert isinstance(x, X)
    assert isinstance(x, const[X])
    assert not isinstance(x, const)
    assert not issubclass(X, const)
    assert issubclass(const[X], const[X])
    assert issubclass(X, const[X])
    assert not issubclass(const[X], X)
    print(x)
    print(x + X(1))
    try:
        x += X(2)  # should raise because x in const
    except:
        pass
    else:
        raise ConstMethodError
    print(x)

    x = X.from_int(1)
    print(x)
    print(x + X(1))
    x += X(2)
    print(x)

    x = const[X].from_int(1)
    print(x)
    print(x + X(1))
    # try:
    #     x += X(2)  # should raise because x in const
    # except:
    #     pass
    # else:
    #     raise ConstMethodError
    print(x)

    # pprint(GenericAlias.__dict__)
    # pprint(X.__dict__)
    # pprint(Y.__dict__)
    # print(Y().method)
    # print(Y().staticmeth)
    # print(Y().classmeth)

    # alias = const[X]
    # print(alias)
