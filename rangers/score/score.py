"""!
@file
"""

import zlib
from typing import Generator

from ..io import Buffer
from ..std.dataclass import BufEC
from ..std.mixins import PrintableMixin
from .fgint import FGInt

__all__ = [
    'SCORE',
]


def _rand31pm(seed: int) -> Generator[int, None, None]:
    while True:
        hi, lo = divmod(seed, 0x1F31D)
        seed = lo * 0x41A7 - hi * 0xB14
        if seed < 1:
            seed += 0x7FFFFFFF
        yield seed - 1


def decipher(data: bytes, key: int) -> bytes:
    din = Buffer(data)
    rnd = _rand31pm(key)
    dout = Buffer()
    while not din.is_end():
        dout.write_byte(din.read_byte() ^ (next(rnd) & 0xFF))
    result = dout.to_bytes()
    return result


class SCORE(PrintableMixin):
    KEY_MAGIC = 0x140F3F9B
    FG_INT_1 = 'HjwH94fmhClFC1prPy'
    FG_INT_2 = 'DjAVRGx='
    UNK = 0x31304C5A

    def __init__(self):
        self.data = {}

    @classmethod
    def from_txt(cls, filename):
        self = cls()

        with open(filename, 'rt', encoding='cp1251') as file:
            text = file.read()

        text = text.split('*************** Protect database ****************')[-1]

        buf = Buffer(bytes.fromhex(text))

        buf.pos = 0
        _three = buf.read_int()
        key_xored = buf.read_int()
        unknown1 = buf.read_uint()
        unknown2 = buf.read_uint()
        assert _three == 3, _three

        key = key_xored ^ cls.KEY_MAGIC
        assert key in range(0, 2000000000), key

        buf = Buffer(decipher(buf.read(), key))
        zl01 = buf.read(4)
        assert zl01 == b'ZL01', zl01
        decompressed_size = buf.read_uint()

        data = zlib.decompress(buf.read())
        assert decompressed_size == len(data), (decompressed_size, len(data))

        self.data['_three'] = _three
        self.data['_key'] = key
        self.data['_crc1'] = unknown1
        self.data['_crc2'] = unknown2

        self.load_from_buf(Buffer(data))

        return self

    def load_from_buf(self, buf: Buffer):
        d = self.data

        d['_version'] = buf.read_uint()
        assert d['_version'] == 205

        d['_04'] = buf.read_byte()

        d['difflevels'] = []
        for _ in range(8):
            d['difflevels'].append(buf.read_byte())

        d['name'] = buf.read_wstr()
        d['_18'] = buf.read_byte()
        d['race'] = buf.read_byte()
        d['date'] = buf.read_uint()
        d['rank'] = buf.read_byte()
        d['_25'] = buf.read_byte()
        d['_28'] = buf.read_uint()
        d['_2C'] = buf.read_uint()
        d['_30'] = buf.read_uint()
        d['liberation_system'] = buf.read_uint()
        d['_44'] = buf.read_uint()
        d['rewards'] = buf.read_uint()

        n = buf.read_uint()
        d['rewards_list'] = []
        for _ in range(n):
            d['rewards_list'].append(buf.read_byte())

        d['_50'] = buf.read_uint()
        d['skills'] = []
        for _ in range(6):
            d['skills'].append(buf.read_byte())

        d['_05'] = buf.read_byte()
        d['_60'] = self.decode_buf1(buf.read_obj(BufEC()))
        d['_5C'] = buf.read_uint()

        n = buf.read_ushort()
        d['_64'] = []
        for _ in range(n):
            d['_64'].append(
                [
                    buf.read_byte(),
                    buf.read_byte(),
                    buf.read_byte(),
                ]
            )

        d['_68'] = buf.read_uint()
        d['_70'] = buf.read_byte()
        d['_71'] = buf.read_byte()
        d['_72'] = buf.read_byte()
        d['_73'] = buf.read_byte()

        n = buf.read_ushort()
        d['planetary_battles'] = []
        for _ in range(n):
            d['planetary_battles'].append(
                [
                    buf.read_uint(),
                    buf.read_int(),
                    buf.read_uint(),
                    buf.read_uint(),
                    buf.read_uint(),
                    buf.read_uint(),
                    buf.read_uint(),
                    buf.read_byte(),
                    buf.read_byte(),
                    buf.read_uint(),
                ]
            )

        d['__'] = buf.read()
        # print(buf)

    @classmethod
    def decode_buf1(cls, data: bytes) -> list[dict]:
        dd: list[dict] = []
        b = Buffer(data)
        while b.bytes_remains():
            d: dict = {}
            dd.append(d)

            d['_13'] = b.read_uint()
            d['_bufsize'] = b.read_uint()
            d['_crc32'] = b.read_uint()
            d['_zero'] = b.read_uint()

            data1 = b.read(d['_bufsize'] - 16)

            d['buf'] = cls.decode_buf2(data1)

        return dd

    @classmethod
    def decode_buf2(cls, data: bytes) -> dict:
        d = {}
        d['_'] = data.hex(' ', -4)

        return d
