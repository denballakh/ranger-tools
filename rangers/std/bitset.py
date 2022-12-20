from __future__ import annotations

from typing import (
    Iterator,
    Iterable,
    TypeVar,
    Literal,
    overload,
    NoReturn,
)

import random

__all__ = [
    'frozenbitset',
    'bitset',
]


FT = TypeVar('FT', bound='frozenbitset')
BT = TypeVar('BT', bound='bitset')
BIN = int  # only 0 or 1
ByteOrder = Literal['big', 'little']


class frozenbitset:
    __slots__ = ('_value', '_size', '_str')

    _value: int
    _size: int
    _str: str | None

    def __init__(
        self: FT, value: int = 0, /, size: int | None = None, *, _check: bool = True
    ) -> None:
        self._str = None

        if not _check:
            self._value = value
            assert size is not None
            self._size = size
            return

        if not isinstance(value, int):
            raise TypeError(f'{self.__class__.__name__} value should be int')

        if size is not None and not isinstance(size, int):
            raise TypeError(f'{self.__class__.__name__} size should be int or None')

        if value < 0:
            raise ValueError(f'{self.__class__.__name__} value should be non-negative')

        if size is not None and size < 0:
            raise ValueError(f'{self.__class__.__name__} size should be non-negative')

        if size is None:
            size = value.bit_length()
        elif value:
            value &= (1 << size) - 1  # truncating

        self._value = value
        self._size = size

    # alternative constructors
    @classmethod
    def from_bytes(
        cls: type[FT],
        value: bytes | bytearray,
        size: int | None = None,
        byteorder: ByteOrder = 'little',
    ) -> FT:
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError
        if size is None:
            size = 8 * len(value)
        return cls(
            int.from_bytes(value, byteorder),
            size=size,
        )

    @classmethod
    def from_int(cls: type[FT], value: int, size: int | None = None) -> FT:
        return cls(value, size=size)

    @classmethod
    def from_str(cls: type[FT], value: str, size: int | None = None) -> FT:
        if value.startswith('0b'):
            value = value[2:]
        if size is None:
            size = len(value)
        if value == '':
            return cls(size=size)
        return cls(
            int(value, 2),
            size=size,
            _check=False,
        )

    @classmethod
    def from_list(cls: type[FT], value: list[BIN] | tuple[BIN], size: int | None = None) -> FT:
        if not value:
            return cls(size=size)
        if size is None:
            size = len(value)

        bin_string = ''.join('1' if item else '0' for item in reversed(value))
        bin_string = ''.join(str(int(bool(item))) for item in reversed(value))
        return cls.from_str(bin_string, size=size)

    @classmethod
    def from_bitset(cls: type[FT], value: frozenbitset) -> FT:
        return cls(
            value.value,
            size=value.size,
            _check=False,
        )

    @classmethod
    def from_file(cls: type[FT], filename: str, size: int | None = None) -> FT:
        with open(filename, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data, size=size)

    @classmethod
    def from_iterable(cls: type[FT], iterable: Iterable[BIN], size: int | None = None) -> FT:
        return cls.from_list(list(iterable), size=size)

    @classmethod
    def random(cls: type[FT], size: int) -> FT:
        return cls(
            int.from_bytes(random.randbytes((size + 7) // 8), 'little'),
            size=size,
            _check=False,
        )

    def __str__(self) -> str:
        if self._str is None:
            self._str = f'{self._value:0{self._size}b}'
        return self._str

    def __repr__(self) -> str:
        if self._value == 0 and self._size == 0:
            return f'{self.__class__.__name__}()'
        if self._value == 0:
            return f'{self.__class__.__name__}(size={self._size})'
        if self._size == self._value.bit_length():
            return f'{type(self).__name__}({self._value})'
        return f'{type(self).__name__}({self._value}, size={self._size})'

    def __len__(self) -> int:
        return self._size

    # def __index__(self) -> int:
    #     return self._value

    def __int__(self) -> int:
        return self._value

    def __bytes__(self) -> bytes:
        return self._value.to_bytes(length=(self._size + 7) // 8, byteorder='big')

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __iter__(self) -> Iterator[BIN]:
        return map(int, map('1'.__eq__, str(self)[::-1]))

    def __reversed__(self) -> Iterator[BIN]:
        return map(int, map('1'.__eq__, str(self)))

    @overload
    def __getitem__(self: FT, key: int) -> BIN:
        ...

    @overload
    def __getitem__(self: FT, key: slice) -> FT:
        ...

    def __getitem__(self: FT, key: int | slice) -> BIN | FT:
        if isinstance(key, int):
            if key < 0:
                key += self._size

            if not 0 <= key < self._size:
                raise IndexError(f'Invalid {self.__class__.__name__} index: {key}')

            return self._value >> key & 1

        if isinstance(key, slice):
            if key == slice(None):
                return self.__class__(
                    self._value,
                    size=self._size,
                    _check=False,
                )

            if key.step == 1 or key.step is None:
                start, stop, step = key.indices(self._size)
                assert step == 1
                assert start >= 0
                assert stop >= start

                return self.__class__(
                    (self._value >> start) & ((1 << stop - start) - 1),
                    size=stop - start,
                    _check=False,
                )

            return self.from_str(str(self)[::-1][key][::-1])

        raise TypeError

    def __eq__(self, other: frozenbitset | int | object) -> bool:
        if isinstance(other, frozenbitset):
            return self._size == other._size and self._value == other._value

        if isinstance(other, int):
            return self._value == other

        return NotImplemented

    def __ne__(self, other: frozenbitset | int | object) -> bool:
        return not self == other

    def __invert__(self: FT) -> FT:
        return self.__class__(
            self.bit_mask ^ self._value,
            size=self._size,
            _check=False,
        )

    def __and__(self: FT, other: frozenbitset | int) -> FT:
        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value & other._value,
                size=max(self._size, other._size),
                _check=False,
            )
        if isinstance(other, int):
            return self.__class__(
                self._value & other,
                size=self._size,
                _check=False,
            )
        return NotImplemented  # type: ignore[unreachable]

    def __rand__(self: FT, other: frozenbitset | int) -> FT:
        return self & other

    def __or__(self: FT, other: frozenbitset | int) -> FT:
        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value | other._value,
                size=max(self._size, other._size),
                _check=False,
            )
        if isinstance(other, int):
            return self.__class__(
                self._value | other,
                size=self._size,
            )
        return NotImplemented  # type: ignore[unreachable]

    def __ror__(self: FT, other: frozenbitset | int) -> FT:
        return self | other

    def __xor__(self: FT, other: frozenbitset | int) -> FT:
        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value ^ other._value,
                size=max(self._size, other._size),
                _check=False,
            )
        if isinstance(other, int):
            return self.__class__(
                self._value ^ other,
                size=self._size,
            )
        return NotImplemented  # type: ignore[unreachable]

    def __rxor__(self: FT, other: frozenbitset | int) -> FT:
        return self ^ other

    def __lshift__(self: FT, other: int) -> FT:
        if isinstance(other, int):
            return self.__class__(
                self._value << other,
                size=self._size + other,
                _check=False,
            )
        return NotImplemented  # type: ignore[unreachable]

    def __rshift__(self: FT, other: int) -> FT:
        if isinstance(other, int):
            return self.__class__(
                self._value >> other,
                size=self._size - other,
                _check=False,
            )
        return NotImplemented  # type: ignore[unreachable]

    def __add__(self: FT, other: frozenbitset) -> FT:
        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value << other._size | other._value,
                size=self._size + other._size,
                _check=False,
            )
        return NotImplemented  # type: ignore[unreachable]

    def __mul__(self: FT, other: int) -> FT:
        if not isinstance(other, int):
            return NotImplemented  # type: ignore[unreachable]

        if other < 0:
            raise ValueError

        if other == 0:
            return self.__class__()

        if other == 1:
            return self.copy()

        if other == 2:
            return self + self

        a = other // 2
        b = other - a

        return (self * a) + (self * b)

    def __rmul__(self: FT, other: int) -> FT:
        return self * other

    def __mod__(self: FT, other: int) -> FT:
        if isinstance(other, int):
            return self.__class__(
                self._value & ((1 << other) - 1),
                size=other,
                _check=False,
            )
        return NotImplemented  # type: ignore[unreachable]

    @property
    def bit_mask(self) -> int:
        return (1 << self._size) - 1

    # operating on whole set
    @property
    def all(self) -> bool:
        return self._value == self.bit_mask

    @property
    def any(self) -> bool:
        return bool(self._value)

    @property
    def all_one(self) -> bool:
        return self.all

    @property
    def any_one(self) -> bool:
        return self.any

    @property
    def all_zero(self) -> bool:
        return not self.any

    @property
    def any_zero(self) -> bool:
        return not self.all

    @property
    def size(self) -> int:
        assert self._size >= 0
        assert self._value >= 0
        assert self._size >= self._value.bit_length()
        return self._size

    @property
    def value(self) -> int:
        assert self._size >= 0
        assert self._value >= 0
        assert self._size >= self._value.bit_length()
        return self._value

    def strip(self: FT) -> FT:
        return self.__class__(
            self._value,
            size=self._value.bit_length(),
            _check=False,
        )

    def copy(self: FT) -> FT:
        return self.__class__(
            self._value,
            size=self._size,
            _check=False,
        )

    __copy__ = copy
    __deepcopy__ = copy


