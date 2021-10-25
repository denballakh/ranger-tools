"""!
@file
"""
from __future__ import annotations

import zlib
from typing import Any

from ranger_tools.io import Buffer

__all__ = [
    'SAV',
]

class SAV:
    data: dict[str, Any]

    def __init__ (self) -> None:
        self.data = {}

    def __repr__(self) -> str:
        return str(self.data)

    def __str__(self) -> str:
        return str(self.data)

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
        # len1 = buf.read_uint()

        d['data1'] = zlib.decompress(buf.read(buf.read_uint())[8:]).hex(' ', -4)
        print(buf)
        d['data2'] = zlib.decompress(buf.read(buf.read_uint())[8:]).hex(' ', -4)
        print(buf)
        d['data3'] = zlib.decompress(buf.read(buf.read_uint())[8:]).hex(' ', -4)
        # d['data2'] = buf.decodeZL().hex(' ', -4)
        # print(buf)
        # d['data3'] = buf.decodeZL().hex(' ', -4)



        return self

    @classmethod
    def from_bytes(cls, data: bytes) -> SAV:
        return cls.from_buffer(Buffer(data))

    @classmethod
    def from_file(cls, filename: str) -> SAV:
        with open(filename, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)


a = [1,2,3]
for a[0] in [5,6,7]:
    print(a)
