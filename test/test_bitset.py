from __future__ import annotations
from typing import TYPE_CHECKING

from itertools import repeat
import unittest
import time
from hashlib import md5, sha256
import random
from struct import Struct, calcsize, pack, unpack

from rangers.std.time import AdaptiveTimeMeasurer
from rangers.std.bitset import frozenbitset, bitset

COMPILED = frozenbitset.__init__.__class__.__name__ != 'function'

if TYPE_CHECKING:
    # reveal_type(frozenbitset.__add__)
    # reveal_type(bitset.__iadd__)

    reveal_type(bitset.from_list([]))
    reveal_type(frozenbitset.from_list([]))

    reveal_type(bitset() + bitset())
    reveal_type(bitset() + frozenbitset())
    reveal_type(frozenbitset() + bitset())
    reveal_type(frozenbitset() + frozenbitset())

    reveal_type(bitset() & bitset())
    reveal_type(bitset() & frozenbitset())
    reveal_type(frozenbitset() & bitset())
    reveal_type(frozenbitset() & frozenbitset())


def test_doc():
    """!

    Constructing:
    .from_bytes()
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

    .from_str()
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

    .from_list():
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

    .from_bitset():
    >>> frozenbitset.from_bitset(frozenbitset())
    frozenbitset()
    >>> frozenbitset.from_bitset(frozenbitset(9, size=7))
    frozenbitset(9, size=7)
    >>> frozenbitset.from_iterable(iter([0, 0, 1, 0]))
    frozenbitset(4, size=4)

    str():
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

    repr():
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

    len():
    >>> len(frozenbitset())
    0
    >>> len(frozenbitset(size=10))
    10
    >>> len(frozenbitset(7))
    3
    >>> int(frozenbitset(7))
    7
    >>> int(frozenbitset())
    0
    >>> int(frozenbitset(10, size=3))
    2

    bytes():
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

    >>> bytearray(frozenbitset())
    bytearray(b'\\x00')
    >>> bytearray(bitset())
    bytearray(b'\\x00')

    hash():
    # >>> hash(frozenbitset()) == hash(('frozenbitset', 0, 0))
    # True
    >>> _ = hash(frozenbitset())
    >>> hash(bitset())
    Traceback (most recent call last):
      ...
    TypeError: unhashable type: 'bitset'

    bool():
    >>> bool(frozenbitset())
    False
    >>> bool(frozenbitset(1))
    True
    >>> bool(frozenbitset(size=10))
    False

    list():
    >>> list(frozenbitset(7))
    [1, 1, 1]
    >>> list(frozenbitset(8))
    [0, 0, 0, 1]
    >>> list(frozenbitset(10, size=5))
    [0, 1, 0, 1, 0]
    >>> list(reversed(frozenbitset(8)))
    [1, 0, 0, 0]

    [index], [start:stop:step]:
    >>> frozenbitset(8)[0]
    0
    >>> frozenbitset(8)[3]
    1
    >>> frozenbitset(8)[-1]
    1
    >>> frozenbitset()[0]
    Traceback (most recent call last):
      ...
    IndexError: Invalid frozenbitset index: 0
    >>> frozenbitset()[::]
    frozenbitset()
    >>> frozenbitset()[::1]
    frozenbitset()
    >>> frozenbitset(0b111000)[:3]
    frozenbitset(size=3)
    >>> frozenbitset(0b111000)[3:]
    frozenbitset(7)
    >>> frozenbitset(0b111000)[:3:1]
    frozenbitset(size=3)
    >>> frozenbitset(0b111000)[3::1]
    frozenbitset(7)
    >>> frozenbitset(8)[::-1]
    frozenbitset(1, size=4)
    >>> frozenbitset(10)[::2]
    frozenbitset(size=2)

    ==:
    >>> frozenbitset() == frozenbitset()
    True
    >>> frozenbitset() == frozenbitset(size = 1)
    False
    >>> frozenbitset() == bitset()
    True
    >>> frozenbitset() == 0
    True

    # >>> frozenbitset() == (0, 0)
    # True

    ~:
    >>> ~frozenbitset()
    frozenbitset()
    >>> ~frozenbitset(8)
    frozenbitset(7, size=4)

    &:
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
    >>> 8 & frozenbitset(8)
    frozenbitset(8)
    >>> 0 & frozenbitset(8)
    frozenbitset(size=4)

    |:
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
    >>> 8 | frozenbitset(8)
    frozenbitset(8)
    >>> 0 | frozenbitset(8)
    frozenbitset(8)

    ^:
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
    >>> 8 ^ frozenbitset(8)
    frozenbitset(size=4)
    >>> 0 ^ frozenbitset(8)
    frozenbitset(8)

    <<:
    >>> frozenbitset() << 5
    frozenbitset(size=5)
    >>> frozenbitset(1) << 5
    frozenbitset(32)
    >>> frozenbitset() << 0
    frozenbitset()

    >>:
    >>> frozenbitset(1) >> 1
    frozenbitset()
    >>> frozenbitset(8) >> 3
    frozenbitset(1)

    +:
    >>> frozenbitset() + frozenbitset()
    frozenbitset()
    >>> frozenbitset(8) +  frozenbitset(7)
    frozenbitset(71)
    >>> (8 << 3) + 7
    71

    *:
    >>> frozenbitset(7) * 2
    frozenbitset(63)
    >>> frozenbitset(2) * 2
    frozenbitset(10)
    >>> 2 * frozenbitset(7)
    frozenbitset(63)
    >>> 2 * frozenbitset(2)
    frozenbitset(10)

    %:
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

    .bit_mask:
    >>> frozenbitset().bit_mask
    0
    >>> frozenbitset(1).bit_mask
    1
    >>> frozenbitset(2).bit_mask
    3
    >>> frozenbitset(8).bit_mask
    15

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
    >>> x = bitset(0b100111100101); print(x)
    100111100101
    >>> x &= 0; print(x)
    000000000000
    >>> x = bitset( 0b00111100101)
    >>> y = bitset(0b101010101001)
    >>> x &= y; print(x)
    000010100001
    """


