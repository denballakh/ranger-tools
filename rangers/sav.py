"""!
@file
"""
from __future__ import annotations
from typing import Any, Iterator

import zlib

from .io import Buffer
from .std.dataclass import DataClass, ZL

__all__ = [
    'SAV',
]

def _rand31pm(seed: int) -> Iterator[int]:
    while True:
        hi, lo = divmod(seed, 0x1F31D)
        seed = lo * 0x41A7 - hi * 0xB14
        if seed < 1:
            seed += 0x7FFFFFFF
        yield seed - 1

class SAV:
    data: dict[str, Any]

    def __init__ (self) -> None:
        self.data = {}

    def __repr__(self) -> str:
        return str(self.data)

    def __str__(self) -> str:
        return str(self.data)

    @classmethod
    def from_bytes(cls, data: bytes) -> SAV:
        return cls.from_buffer(Buffer(data))

    @classmethod
    def from_file(cls, filename: str) -> SAV:
        with open(filename, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    @classmethod
    def from_buffer(cls, buf: Buffer) -> SAV:
        self = cls()
        d = self.data

        d['magic'] = buf.read_wstr()
        assert d['magic'] == 'RSG', d['magic']
        d['version'] = buf.read_wstr()
        assert d['version'].startswith('v'), d['version']

        d['mode'] = buf.read_wstr()
        d['turn'] = int(buf.read_wstr())
        d['money'] = int(buf.read_wstr())
        d['name'] = buf.read_wstr()
        d['race'] = buf.read_wstr()
        d['EZ'] = buf.read_wstr()

        print(buf)
        d['data1'] = buf.read_obj(ZL(1))
        print(buf)
        d['data2'] = buf.read_obj(ZL(1))
        print(buf)
        crc = buf.read_uint()
        key = buf.read_uint()
        size = buf.read_uint()
        assert key in range(0, 2000000001), f'Invalid key: {key}'
        data3 = Buffer()
        data3.write_uint(size)
        rnd = _rand31pm(key)
        for _ in range(size):
            data3.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))
        assert zlib.crc32(data3.data[4:]) == crc, 'Invalid hash'
        data3.pos = 0
        d['data3'] = data3.read_obj(ZL(1))
        print(buf)

        d['data4'] = buf.read_obj(ZL(1, length=buf.bytes_remains()))







        return self


'''
_34 = a4 = data1
_38 = a5 = data2
_3C = a6 = data3
_40 = a7 = data4

'''
