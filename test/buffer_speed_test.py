from __future__ import annotations
from itertools import repeat
from typing import Any, Generic, Iterator, TypeVar

import random

# from t import AdaptiveTimeMeasurer, print_stats
from rangers._drafts.t import AdaptiveTimeMeasurer, print_stats

import rangers

from rangers.std.buffer import Buffer

# from rangers.std.buffer_old import Buffer
# from rangers.std._buffer import Buffer


def test_speed() -> None:
    with AdaptiveTimeMeasurer(
        target_time=0.2,  # in seconds
        config_file='bench.json',
        history_len=10,
        # flush=True,
    ) as atm:
        n3 = 10**3
        n6 = 10**6
        n9 = 10**9

        bytes_3 = bytes(i % 256 for i in range(n3))
        bytes_6 = bytes(i % 256 for i in range(n6))

        a: Any

        T = atm('pass', extra=2)
        T.calibrate(0)
        with T as _:
            for _ in _:
                pass
        assert T.time is not None
        T.calibrate(T.time)

        with atm('pass*') as _:
            for _ in _:
                pass

        print()

        b = Buffer(bytes_6)
        with atm('read(1)', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.read(1)

        with atm('read_byte', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.read_byte()

        with atm('read_bool', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.read_bool()

        with atm('read_i8', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.read_i8()

        with atm('read_i32', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.read_i32()

        print()

        b = Buffer()
        with atm('write(b" ")', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.write(b' ')

        b = Buffer()
        with atm('write_byte', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.write_byte(1)

        b = Buffer()
        with atm('write_i8', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.write_i8(1)

        b = Buffer()
        with atm('write_i32', k=n3) as _:
            for _ in _:
                b.pos = 0
                for _ in repeat(None, n3):
                    b.write_i32(1)

        print()
        print()


def main() -> None:
    import platform
    import sys

    print(platform.processor())
    print(f'{sys.implementation.name} v{".".join(map(str, sys.version_info))}')
    print()
    print_stats('bench.json')
    input('Press enter to continue...')
    for _ in range(10):
        test_speed()


if __name__ == '__main__':
    main()
