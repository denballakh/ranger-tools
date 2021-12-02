from __future__ import annotations
from typing import Any, Callable, Generic, NoReturn, TypeVar

from pprint import pprint

T = TypeVar('T')
CT = TypeVar('CT', bound='constmethod')
OT = TypeVar('OT', bound='usesconstmethod')


class ConstMethodError(Exception):
    pass


class const(Generic[T]):
    def __new__(cls, *args: Any, **kwargs: Any) -> NoReturn:  # type: ignore[misc]
        raise TypeError(f'const class cannot be instantiated')

    def __class_getitem__(cls, params):
        return params

def _create_instance(cls: type[T], *args, **kwargs) -> T:
    pass


class usesconstmethod:
    __slots__ = ()
    __const__: bool = False

    def __init_subclass__(cls: type) -> None:
        for attr, value in cls.__dict__.items():
            if isinstance(value, constmethod):
                setattr(cls, attr, value.__func__)
                continue

            if not callable(value):
                continue

            if isinstance(value, (classmethod,)):
                continue

            if isinstance(value, type):
                continue

            if attr not in {'__init__', '__new__'}:
                setattr(cls, attr, nonconstmethod(value))


class boundconstmethod(Generic[T]):
    def __init__(self, func: Callable[..., T], obj: usesconstmethod) -> None:
        self.__func__ = func
        self.__self__ = obj

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        func = self.__func__
        obj = self.__self__
        return func(obj, *args, **kwargs)

    def __repr__(self) -> str:
        return f'<bound constmethod {self.__self__.__class__.__name__}.{self.__func__.__name__} of <{self.__self__.__class__.__name__!r} object at {id(self.__self__)}>>'


class boundnonconstmethod(boundconstmethod[T]):
    def __call__(self, *args: Any, **kwargs: Any) -> T:
        func = self.__func__
        print(f'Calling {func!r}')
        obj = self.__self__
        if obj.__const__:
            raise ConstMethodError
        return func(obj, *args, **kwargs)


class constmethod(Generic[T]):
    __slots__ = ('__func__',)

    # __func__: Callable[..., T] # mypy bug

    def __new__(cls: type[CT], func: Callable[..., T], /) -> CT:
        return super().__new__(cls)

    def __init__(self, func: Callable[..., T], /) -> None:
        self.__func__ = func

    def __get__(self, obj: OT | None, objcls: type[OT] | None = None, /) -> Callable[..., T]:
        if obj is None:
            return self.__func__
        return boundconstmethod(self.__func__, obj)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({self.__func__!r})>'


class nonconstmethod(constmethod[T]):
    __slots__ = ()

    def __get__(self, obj: OT | None, objcls: type[OT] | None = None, /) -> Callable[..., T]:
        if obj is None:
            return self.__func__
        return boundnonconstmethod(self.__func__, obj)


class X(usesconstmethod):
    def __init__(self, value: int = 0) -> None:
        self.value = value

    @constmethod
    def add(self, value: int) -> X:
        return X(self.value + value)

    def iadd(self, value: int) -> X:
        self.value += value
        return self

    def __repr__(self) -> str:
        return f'X({self.value})'

# class Y:
#     def __new__(cls): return super().__new__(cls)
#     def __init__(self): ...
#     def __repr__(self): return super().__repr__()
#     def method(self): ...
#     @staticmethod
#     def staticmeth(): ...
#     @classmethod
#     def classmeth(cls): ...
#     @property
#     def prop(self): ...

# pprint(X.__dict__)
# pprint(Y.__dict__)
# print(Y().method)
# print(Y().staticmeth)
# print(Y().classmeth)

# x = X()
# print(x)
# x.iadd(1)
# print(x)
# y = x.add(1)
# print(y)


