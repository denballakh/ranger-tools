from __future__ import annotations
from typing import TYPE_CHECKING

from itertools import repeat
import random

from rangers.std.time import AdaptiveTimeMeasurer
from rangers.std.bidict import bidict
from rangers.common import rand31pm
COMPILED = bidict.__init__.__class__.__name__ != 'function'


def test_doc():
    """!
    >>> bidict()
    bidict()
    >>> bidict({})
    bidict()
    >>> bidict({1: 2})
    bidict({1: 2})
    >>> bidict({1: 2, 2: 3, 3: 1})
    bidict({1: 2, 2: 3, 3: 1})

    >>> bidict().inv
    bidict()
    >>> bidict({1: 2}).inv
    bidict({2: 1})
    >>> bidict({1: 2, 2: 3, 3: 1}).inv
    bidict({2: 1, 3: 2, 1: 3})

    >>> b = bidict()
    >>> b[1] = 1
    >>> b[2] = 1
    >>> b[3] = 1
    >>> b
    bidict({3: 1})
    >>> b[1] = True
    >>> b
    bidict({1: True})
    >>> b.inv[1] = True
    >>> b
    bidict({True: 1})
    >>> del b[1]
    >>> b
    bidict()

    >>> b = bidict()
    >>> b[1] = 1
    >>> b[True] = 1
    >>> b[1] = True
    >>> b[True] = True

    >>> bidict({1: 2, 3: 2})
    Traceback (most recent call last):
      ...
    ValueError: value 2 repeats at key 1 and 3

    """

type
def test_speed() -> None:
    runs = 1
    for _ in range(runs):
        with AdaptiveTimeMeasurer(
            target_time=0.5,
            config_file='_bidict_bench_opt.json' if COMPILED else '_bidict_bench_pure.json',
            history_len=20,
            # print_to='_bidict_bench_opt.txt' if COMPILED else '_bidict_bench_pure.txt',
        ) as atm:
            d = dict[int, int]()
            bd = bidict[int, int]()
            randint = random.randint
            rnd = rand31pm(randint(0, 2 ** 31))

            b1 = bidict[int, int]()
            for _ in range(1_000):
                b1[next(rnd)] = next(rnd)

            b2 = bidict[int, int]()
            for _ in range(1_000):
                b2[next(rnd)] = next(rnd)

            d1 = dict(b1.proxy)
            d2 = dict(b2.proxy)


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

            print()

            with atm('randint(0, 100)') as cnt:
                for _ in repeat(None, cnt):
                    randint(0, 100)

            with atm('next(rnd)') as cnt:
                for _ in repeat(None, cnt):
                    next(rnd)

            print()

            with atm('bidict()') as cnt:
                for _ in repeat(None, cnt):
                    bidict()

            with atm('dict()') as cnt:
                for _ in repeat(None, cnt):
                    dict()

            print()

            with atm('d[next(rnd)]') as cnt:
                for _ in repeat(None, cnt):
                    if (r := next(rnd)) in d:
                        d[r]

            with atm('d[next(rnd)] = next(rnd)') as cnt:
                for _ in repeat(None, cnt):
                    d[next(rnd)] = next(rnd)

            with atm('d[next(rnd)] = next(rnd) & del') as cnt:
                for _ in repeat(None, cnt):
                    d[(r := next(rnd))] = next(rnd)
                    del d[r]

            with atm('d1 | d2') as cnt:
                for _ in repeat(None, cnt):
                    d1 | d2

            print()

            with atm('bd[next(rnd)]') as cnt:
                for _ in repeat(None, cnt):
                    if (r := next(rnd)) in bd.proxy:
                        bd[r]

            with atm('bd[next(rnd)] = next(rnd)') as cnt:
                for _ in repeat(None, cnt):
                    bd[next(rnd)] = next(rnd)

            with atm('bd[next(rnd)] = next(rnd) & del') as cnt:
                for _ in repeat(None, cnt):
                    bd[(r := next(rnd))] = next(rnd)
                    del bd[r]

            with atm('b1 | b2') as cnt:
                for _ in repeat(None, cnt):
                    b1 | b2



if __name__ == '__main__':
    import doctest
    import os

    res = doctest.testmod(optionflags=doctest.ELLIPSIS)

    if res.failed == 0:
        test_speed()

    input('Press enter to exit...')
    os._exit(res.failed)
