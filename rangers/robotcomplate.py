"""!
@file
"""
from __future__ import annotations

import json

from .buffer import Buffer
from .std.dataclass import (
    DataClass,
    Int32,
    CRC,
    List,
    Converted,
    Nested,
)

__all__ = [
    'RC',
]

RCObj: DataClass[list[dict[str, int]]] = Nested(
    CRC(),
    Converted(
        List(Int32(), lensize=4),
        decode=lambda l: [
            {
                'time': a,
                'win_type': b,
            }
            for a, b in zip(l[::2], l[1::2])
        ],
        encode=lambda l: sum(
            [
                [
                    i['time'],
                    i['win_type'],
                ]
                for i in l
            ],
            start=[],
        ),
    ),
)


class RC:
    data: list[dict[str, int]]

    def __init__(self) -> None:
        self.data = []

    def __repr__(self) -> str:
        return str(self.data)

    def __str__(self) -> str:
        return str(self.data)

    @classmethod
    def from_buffer(cls, buf: Buffer) -> RC:
        self = cls()
        self.data = buf.read_dcls(RCObj)
        return self

    def to_buffer(self, buf: Buffer) -> None:
        buf.write_dcls(RCObj, self.data)

    @classmethod
    def from_bytes(cls, data: bytes) -> RC:
        return cls.from_buffer(Buffer(data))

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_file(cls, filename: str) -> RC:
        with open(filename, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_file(self, filename: str) -> None:
        data = self.to_bytes()
        with open(filename, 'wb') as file:
            file.write(data)

    @classmethod
    def from_json(cls, filename: str) -> RC:
        self = cls()
        with open(filename, 'rt', encoding='utf-8') as file:
            self.data = json.load(
                file,
            )
        return self

    def to_json(self, filename: str) -> None:
        with open(filename, 'wt', encoding='utf-8') as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=2,
            )
