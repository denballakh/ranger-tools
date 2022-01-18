from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    NoReturn,
    TypeAlias,
    TypeGuard,
    TypeVar,
    Union,
)
from types import EllipsisType

__all__ = ('GenericAlias',)


_arg: TypeAlias = Union[type, TypeVar, 'GenericAlias']
_origin: TypeAlias = type

_args: TypeAlias = tuple[_arg, ...]
_parameters: TypeAlias = tuple[TypeVar, ...]


def _is_typevar(arg: _arg) -> TypeGuard[TypeVar]:
    t = type(arg)
    if t.__name__ != 'TypeVar':
        return False
    return t.__module__ == 'typing'


def _subs_tvars(obj: _arg, params: _parameters, items: _args) -> _arg:
    if (
        (subparams := getattr(obj, '__parameters__', None)) is not None
        and isinstance(subparams, tuple)
        and subparams
    ):
        assert isinstance(obj, GenericAlias)
        subargs: list[_arg] = []

        arg: _arg | TypeVar

        for arg in subparams:
            if arg in params:
                arg = items[params.index(arg)]
            subargs.append(arg)

        obj = obj[tuple(subargs)]

    return obj


def _make_parameters(args: _args) -> _parameters:
    nargs = len(args)
    newparams: list[TypeVar] = []

    for t in args:
        if _is_typevar(t):
            if t not in newparams:
                newparams.append(t)
        else:
            if isinstance((subparams := getattr(t, '__parameters__', None)), tuple):
                for t2 in subparams:
                    if t2 not in newparams:
                        newparams.append(t2)

    return tuple(newparams)


def _subs_parameters(
    self: GenericAlias,
    args: _args,
    parameters: _parameters,
    item: _arg | _args,
) -> _args:
    n_params = len(parameters)
    if not n_params:
        raise TypeError(
            f'There are no type variables left in {self!r}',
        )
    items: _args = item if isinstance(item, tuple) else (item,)
    n_items = len(items)
    if n_items != n_params:
        raise TypeError(
            f'Too {"many" if n_items > n_params else "few"} arguments for {self!r}',
        )

    newargs: list[_arg] = []
    for arg in args:
        if _is_typevar(arg):
            arg = items[parameters.index(arg)]
        else:
            arg = _subs_tvars(arg, parameters, items)
        newargs.append(arg)

    return tuple(newargs)


def _repr_item(arg: _arg) -> str:
    if arg is ...:
        return '...'

    if hasattr(arg, '__origin__') and hasattr(arg, '__args__'):
        return repr(arg)

    if not hasattr(arg, '__qualname__') or (qualname := getattr(arg, '__qualname__')) is None:
        return repr(arg)

    if not hasattr(arg, '__module__') or (module := getattr(arg, '__module__')) is None:
        return repr(arg)

    if module == 'builtins':
        return qualname

    return f'{module!s}.{qualname!s}'


class GenericAlias:
    __origin__: _origin
    __args__: _args
    __parameters: _parameters | None

    def __init__(self, origin: _origin, args: _args) -> None:
        self.__origin__ = origin
        self.__args__ = args
        self.__parameters = None

    def __repr__(self) -> str:
        this = _repr_item(self.__origin__)
        items = '()' if not self.__args__ else ', '.join(_repr_item(arg) for arg in self.__args__)
        return f'{this!s}[{items!s}]'

    def __hash__(self) -> int:
        return hash(self.__origin__) ^ hash(self.__args__)

    def __getattribute__(self, attr: str) -> object:
        if attr in {
            '__origin__',
            '__args__',
            '_GenericAlias__parameters',  # mangled version of __parameters
            '__parameters__',
            '__mro_entries__',
            '__reduce_ex__',
            '__reduce__',
            '__copy__',
            '__deepcopy__',
        }:
            return super().__getattribute__(attr)
        return getattr(self.__origin__, attr)

    def __getitem__(self, item: _arg | _args) -> GenericAlias:
        return GenericAlias(
            self.__origin__,
            _subs_parameters(
                self,
                self.__args__,
                self.__parameters__,
                item,
            ),
        )

    def __dir__(self) -> list[str]:
        return dir(self.__origin__)

    def __call__(self, *args: object, **kwargs: object) -> object:
        obj = self.__origin__(*args, **kwargs)
        try:
            obj.__orig_class__ = self
        except (AttributeError, TypeError):
            pass
        return obj

    def __or__(self, other: object) -> Union[GenericAlias, object]:
        return Union[self, other]

    def __ror__(self, other: object) -> Union[GenericAlias, object]:
        return Union[other, self]

    @property
    def __parameters__(self) -> _parameters:
        if self.__parameters is None:
            self.__parameters = _make_parameters(self.__args__)
        return self.__parameters

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GenericAlias):
            return NotImplemented

        return (self.__origin__, self.__args__) == (other.__origin__, other.__args__)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, GenericAlias):
            return NotImplemented

        return not (self == other)

    def __mro_entries__(self, bases: Any) -> tuple[_origin]:
        return (self.__origin__,)

    def __instancecheck__(self, other: object) -> NoReturn:
        raise TypeError('isinstance() argument 2 cannot be a parameterized generic')

    def __subclasscheck__(self, other: object) -> NoReturn:
        raise TypeError('issubclass() argument 2 cannot be a parameterized generic')

    def __reduce__(self) -> tuple[type[GenericAlias], tuple[_origin, _args]]:
        return type(self), (self.__origin__, self.__args__)


if not TYPE_CHECKING and __name__ == '__main__':

    class X:
        pass

    GA = GenericAlias
    T = TypeVar('T')
    T1 = TypeVar('T1')
    T2 = TypeVar('T2')

    assert str(GA(list, (int, ...))) == 'list[int, ...]'
    assert str(GA(str, (1,))) == 'str[1]'
    assert str(GA(1, (str,))) == '1[str]'
    assert str(GA(T, (T,))) == '~T[~T]'
    assert str(GA(X, (T1, T2))) == '__main__.X[~T1, ~T2]'
    assert str(GA(dict, (T1, T1, T2, T2))[1, 2]) == 'dict[1, 1, 2, 2]'
    assert str(GA(dict, (1, list, T1, T2))[1, '<>']) == 'dict[1, list, 1, \'<>\']'

    assert str(GA(list, (int,))()) == '[]'
    assert str(GA(dict, (1, list, T1, T2))[1, '<>']()) == '{}'
    assert str(GA(object, (1, object, T1, object, T2))[1, '<>']()) != ''

    ga1 = list[int]
    ga2 = GA(list, (int,))

    assert ga1.__new__ is ga2.__new__ is list.__new__
    assert ga1.__init__ is ga2.__init__ is list.__init__
    assert ga1.__repr__ is ga2.__repr__ is list.__repr__
    assert ga1.__str__ is ga2.__str__ is list.__str__

    ga1 = tuple[int]
    ga2 = GA(tuple, (int,))

    assert ga1.__new__ is ga2.__new__ is tuple.__new__
    assert ga1() is ga2() is tuple() is [()][0]
