from __future__ import annotations
from typing import Any

from .std.buffer import IBuffer, OBuffer
from .std.mixin import DataMixin, JSONMixin
from .std.dataclass import (
    DataClass,
    Int32,
    CRC,
    List,
    Converted,
    Nested,
    UInt32,
)

__all__ = ('RC',)

RCObj: DataClass[list[dict[str, int]]] = Nested(
    CRC(),
    Converted(
        List(Int32, UInt32),
        decode=lambda l: [
            {
                'time': a,
                'win_type': b,
            }
            for a, b in zip(l[::2], l[1::2])
        ],
        encode=lambda l: sum(
            (
                [
                    i['time'],
                    i['win_type'],
                ]
                for i in l
            ),
            start=[],
        ),
    ),
)


class RC(DataMixin, JSONMixin):
    data: list[dict[str, int]]

    def __init__(self) -> None:
        self.data = []

    @classmethod
    def from_buffer(cls, buf: IBuffer, **kwargs: Any) -> RC:
        self = cls()
        self.data = RCObj.read(buf)
        return self

    def to_buffer(self, buf: OBuffer, **kwargs: Any) -> None:
        RCObj.write(buf, self.data)
