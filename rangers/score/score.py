from __future__ import annotations

import zlib
from typing import Generator

import random

from ..buffer import Buffer
from ..common import rand31pm
from ..std.mixin import PrintableMixin
from .fgint import FGInt

from ..std.dataclass import (
    DataClass,
    Byte,
    Int32,
    UInt32,
    WStr,
    Bytes,
    List,
    Pack,
    Const,
    AnyOf,
    Repeat,
    NamedSequence,
    Nested,
    CustomCallable,
    Converted,
    BufEC,
    ZL,
    AddToMemo,
    Memo,
)

__all__ = [
    'SCORE',
]

KEY_MAGIC = 0x140F3F9B
FG_INT_1 = 'HjwH94fmhClFC1prPy'
FG_INT_2 = 'DjAVRGx='
UNK = 0x31304C5A


class CryptedRand31pmMod(DataClass[bytes]):
    __slots__ = 'key_name'

    def __init__(self, key_name: str) -> None:
        self.key_name = key_name

    def read(self, buf: Buffer, *, memo: Memo) -> bytes:
        key = memo[self.key_name]
        rnd = rand31pm(key)

        out = Buffer()

        while buf:
            out.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))
        result = bytes(out)
        return result

    def write(self, buf: Buffer, obj: bytes, *, memo: Memo) -> None:
        key = memo[self.key_name]
        rnd = rand31pm(key)

        inp = Buffer(obj)

        while inp:
            buf.write_byte(inp.read_byte() ^ (next(rnd) & 0xFF))


ScoreObj = NamedSequence(
    _three=Const(Int32(), 3, 'invalid magic number'),
    cipher_key=AddToMemo(
        'cipher_key',
        AnyOf(
            Converted(
                Int32(),
                decode=lambda i: i ^ KEY_MAGIC,
                encode=lambda i: i ^ KEY_MAGIC,
            ),
            range(2 * 10 ** 9),
        ),
    ),
    _unknown1=UInt32(),
    _unknown2=UInt32(),
    _buf=Nested(
        CryptedRand31pmMod('cipher_key'),
        Nested(
            ZL(1, length=-1),
            NamedSequence(
                version=Const(UInt32(), 205),
                _04=Byte(),
                difflevels=Repeat(Byte(), 8),
                name=WStr(),
                _18=Byte(),
                race=Byte(),
                date=UInt32(),
                rank=Byte(),
                _25=Byte(),
                _28=UInt32(),
                _2C=UInt32(),
                _30=UInt32(),
                liberation_system=UInt32(),
                _44=UInt32(),
                rewards_cnt=UInt32(),
                rewards=List(Byte(), lensize=4),
                _50=UInt32(),
                skills=Repeat(Byte(), 6),
                _05=Byte(),
                _60=Nested(
                    BufEC(),
                    Pack(
                        NamedSequence(
                            _13=UInt32(),
                            _bufsize=AddToMemo('bufsize', UInt32()),
                            _crc32=UInt32(),
                            _zero=Const(UInt32(), 0, 'not zero'),
                            _buf=Nested(
                                CustomCallable(  # type: ignore[call-arg]
                                    decode=lambda buf, memo: buf.read(memo['bufsize'] - 16),
                                    encode=lambda buf, data, memo: (
                                        memo.__setitem__('bufsize', len(data) + 16),  # type: ignore[func-returns-value]
                                        buf.write(data),  # type: ignore[func-returns-value]
                                    )[-1],
                                ),
                                NamedSequence(
                                    remains=Converted(
                                        Bytes(),
                                        decode=lambda b: b.hex(' ', -4),
                                        encode=lambda s: bytes.fromhex(s),
                                    ),
                                ),
                            ),
                        )
                    ),
                ),
                _5c=UInt32(),
                _64=List(
                    NamedSequence(
                        _0=Byte(),
                        _1=Byte(),
                        _2=Byte(),
                    ),
                    lensize=2,
                ),
                _68=UInt32(),
                _70=Byte(),
                _71=Byte(),
                _72=Byte(),
                _73=Byte(),
                planetary_battles=List(
                    NamedSequence(
                        _0=UInt32(),
                        _1=Int32(),
                        _2=UInt32(),
                        _3=UInt32(),
                        _4=UInt32(),
                        _5=UInt32(),
                        _6=UInt32(),
                        _7=Byte(),
                        _8=Byte(),
                        _9=UInt32(),
                    ),
                    lensize=2,
                ),
                _remains=Bytes(),
            ),
        ),
    ),
)


class SCORE(PrintableMixin):
    def __init__(self):
        self.data = {}

    @classmethod
    def from_txt(cls, path: str) -> SCORE:

        with open(path, 'rt', encoding='cp1251') as file:
            text = file.read()

        text = text.split('*************** Protect database ****************')[-1]

        return cls.from_bytes(bytes.fromhex(text))

    @classmethod
    def from_bytes(cls, data: bytes) -> SCORE:
        return cls.from_buffer(Buffer(data))

    @classmethod
    def from_buffer(cls, buf: Buffer) -> SCORE:
        self = cls()
        self.data = buf.read_dcls(ScoreObj)
        return self