def test_speed() -> None:
    runs = 100
    # size = 1_000_000
    size = 1_000
    size8 = size // 8
    size2 = size // 2

    for _ in range(runs):
        with AdaptiveTimeMeasurer(
            target_time=0.2,
            config_file='_bitset_bench_opt.json' if COMPILED else '_bitset_bench_pure.json',
            history_len=100,
            adapt_ratio=10,
            # print_to='_bitset_bench_opt.txt' if COMPILED else '_bitset_bench_pure.txt',
        ) as atm:
            by = random.randbytes(size)
            b = bitset.random(size)
            l = list(b)

            print(f'size = {size}')
            print()

            T = atm('empty loop', extra=2)
            T.calibrate(0)
            with T as cnt:
                for _ in repeat(None, cnt):
                    pass
            assert T.time is not None
            T.calibrate(T.time)

            with atm('calibrated empty loop') as cnt:
                for _ in repeat(None, cnt):
                    pass

            with atm('range loop') as cnt:
                for _ in range(cnt):
                    pass

            with atm('while loop down') as cnt:
                i = cnt
                while i:
                    i -= 1

            with atm('while loop up') as cnt:
                i = 0
                while i < cnt:
                    i += 1

            with atm('repeat(None, cnt)') as cnt:
                for _ in repeat(None, cnt):
                    repeat(None, cnt)

            with atm('empty loop with 100 assignment') as cnt:
                for _ in repeat(None, cnt):
                    # fmt: off
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    _=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;_=_;
                    # fmt: on

            print()

            with atm('1') as cnt:
                for _ in repeat(None, cnt):
                    1

            print()

            a = 1.0
            b = 2.0

            with atm('a + b') as cnt:
                for _ in repeat(None, cnt):
                    a + b

            with atm('a - b') as cnt:
                for _ in repeat(None, cnt):
                    a - b

            with atm('a * b') as cnt:
                for _ in repeat(None, cnt):
                    a * b

            with atm('a / b') as cnt:
                for _ in repeat(None, cnt):
                    a / b

            with atm('a // b') as cnt:
                for _ in repeat(None, cnt):
                    a // b

            with atm('a % b') as cnt:
                for _ in repeat(None, cnt):
                    a % b

            with atm('a ** b') as cnt:
                for _ in repeat(None, cnt):
                    a**b

            with atm('a ** 2') as cnt:
                for _ in repeat(None, cnt):
                    a**2

            with atm('a * a') as cnt:
                for _ in repeat(None, cnt):
                    a * a

            print()

            with atm('int("1")') as cnt:
                for _ in repeat(None, cnt):
                    int("1")

            with atm('str(1)') as cnt:
                for _ in repeat(None, cnt):
                    str(1)

            with atm('hash(hash)') as cnt:
                for _ in repeat(None, cnt):
                    hash(hash)

            with atm('eval("1 + 1")') as cnt:
                for _ in repeat(None, cnt):
                    eval("1 + 1")

            with atm('object') as cnt:
                for _ in repeat(None, cnt):
                    object

            with atm('_') as cnt:
                for _ in repeat(None, cnt):
                    _

            print()

            # fmt: off
            with atm('try-except passes') as cnt:
                for _ in repeat(None, cnt):
                    try: pass
                    except: pass

            with atm('try-except failed') as cnt:
                for _ in repeat(None, cnt):
                    try: 1/0
                    except: pass

            with atm('def _(): pass') as cnt:
                for _ in repeat(None, cnt):
                    def _(): pass

            with atm('lambda: None') as cnt:
                for _ in repeat(None, cnt):
                    lambda: None

            with atm('(lambda: None)()') as cnt:
                for _ in repeat(None, cnt):
                    (lambda: None)()

            with atm('class _: pass') as cnt:
                for _ in repeat(None, cnt):
                    class _: pass  # type: ignore[no-redef]
            # fmt: on

            print()

            noop = lambda *_, **__: None

            with atm('noop1()') as cnt:
                for _ in repeat(None, cnt):
                    noop()

            noop = lambda: None

            with atm('noop2()') as cnt:
                for _ in repeat(None, cnt):
                    noop()

            print()

            # with atm('int()') as cnt:
            #     for _ in repeat(None, cnt):
            #         int()

            # with atm('0') as cnt:
            #     for _ in repeat(None, cnt):
            #         0

            # with atm('1+1') as cnt:
            #     for _ in repeat(None, cnt):
            #         _ = 1
            #         _ + _

            # print()

            # with atm('str()') as cnt:
            #     for _ in repeat(None, cnt):
            #         str()

            # with atm('""') as cnt:
            #     for _ in repeat(None, cnt):
            #         """"""

            # print()

            # with atm('list()') as cnt:
            #     for _ in repeat(None, cnt):
            #         list()

            # with atm('[]') as cnt:
            #     for _ in repeat(None, cnt):
            #         []

            # print()

            # with atm('tuple()') as cnt:
            #     for _ in repeat(None, cnt):
            #         tuple()

            # with atm('()') as cnt:
            #     for _ in repeat(None, cnt):
            #         ()

            # print()

            # with atm('dict()') as cnt:
            #     for _ in repeat(None, cnt):
            #         dict()

            # with atm('{}') as cnt:
            #     for _ in repeat(None, cnt):
            #         {}

            # print()

            # with atm('bytes()') as cnt:
            #     for _ in repeat(None, cnt):
            #         bytes()

            # with atm('b""') as cnt:
            #     for _ in repeat(None, cnt):
            #         b""""""

            # print()

            # with atm('set()') as cnt:
            #     for _ in repeat(None, cnt):
            #         set()

            # with atm('{0}') as cnt:
            #     for _ in repeat(None, cnt):
            #         {0}

            # with atm('0 in {0}') as cnt:
            #     for _ in repeat(None, cnt):
            #         0 in {0}

            # print()

            # with atm('by + b"0"') as cnt:
            #     for _ in repeat(None, cnt):
            #         by + b"0"

            # with atm('hash(by + b"0")') as cnt:
            #     for _ in repeat(None, cnt):
            #         hash(by + b"0")

            # with atm('md5(by + b"0").digest()') as cnt:
            #     for _ in repeat(None, cnt):
            #         md5(by + b"0").digest()

            # with atm('sha256(by + b"0").digest()') as cnt:
            #     for _ in repeat(None, cnt):
            #         sha256(by + b"0").digest()

            # print()

            # with atm('object()') as cnt:
            #     for _ in repeat(None, cnt):
            #         object()

            # with atm('bitset()') as cnt:
            #     for _ in repeat(None, cnt):
            #         bitset()

            # with atm('frozenbitset()') as cnt:
            #     for _ in repeat(None, cnt):
            #         frozenbitset()

            # with atm('bitset(size=size)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bitset(size=size)

            # print()

            # with atm('~bitset(size=size)') as cnt:
            #     for _ in repeat(None, cnt):
            #         ~bitset(size=size)

            # with atm('bitset((1<<size)-1)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bitset((1 << size) - 1)

            # with atm('[0]*size') as cnt:
            #     for _ in repeat(None, cnt):
            #         [0] * size

            # with atm('[0 for _ in range(size)]') as cnt:
            #     for _ in repeat(None, cnt):
            #         [0 for _ in range(size)]

            # with atm('bytes(size8)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bytes(size8)

            # print()

            # with atm('type(b)') as cnt:
            #     for _ in repeat(None, cnt):
            #         type(b)

            # with atm('b.__class__') as cnt:
            #     for _ in repeat(None, cnt):
            #         b.__class__

            # with atm('b.value b.size') as cnt:
            #     for _ in repeat(None, cnt):
            #         b.value
            #         b.size

            # with atm('b._value b._size') as cnt:
            #     for _ in repeat(None, cnt):
            #         b._value
            #         b._size

            # print()

            # with atm('list(b)') as cnt:
            #     for _ in repeat(None, cnt):
            #         list(b)

            # with atm('list(l)') as cnt:
            #     for _ in repeat(None, cnt):
            #         list(l)

            # with atm('bitset.from_list(l)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bitset.from_list(l)

            # with atm('bitset.from_iterable(b)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bitset.from_iterable(b)

            # print()

            # with atm('bitset.random(size)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bitset.random(size)

            # print()

            # with atm('b[size2]') as cnt:
            #     for _ in repeat(None, cnt):
            #         b[size2]

            # with atm('l[size2]') as cnt:
            #     for _ in repeat(None, cnt):
            #         l[size2]

            # print()

            # with atm('b[::]') as cnt:
            #     for _ in repeat(None, cnt):
            #         b[::]

            # with atm('l[::]') as cnt:
            #     for _ in repeat(None, cnt):
            #         l[::]

            # print()

            # with atm('b[::2]') as cnt:
            #     for _ in repeat(None, cnt):
            #         b[::2]

            # with atm('l[::2]') as cnt:
            #     for _ in repeat(None, cnt):
            #         l[::2]

            # print()

            # with atm('b[::-1]') as cnt:
            #     for _ in repeat(None, cnt):
            #         b[::-1]

            # with atm('l[::-1]') as cnt:
            #     for _ in repeat(None, cnt):
            #         l[::-1]

            # print()

            # with atm('b + b') as cnt:
            #     for _ in repeat(None, cnt):
            #         b + b

            # with atm('l + l') as cnt:
            #     for _ in repeat(None, cnt):
            #         l + l

            # print()

            # with atm('b * 2') as cnt:
            #     for _ in repeat(None, cnt):
            #         b * 2

            # with atm('b * 2 * 2') as cnt:
            #     for _ in repeat(None, cnt):
            #         b * 2 * 2

            # with atm('l * 2') as cnt:
            #     for _ in repeat(None, cnt):
            #         l * 2

            # print()

            # with atm('b % size2') as cnt:
            #     for _ in repeat(None, cnt):
            #         b % size2

            # with atm('l[:size2]') as cnt:
            #     for _ in repeat(None, cnt):
            #         l[:size2]

            # print()

            # with atm('bool(b)') as cnt:
            #     for _ in repeat(None, cnt):
            #         bool(b)

            # with atm('any(l)') as cnt:
            #     for _ in repeat(None, cnt):
            #         any(l)

            # print()

            # with atm('iter(b)') as cnt:
            #     for _ in repeat(None, cnt):
            #         iter(b)

            # with atm('reversed(b)') as cnt:
            #     for _ in repeat(None, cnt):
            #         reversed(b)

            # with atm('iter(l)') as cnt:
            #     for _ in repeat(None, cnt):
            #         iter(l)

            # print()

            # with atm('b == b') as cnt:
            #     for _ in repeat(None, cnt):
            #         b == b

            # with atm('l == l') as cnt:
            #     for _ in repeat(None, cnt):
            #         l == l

            # print()

            # with atm('~b') as cnt:
            #     for _ in repeat(None, cnt):
            #         ~b

            # with atm('[not i for i in l]') as cnt:
            #     for _ in repeat(None, cnt):
            #         [not i for i in l]

            # print()

            # with atm('b & b') as cnt:
            #     for _ in repeat(None, cnt):
            #         b & b
            # with atm('b | b') as cnt:
            #     for _ in repeat(None, cnt):
            #         b | b
            # with atm('b ^ b') as cnt:
            #     for _ in repeat(None, cnt):
            #         b ^ b
            # with atm('b & 0') as cnt:
            #     for _ in repeat(None, cnt):
            #         b & 0
            # with atm('b & 1') as cnt:
            #     for _ in repeat(None, cnt):
            #         b & 1
            # with atm('b | 0') as cnt:
            #     for _ in repeat(None, cnt):
            #         b | 0
            # with atm('b ^ 0') as cnt:
            #     for _ in repeat(None, cnt):
            #         b ^ 0
            # with atm('b << size2') as cnt:
            #     for _ in repeat(None, cnt):
            #         b << size2
            # with atm('b >> size2') as cnt:
            #     for _ in repeat(None, cnt):
            #         b >> size2

            # print()
            # with atm('b.bit_mask') as cnt:
            #     for _ in repeat(None, cnt):
            #         b.bit_mask
            # with atm('b.strip()') as cnt:
            #     for _ in repeat(None, cnt):
            #         b.strip()


if __name__ == '__main__':
    import doctest

    res = doctest.testmod(optionflags=doctest.ELLIPSIS)