class bitset(frozenbitset):
    __slots__ = ()

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, newsize: int) -> None:
        self._size = newsize

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, newvalue: int) -> None:
        self._value = newvalue

    def copy_from(self, other: frozenbitset) -> None:
        self._value = other.value
        self._size = other.size

    def set_all(self, value: BIN = 1) -> None:
        if value:
            self._value = self.bit_mask
        else:
            self._value = 0

    @overload
    def __setitem__(self, key: int, value: BIN) -> None:
        ...

    @overload
    def __setitem__(self, key: slice, value: BIN) -> None:
        ...

    @overload
    def __setitem__(self, key: slice, value: list[BIN] | frozenbitset) -> None:
        ...

    def __setitem__(self, key: int | slice, value: BIN | list[BIN] | frozenbitset = 1) -> None:
        self._str = None

        if isinstance(key, int):
            if key < 0:
                key += self._size

            if not 0 <= key < self._size:
                raise IndexError(f'Invalid {self.__class__.__name__} index: {key}')

            if not isinstance(value, int):
                raise TypeError

            self._value = self._value & (self.bit_mask ^ 1 << key) | (bool(value) << key)
            return

        if isinstance(key, slice):
            rng = range(*key.indices(self._size))
            if isinstance(value, int):
                if value:
                    s = 0
                    for i in rng:
                        s |= 1 << i

                    self._value |= s

                else:
                    s = 0
                    for i in rng:
                        s |= 1 << i

                    self._value &= self.bit_mask ^ s

                return

            if isinstance(value, (list, frozenbitset)):
                if len(value) != len(rng):
                    raise IndexError

                for i in rng:
                    self._value = self._value & (self.bit_mask ^ 1 << i) | (bool(value[i]) << i)

                return

        raise TypeError

    def __hash__(self) -> NoReturn:
        raise TypeError(f'unhashable type: {type(self).__name__!r}')

    def __iand__(self: BT, other: frozenbitset | int) -> BT:
        self._str = None
        if isinstance(other, frozenbitset):
            self._size = max(self._size, other._size)
            self._value &= other._value
            return self

        if isinstance(other, int):
            self._value &= other
            return self

        raise TypeError

    def __ior__(self: BT, other: frozenbitset | int) -> BT:
        self._str = None
        if isinstance(other, frozenbitset):
            self._size = max(self._size, other._size)
            self._value |= other._value
            return self

        if isinstance(other, int):
            self._value |= other
            return self

        raise TypeError

    def __ixor__(self: BT, other: frozenbitset | int) -> BT:
        self._str = None
        if isinstance(other, frozenbitset):
            self._size = max(self._size, other._size)
            self._value ^= other._value
            return self

        if isinstance(other, int):
            self._value ^= other
            return self

        raise TypeError

    def __ilshift__(self: BT, other: int) -> BT:
        self._str = None
        if isinstance(other, int):
            self._value <<= other
            self._size += other
            return self

        raise TypeError

    def __irshift__(self: BT, other: int) -> BT:
        self._str = None
        if isinstance(other, int):
            self._value >>= other
            self._size -= other
            return self

        raise TypeError

    def __iadd__(self: BT, other: frozenbitset) -> BT:
        self._str = None
        if isinstance(other, frozenbitset):
            self._value <<= other._size
            self._size += other._size
            self._value |= other._value
            return self

        raise TypeError

    def __imul__(self: BT, other: int) -> BT:
        self._str = None
        if isinstance(other, int):
            self.copy_from(self * other)
            return self

        raise TypeError

    def __imod__(self: BT, other: int) -> BT:
        self._str = None
        if isinstance(other, int):
            if other < 0:
                raise ValueError
            self._size = other
            self._value &= self.bit_mask
            return self

        raise TypeError
