from __future__ import annotations

from typing import (
    Iterator,
    Iterable,
    TypeVar,
    Literal,
    overload,
    Any,
    NoReturn,
    # TYPE_CHECKING,
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

# def coerce_types(cls1: type[_T1], cls2: type[_T2]) -> type[_T1] | type[_T2]:
#     if cls1 is cls2:
#         return cls1
#     if issubclass(cls1, cls2):
#         return cls1
#     if issubclass(cls2, cls1):
#         return cls2
#     raise TypeError


class frozenbitset:
    __slots__ = ('_value', '_size')

    _value: int
    _size: int

    def __init__(self: FT, value: int = 0, /, size: int = None) -> None:
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
        else:
            value &= (1 << size) - 1  # truncating

        self._value = value
        self._size = size

    # alternative constructors
    @classmethod
    def from_bytes(
        cls: type[FT], value: bytes | bytearray, size: int = None, byteorder: ByteOrder = 'little'
    ) -> FT:
        """!
        >>> frozenbitset.from_bytes(b'')
        frozenbitset()
        >>> frozenbitset.from_bytes(b'\\0')
        frozenbitset(size=8)
        >>> frozenbitset.from_bytes(b'\\xff')
        frozenbitset(255)
        >>> frozenbitset.from_bytes(b'\\0\\0')
        frozenbitset(size=16)
        >>> frozenbitset.from_bytes(b'\\1\\0')
        frozenbitset(1, size=16)
        >>> frozenbitset.from_bytes(b'0')
        frozenbitset(48, size=8)
        """

        if not isinstance(value, (bytes, bytearray)):
            raise TypeError

        if size is None:
            size = 8 * len(value)

        return cls(int.from_bytes(value, byteorder), size=size)

    @classmethod
    def from_int(cls: type[FT], value: int, size: int = None) -> FT:
        return cls(value, size=size)

    @classmethod
    def from_str(cls: type[FT], value: str, size: int = None) -> FT:
        """!
        >>> frozenbitset.from_str('')
        frozenbitset()
        >>> frozenbitset.from_str('0')
        frozenbitset(size=1)
        >>> frozenbitset.from_str('1')
        frozenbitset(1)
        >>> frozenbitset.from_str('1000')
        frozenbitset(8)
        >>> frozenbitset.from_str('111', size=5)
        frozenbitset(7, size=5)
        """

        if value.startswith('0b'):
            value = value[2:]

        if size is None:
            size = len(value)

        if value == '':
            value = '0'

        return cls(int(value, 2), size=size)

    @classmethod
    def from_list(cls: type[FT], value: list[BIN] | tuple[BIN], size: int = None) -> FT:
        """!
        >>> frozenbitset.from_list([])
        frozenbitset()
        >>> frozenbitset.from_list([], size=3)
        frozenbitset(size=3)
        >>> frozenbitset.from_list([0])
        frozenbitset(size=1)
        >>> frozenbitset.from_list([1])
        frozenbitset(1)
        >>> frozenbitset.from_list([1, 0, 0, 0])
        frozenbitset(1, size=4)
        >>> frozenbitset.from_list([0, 0, 0, 1])
        frozenbitset(8)
        """

        if not value:
            return cls(size=size)

        bin_string = ''.join('1' if item else '0' for item in reversed(value))
        return cls.from_str(bin_string, size=size)

    @classmethod
    def from_bitset(cls: type[FT], value: frozenbitset) -> FT:
        """!
        >>> frozenbitset.from_bitset(frozenbitset())
        frozenbitset()
        >>> frozenbitset.from_bitset(frozenbitset(9, size=7))
        frozenbitset(9, size=7)
        """

        return cls(value.value, size=value.size)

    @classmethod
    def from_file(cls: type[FT], filename: str, size: int = None) -> FT:
        with open(filename, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data, size=size)

    @classmethod
    def from_iterable(cls: type[FT], iterable: Iterable[BIN], size: int = None) -> FT:
        """!
        >>> frozenbitset.from_iterable(iter([0, 0, 1, 0]))
        frozenbitset(4, size=4)
        """

        return cls.from_list(list(iterable), size=size)

    @classmethod
    def random(cls: type[FT], size: int) -> FT:
        return cls(
            int.from_bytes(random.randbytes((size + 7) // 8), 'little') & ((1 << size) - 1),
            size=size,
        )

    def __str__(self) -> str:
        """!
        >>> print(frozenbitset())
        0
        >>> print(frozenbitset(size=10))
        0000000000
        >>> print(frozenbitset(size=0))
        0
        >>> print(frozenbitset(14))
        1110
        >>> print(frozenbitset(14, size=6))
        001110
        >>> print(frozenbitset(1024))
        10000000000
        >>> print(frozenbitset(1024, size=7))
        0000000
        """

        return f'{self._value:0{self._size}b}'

    def __repr__(self) -> str:
        """!
        >>> frozenbitset()
        frozenbitset()
        >>> frozenbitset(0)
        frozenbitset()
        >>> frozenbitset(0, size=0)
        frozenbitset()
        >>> frozenbitset(7)
        frozenbitset(7)
        >>> frozenbitset(256)
        frozenbitset(256)
        >>> frozenbitset(256, size=20)
        frozenbitset(256, size=20)
        """

        if self._value == 0 and self._size == 0:
            return f'{self.__class__.__name__}()'
        if self._value == 0:
            return f'{self.__class__.__name__}(size={self._size})'
        if self._size == self._value.bit_length():
            return f'{type(self).__name__}({self._value})'
        return f'{type(self).__name__}({self._value}, size={self._size})'

    def __len__(self) -> int:
        """!
        >>> len(frozenbitset())
        0
        >>> len(frozenbitset(size=10))
        10
        >>> len(frozenbitset(7))
        3
        """
        return self._size

    def __index__(self) -> int:
        return self._value

    def __int__(self) -> int:
        """!
        >>> int(frozenbitset(7))
        7
        >>> int(frozenbitset())
        0
        >>> int(frozenbitset(10, size=3))
        2
        """
        return self._value

    def __bytes__(self) -> bytes:
        """!
        >>> bytes(frozenbitset())
        b''
        >>> bytes(frozenbitset(255))
        b'\\xff'
        >>> bytes(frozenbitset(size=64))
        b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        >>> bytes(frozenbitset(size=15))
        b'\\x00\\x00'
        >>> bytes(frozenbitset(1, size=15))
        b'\\x00\\x01'
        """
        return self._value.to_bytes(length=(self._size + 7) // 8, byteorder='big')

    def __hash__(self) -> int:
        """!
        >>> hash(frozenbitset()) == hash(('frozenbitset', 0, 0))
        True
        >>> _ = hash(frozenbitset())
        >>> hash(bitset())
        Traceback (most recent call last):
          ...
        TypeError: unhashable type: 'bitset'
        """
        return hash((self.__class__.__name__, self._size, self._value))

    def __bool__(self) -> bool:
        """!
        >>> bool(frozenbitset())
        False
        >>> bool(frozenbitset(1))
        True
        >>> bool(frozenbitset(size=10))
        False
        """
        return bool(self._value)

    def __iter__(self) -> Iterator[BIN]:
        """!
        >>> list(frozenbitset(7))
        [1, 1, 1]
        >>> list(frozenbitset(8))
        [0, 0, 0, 1]
        >>> list(frozenbitset(10, size=5))
        [0, 1, 0, 1, 0]
        """
        # for key in range(self._size):
            # yield self[key]
        s = str(self)[::-1]
        lc = list(s)
        li = [int(c) for c in lc]
        return iter(li)

    def __reversed__(self) -> Iterator[BIN]:
        """!
        >>> list(reversed(frozenbitset(8)))
        [1, 0, 0, 0]
        """
        return iter(self[::-1])

    @overload
    def __getitem__(self: FT, key: int) -> BIN:
        ...

    @overload
    def __getitem__(self: FT, key: slice) -> FT:
        ...

    def __getitem__(self: FT, key: int | slice) -> BIN | FT:
        """!
        >>> frozenbitset(8)[0]
        0
        >>> frozenbitset(8)[3]
        1
        >>> frozenbitset(8)[-1]
        1
        >>> frozenbitset()[0]
        Traceback (most recent call last):
          ...
        IndexError: Invalid bitset index: 0
        >>> frozenbitset()[::]
        frozenbitset()
        >>> frozenbitset(8)[::-1]
        frozenbitset(1, size=4)
        >>> frozenbitset(10)[::2]
        frozenbitset(size=2)
        """

        if isinstance(key, int):
            if key < 0:
                key += self._size

            if not 0 <= key < self._size:
                raise IndexError(f'Invalid bitset index: {key}')

            return self._value >> key & 1

        if isinstance(key, slice):
            if key == slice(None):
                return self.__class__(self._value, size=self._size)

            return self.from_str(str(self)[::-1][key][::-1])

            # rng = range(*key.indices(self._size))
            # return self.from_list([(self._value >> i & 1) for i in rng], size=len(rng))

        raise TypeError

    def __eq__(self, other: frozenbitset | int | tuple | Any) -> bool:
        """!
        >>> frozenbitset() == frozenbitset()
        True
        >>> frozenbitset() == frozenbitset(size = 1)
        False
        >>> frozenbitset() == bitset()
        True
        >>> frozenbitset() == 0
        True
        >>> frozenbitset() == (0, 0)
        True
        """

        if isinstance(other, frozenbitset):
            return self._size == other._size and self._value == other._value
        if isinstance(other, int):
            return self._value == other
        if isinstance(other, tuple):
            return (self._value, self._size) == other
        return NotImplemented

    def __invert__(self: FT) -> FT:
        """!
        >>> ~frozenbitset()
        frozenbitset()
        >>> ~frozenbitset(8)
        frozenbitset(7, size=4)
        """
        return self.from_int(self.bit_mask ^ self._value, size=self._size)

    def __and__(self: FT, other: frozenbitset | int) -> FT:
        """!
        >>> frozenbitset() & frozenbitset()
        frozenbitset()
        >>> frozenbitset() & 1
        frozenbitset()
        >>> frozenbitset(8) & 8
        frozenbitset(8)
        >>> frozenbitset(10) & ~frozenbitset(10)
        frozenbitset(size=4)
        >>> frozenbitset(10) & frozenbitset(10)
        frozenbitset(10)
        """

        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value & other._value,
                size=max(self._size, other._size),
            )

        if isinstance(other, int):
            return self.__class__(self._value & other, size=self._size)

        return NotImplemented

    def __rand__(self: FT, other: frozenbitset | int) -> FT:
        """!
        >>> 8 & frozenbitset(8)
        frozenbitset(8)
        >>> 0 & frozenbitset(8)
        frozenbitset(size=4)
        """
        return self & other

    def __or__(self: FT, other: frozenbitset | int) -> FT:
        """!
        >>> frozenbitset() | frozenbitset()
        frozenbitset()
        >>> frozenbitset() | 1
        frozenbitset()
        >>> frozenbitset(8) | 8
        frozenbitset(8)
        >>> frozenbitset(10) | ~frozenbitset(10)
        frozenbitset(15)
        >>> frozenbitset(10) | frozenbitset(10)
        frozenbitset(10)
        """

        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value | other._value,
                size=max(self._size, other._size),
            )
        if isinstance(other, int):
            return self.__class__(self._value | other, size=self._size)
        return NotImplemented

    def __ror__(self: FT, other: frozenbitset | int) -> FT:
        """!
        >>> 8 | frozenbitset(8)
        frozenbitset(8)
        >>> 0 | frozenbitset(8)
        frozenbitset(8)
        """
        return self | other

    def __xor__(self: FT, other: frozenbitset | int) -> FT:
        """!
        >>> frozenbitset() ^ frozenbitset()
        frozenbitset()
        >>> frozenbitset() ^ 1
        frozenbitset()
        >>> frozenbitset(8) ^ 8
        frozenbitset(size=4)
        >>> frozenbitset(10) ^ ~frozenbitset(10)
        frozenbitset(15)
        >>> frozenbitset(10) ^ frozenbitset(10)
        frozenbitset(size=4)
        """

        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value ^ other._value,
                size=max(self._size, other._size),
            )

        if isinstance(other, int):
            return self.__class__(self._value ^ other, size=self._size)

        return NotImplemented

    def __rxor__(self: FT, other: frozenbitset | int) -> FT:
        """!
        >>> 8 ^ frozenbitset(8)
        frozenbitset(size=4)
        >>> 0 ^ frozenbitset(8)
        frozenbitset(8)
        """
        return self ^ other

    def __lshift__(self: FT, other: int) -> FT:
        """!
        >>> frozenbitset() << 5
        frozenbitset(size=5)
        >>> frozenbitset(1) << 5
        frozenbitset(32)
        >>> frozenbitset() << 0
        frozenbitset()
        """
        if isinstance(other, int):
            return self.__class__(self._value << other, size=self._size + other)
        return NotImplemented

    def __rshift__(self: FT, other: int) -> FT:
        """!
        >>> frozenbitset(1) >> 1
        frozenbitset()
        >>> frozenbitset(8) >> 3
        frozenbitset(1)
        """
        if isinstance(other, int):
            return self.__class__(self._value >> other, size=self._size - other)
        return NotImplemented

    def __add__(self: FT, other: frozenbitset) -> FT:
        """!
        >>> frozenbitset() + frozenbitset()
        frozenbitset()
        >>> frozenbitset(8) +  frozenbitset(7)
        frozenbitset(71)
        >>> (8 << 3) + 7
        71
        """
        if isinstance(other, frozenbitset):
            return self.__class__(
                self._value << other._size | other._value, size=self._size + other._size
            )
        return NotImplemented

    def __mul__(self: FT, other: int) -> FT:
        """!
        >>> frozenbitset(7) * 2
        frozenbitset(63)
        >>> frozenbitset(2) * 2
        frozenbitset(10)
        """
        if isinstance(other, int):
            return self.from_list(list[BIN](self) * other)
        return NotImplemented

    def __rmul__(self: FT, other: int) -> FT:
        """!
        >>> 2 * frozenbitset(7)
        frozenbitset(63)
        >>> 2 * frozenbitset(2)
        frozenbitset(10)
        """
        return self * other

    def __mod__(self: FT, other: int) -> FT:
        """!
        >>> frozenbitset(7) % 1
        frozenbitset(1)
        >>> frozenbitset(8) % 3
        frozenbitset(size=3)
        >>> frozenbitset(10) % 2
        frozenbitset(2)
        >>> frozenbitset() % 10
        frozenbitset(size=10)
        >>> frozenbitset(1) % 10
        frozenbitset(1, size=10)
        """
        if isinstance(other, int):
            return self.__class__(self._value & ((1 << other) - 1), size=other)
        return NotImplemented

    @property
    def bit_mask(self) -> int:
        """!
        >>> frozenbitset().bit_mask
        0
        >>> frozenbitset(1).bit_mask
        1
        >>> frozenbitset(2).bit_mask
        3
        >>> frozenbitset(8).bit_mask
        15
        """
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
        assert self._size >= self._value.bit_length()
        return self._size

    @property
    def value(self) -> int:
        assert self._value >= 0
        assert self._size >= self._value.bit_length()
        return self._value

    def strip(self: FT) -> FT:
        return self.__class__(self._value)


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
            self._value = 1 << self._size - 1
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
        """!
        >>> x = bitset(7); x
        bitset(7)
        >>> x[0] = 0; x
        bitset(6)
        >>> x[-1] = 0; x
        bitset(2, size=3)
        >>> y = bitset(10); y
        bitset(10)
        >>> y[0] = 1; y[1] = 0; y
        bitset(9)
        >>> y[-1] = 0; y
        bitset(1, size=4)
        >>> y[::] = 1; y
        bitset(15)
        """
        if isinstance(key, int):
            if key < 0:
                key += self._size
            if not 0 <= key < self._size:
                raise IndexError(f'Invalid bitset index: {key}')
            if not isinstance(value, int):
                raise TypeError
            self._value = self._value & (self.bit_mask ^ 1 << key) | (bool(value) << key)
            return

        if isinstance(key, slice):
            rng = range(*key.indices(self._size))

            if isinstance(value, int):
                if value:
                    for i in rng:
                        self._value |= 1 << i
                else:
                    s = 0
                    for i in rng:
                        s |= 1 << i
                    self._value &= self.bit_mask - s

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
        """!
        >>> x = bitset(0b100111100101); print(x)
        100111100101
        >>> x &= 0; print(x)
        000000000000
        >>> x = bitset( 0b00111100101)
        >>> y = bitset(0b101010101001)
        >>> x &= y; print(x)
        000010100001
        """
        if isinstance(other, int):
            self._value &= other
            return self

        if isinstance(other, frozenbitset):
            self._size = max(self._size, other._size)
            self._value &= other._value
            return self

        raise TypeError

    def __ior__(self: BT, other: frozenbitset | int) -> BT:
        if isinstance(other, int):
            self._value |= other
            return self

        if isinstance(other, frozenbitset):
            self._size = max(self._size, other._size)
            self._value |= other._value
            return self

        raise TypeError

    def __ixor__(self: BT, other: frozenbitset | int) -> BT:
        if isinstance(other, int):
            self._value ^= other
            return self

        if isinstance(other, frozenbitset):
            self._size = max(self._size, other._size)
            self._value ^= other._value
            return self

        raise TypeError

    def __ilshift__(self: BT, other: int) -> BT:
        return self << other

    def __irshift__(self: BT, other: int) -> BT:
        return self >> other

    def __iadd__(self: BT, other: frozenbitset) -> BT:
        if isinstance(other, frozenbitset):
            self._size += other._size
            self._value <<= other._size
            self._value |= other._value
            return self
        raise TypeError

    def __imul__(self: BT, other: int) -> BT:
        if isinstance(other, int):
            b = self + bitset()
            for i in range(other):
                self += b
            return self
        raise TypeError

    def __imod__(self: BT, other: int) -> BT:
        if isinstance(other, int):
            if other < 0:
                raise ValueError
            self._size = other
            self._value &= self.bit_mask
            return self
        raise TypeError


# if TYPE_CHECKING:
#     # reveal_type(frozenbitset.__add__)
#     # reveal_type(bitset.__iadd__)

#     reveal_type(bitset.from_list([]))
#     reveal_type(frozenbitset.from_list([]))

#     reveal_type(bitset() + bitset())
#     reveal_type(bitset() + frozenbitset())
#     reveal_type(frozenbitset() + bitset())
#     reveal_type(frozenbitset() + frozenbitset())

#     reveal_type(bitset() & bitset())
#     reveal_type(bitset() & frozenbitset())
#     reveal_type(frozenbitset() & bitset())
#     reveal_type(frozenbitset() & frozenbitset())


def test_speed():
    from rangers.std.context_managers import TimeMeasure, Timer

    size = 1000000
    size8 = size // 8
    size2 = size // 2

    print(f'size = {size}')
    print()

    with TimeMeasure('bitset(size=size): %s', cnt=10**4):
        for _ in range(10 ** 4):
            _ = bitset(size=size)

    with TimeMeasure('~bitset(size=size): %s', cnt=10**3):
        for _ in range(10 ** 3):
            _ = ~bitset(size=size)


    with TimeMeasure('[0]*size: %s', cnt=10**2):
        for _ in range(10 ** 2):
            _ = [0] * size

    with TimeMeasure('bytes(size8): %s', cnt=10**5):
        for _ in range(10 ** 5):
            _ = bytes(size8)
            # _ = bytearray(size8)


    b = bitset.random(size)
    l = list(b)

    print()

    with TimeMeasure('list(b): %s'):
        list(b)

    with TimeMeasure('bitset.from_list(l): %s'):
        bitset.from_list(l)

    print()

    with TimeMeasure('b[size2]: %s', cnt=10**4):
        for _ in range(10 ** 4):
            _ = b[size2]


    with TimeMeasure('l[i]: %s', cnt=10**7):
        i = size // 2
        for _ in range(10 ** 7):
            _ = l[i]


    print()

    with TimeMeasure('b[::]: %s', cnt=10**3):
        for _ in range(10 ** 3):
            _ = b[::]


    with TimeMeasure('l[::]: %s', cnt=10**3):
        for _ in range(10 ** 3):
            _ = l[::]

    print()

    with TimeMeasure('b[::-1]: %s', cnt=10**3):
        for _ in range(10 ** 3):
            _ = b[::-1]


    with TimeMeasure('l[::-1]: %s', cnt=10**3):
        for _ in range(10 ** 3):
            _ = l[::-1]

    print()

if __name__ == '__main__':
    import doctest
    import os

    res = doctest.testmod(optionflags=doctest.ELLIPSIS)
    if res.failed == 0:
        test_speed()

    input('Press enter to exit...')
    os._exit(res.failed)
