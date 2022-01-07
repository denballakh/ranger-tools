from __future__ import annotations

from typing import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    NoReturn,
    TypeVar,
    Generic,
    Hashable,
    overload,
)

from types import MappingProxyType
from _collections_abc import (
    dict_keys,
    dict_values,
    dict_items,
)

from .sentinel import sentinel, SentinelType

__all__ = ('bidict',)

A = TypeVar('A', bound=Hashable)
B = TypeVar('B', bound=Hashable)
T = TypeVar('T')


def _inv_dict(_dict: dict[A, B], /) -> dict[B, A]:
    inversed = dict[B, A]()

    for key, value in _dict.items():
        if value in inversed:
            raise ValueError(f'value {value!r} repeats at key {inversed[value]!r} and {key!r}')

        inversed[value] = key

    return inversed


class bidict(Generic[A, B]):
    __slots__ = '_dict', '_inv'

    _dict: dict[A, B]
    _inv: bidict[B, A]

    def __init__(
        self,
        _dict: dict[A, B] | None = None,
        /,
        *,
        _inv: bidict[B, A] | None = None,
    ) -> None:
        self._dict = {} if _dict is None else _dict
        self._inv = bidict(_inv_dict(self._dict), _inv=self) if _inv is None else _inv

    @classmethod
    def from_mapping(cls, mapping: Mapping[A, B]) -> bidict[A, B]:
        return cls(dict(mapping))

    def __str__(self, /) -> str:
        return (
            f'<{type(self).__name__!s}'
            + (
                f': {content!s}'
                if (
                    content := ', '.join(f'{key!r}->{value!r}' for key, value in self._dict.items())
                )
                else ''
            )
            + '>'
        )

    def __repr__(self) -> str:
        return f'{type(self).__name__!s}({repr(self._dict) if self._dict else str()})'

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> Iterator[A]:
        return iter(self._dict)

    def __reversed__(self) -> Iterator[A]:
        return reversed(self._dict)

    def __contains__(self, value: object) -> bool:
        return value in self._dict

    def __hash__(self) -> NoReturn:
        raise TypeError(f'unhashable type: {type(self).__name__!r}')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, bidict):
            return self._dict == other._dict and self._inv._dict == other._inv._dict

        if isinstance(other, dict):
            return self._dict == other

        return NotImplemented

    def __setitem__(self, key: A, value: B, /) -> None:
        inv = self._inv

        del self[key]
        del inv[value]

        self._dict[key] = value
        inv._dict[value] = key

    def __getitem__(self, key: A, /) -> B:
        return self._dict[key]

    def __delitem__(self, key: A, /) -> None:
        if key in (d := self._dict):
            del self._inv._dict[d[key]]
            del d[key]

    def __or__(self, other: Mapping[A, B], /) -> bidict[A, B]:
        new = self.copy()
        new |= other
        return new

    def __ror__(self, other: Mapping[A, B], /) -> bidict[A, B]:
        return self | other

    def __ior__(self, other: Mapping[A, B], /) -> bidict[A, B]:
        for key, value in other.items():
            self[key] = value
        return self

    @property
    def inv(self) -> bidict[B, A]:
        return self._inv

    @property
    def proxy(self) -> MappingProxyType[A, B]:
        return MappingProxyType(self._dict)

    def clear(self) -> None:
        self._dict.clear()
        self._inv._dict.clear()

    def copy(self) -> bidict[A, B]:
        d1 = self._dict.copy()
        d2 = self._inv._dict.copy()

        new: bidict[A, B] = bidict(d1, _inv=self._inv)
        inv: bidict[B, A] = bidict(d2, _inv=new)
        new._inv = inv

        return new

    __copy__ = copy
    __deepcopy__ = copy  # FIXME

    # fmt: off
    @overload
    def pop(self, key: A, /) -> B: ...
    @overload
    def pop(self, key: A, default: B, /) -> B: ...
    # fmt: on
    def pop(
        self,
        key: A,
        default: B | SentinelType = sentinel,
        /,
    ) -> B:
        if default is sentinel:
            b = self._dict.pop(key)
            self._inv._dict.pop(b)

        else:
            b = self._dict.pop(key, default)
            self._inv._dict.pop(b, key)

        return b

    def popitem(self) -> tuple[A, B]:
        a, b = self._dict.popitem()
        del self._inv._dict[b]
        return a, b

    def setdefault(self, key: A, default: B, /) -> B:
        if key not in self._dict:
            self[key] = default
        return self._dict[key]

    def update(self, mapping: Mapping[A, B], /) -> None:
        for key, value in mapping.items():
            self[key] = value

    def keys(self) -> dict_keys[A, B]:
        return self._dict.keys()

    def values(self) -> dict_values[A, B]:
        return self._dict.values()

    def items(self) -> dict_items[A, B]:
        return self._dict.items()

    # fmt: off
    @overload
    def get(self, key: A, /) -> B | None: ...
    @overload
    def get(self, key: A, default: B, /) -> B: ...
    # fmt: on
    def get(self, key: A, default: B | None = None, /) -> B | None:
        if key in self._dict:
            return self._dict[key]
        return default
