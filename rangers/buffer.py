"""!
@file
"""
from __future__ import annotations

from typing import (
    Iterable,
    Iterator,
    Any,
    TypeVar,
    TYPE_CHECKING,
    IO,
)
import struct

if TYPE_CHECKING:
    from .std.dataclass import DataClass


__all__ = [
    'Buffer',
    'IBuffer',
    'OBuffer',
    'BaseBuffer',
]

T = TypeVar('T')


class Buffer:
    data: bytearray
    pos: int
    _position_stack: list[int]

    def __init__(self, obj: Buffer | Iterable[int] = b'', *, pos: int = 0) -> None:
        if isinstance(obj, bytearray):
            self.data = obj  # bytearray is mutable

        elif isinstance(obj, bytes):
            self.data = bytearray(obj)

        elif isinstance(obj, Buffer):
            self.data = obj.data  # it will share instances of data between instances of Buffer

        else:
            self.data = bytearray(obj)

        assert isinstance(self.data, bytearray)

        self.pos = pos
        self._position_stack = []

    def __iter__(self) -> Iterator[int]:
        return iter(self.data)
        # i = 0
        # while i < len(self.data):
        #     yield self.data[i]
        #     i += 1

    def __str__(self) -> str:
        # return str(self.data)
        offset = 32
        return (
            f'<Buffer: '
            f'pos={self.pos} '
            f'before={bytes(self.data[max(0, self.pos - offset): min(self.pos, len(self.data))])!r}, '
            f'current={bytes([self.data[self.pos]]) if self.pos in range(len(self.data)) else None!r} ({self.data[self.pos] if self.pos in range(len(self.data)) else None}), '
            f'after={bytes(self.data[self.pos + 1 : min(self.pos + offset, len(self.data))])!r}, '
            f'len={len(self.data)}'
            f'>'
        )

    def __repr__(self) -> str:
        return f'Buffer({self.data!r}, pos={self.pos})'

    def __eq__(self, other) -> bool:
        if isinstance(other, Buffer):
            return self.data == other.data
        return NotImplemented

    def __bool__(self) -> bool:
        return not self.is_end()

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, key: int) -> int:
        return self.data[key]

    def __bytes__(self) -> bytes:
        return bytes(self.data)

    def to_bytes(self) -> bytes:
        return bytes(self.data)

    def is_end(self) -> bool:
        return self.pos >= len(self.data)

    def bytes_remains(self) -> int:
        return len(self.data) - self.pos

    def pop_pos(self) -> int:
        result = self.pos
        self.pos = self._position_stack.pop()
        return result

    def push_pos(self, pos: int = None) -> int:
        if pos is None:
            pos = self.pos
        assert (
            0 <= pos <= len(self.data)
        ), f'Invalid buffer position: {pos}, self.pos={self.pos}, len={len(self.data)}'
        result = self.pos
        self._position_stack.append(self.pos)
        self.pos = pos
        return result

    def read(self, n: int = None, pos: int = None) -> bytes:
        if pos is not None:
            self.push_pos(pos)
        if n is None:
            n = len(self.data) - self.pos
        elif n < 0:
            n = len(self.data) - self.pos + n

        if not 0 <= self.pos <= len(self.data) - n:
            raise ValueError(f'Invalid buffer position: {self.pos}, len={len(self.data)}')

        result = bytes(self.data[self.pos : self.pos + n])
        self.pos += n
        if pos is not None:
            self.pop_pos()
        return result

    def write(self, data: Iterable[int], pos: int = None) -> None:
        if pos is not None:
            self.push_pos(pos)
        assert (
            0 <= self.pos <= len(self.data)
        ), f'Invalid buffer position: {self.pos}, len={len(self.data)}'
        self.data[self.pos : self.pos + len(data)] = data  # type: ignore[arg-type]
        self.pos += len(data)  # type: ignore[arg-type]
        if pos is not None:
            self.pop_pos()

    def seek(self, pos: int) -> None:
        self.pos = pos
        assert 0 <= self.pos <= len(self.data)

    def reset(self) -> None:
        self.pos = 0

    def skip(self, n: int) -> None:
        self.pos += n

    def load(self, buf: Buffer | IO) -> None:
        self.write(buf.read())

    def save(self, buf: Buffer | IO) -> None:
        buf.write(self.read())

    def load_file(self, path: str) -> None:
        with open(path, 'rb') as file:
            self.load(file)

    def save_file(self, path: str) -> None:
        with open(path, 'wb') as file:
            self.save(file)

    @classmethod
    def from_file(cls, path: str) -> Buffer:
        with open(path, 'rb') as file:
            data = file.read()
        return cls(data)

    def write_format(self, fmt: str, *values: Any, pos: int = None):
        if pos is not None:
            self.push_pos(pos)

        try:
            self.write(struct.pack(fmt, *values))
        except Exception as e:
            raise Exception(f'Error in struct.pack: fmt={fmt}, values={values}, pos={pos}') from e
        if pos is not None:
            self.pop_pos()

    def read_format(self, fmt: str, pos: int = None) -> Any:
        if pos is not None:
            self.push_pos(pos)

        try:
            result = struct.unpack(fmt, self.read(struct.calcsize(fmt)))
        except Exception as e:
            raise Exception(f'Error in struct.unpack: fmt={fmt}, pos={pos}') from e

        if pos is not None:
            self.pop_pos()
        return result

    def read_byte(self, pos: int =None) -> int:
        return self.read_format('B', pos=pos)[0]

    def write_byte(self, value: int, pos: int =None) -> None:
        return self.write_format('B', value, pos=pos)

    def read_bool(self, pos: int =None) -> bool:
        return self.read_format('?', pos=pos)[0]

    def write_bool(self, value: bool, pos: int =None) -> None:
        return self.write_format('?', value, pos=pos)

    def read_char(self, pos: int =None) -> int:
        return self.read_format('b', pos=pos)[0]

    def write_char(self, value: int, pos: int =None) -> None:
        return self.write_format('b', value, pos=pos)

    def read_uchar(self, pos: int =None) -> int:
        return self.read_format('B', pos=pos)[0]

    def write_uchar(self, value: int, pos: int =None) -> None:
        return self.write_format('B', value, pos=pos)

    def read_short(self, pos: int =None) -> int:
        return self.read_format('<h', pos=pos)[0]

    def write_short(self, value: int, pos: int =None) -> None:
        return self.write_format('<h', value, pos=pos)

    def read_ushort(self, pos: int =None) -> int:
        return self.read_format('<H', pos=pos)[0]

    def write_ushort(self, value: int, pos: int =None) -> None:
        return self.write_format('<H', value, pos=pos)

    def read_int(self, pos: int =None) -> int:
        return self.read_format('<i', pos=pos)[0]

    def write_int(self, value: int, pos: int =None) -> None:
        return self.write_format('<i', value, pos=pos)

    def read_uint(self, pos: int =None) -> int:
        return self.read_format('<I', pos=pos)[0]

    def write_uint(self, value: int, pos: int =None) -> None:
        return self.write_format('<I', value, pos=pos)

    def read_long(self, pos: int =None) -> int:
        return self.read_format('<q', pos=pos)[0]

    def write_long(self, value: int, pos: int =None) -> None:
        return self.write_format('<q', value, pos=pos)

    def read_ulong(self, pos: int =None) -> int:
        return self.read_format('<Q', pos=pos)[0]

    def write_ulong(self, value: int, pos: int =None) -> None:
        return self.write_format('<Q', value, pos=pos)

    def read_float(self, pos: int =None) -> float:
        return self.read_format('<f', pos=pos)[0]

    def write_float(self, value: float, pos: int =None) -> None:
        return self.write_format('<f', value, pos=pos)

    def read_double(self, pos: int =None) -> float:
        return self.read_format('<d', pos=pos)[0]

    def write_double(self, value: float, pos: int =None) -> None:
        return self.write_format('<d', value, pos=pos)

    def read_str(self, length: int = -1) -> str:
        if length == -1:
            result = ''
            x = self.read(1).decode('utf-8')
            while x != '\0':
                result += x
                x = self.read(1).decode('utf-8')
        else:
            data = self.read(length)
            result = data.decode('utf-8')
            result = result.rstrip('\0')
        return result

    def write_str(self, value: str, length: int = -1) -> None:
        if length == -1:
            value += '\0'
        else:
            value = value[:length]
            value += (length - len(value)) * '\0'
        self.write(value.encode('utf-8'))

    def read_wstr(self, length: int = -1) -> str:
        if length == -1:
            result = ''
            x = self.read(2).decode('utf-16le')
            while x != '\0':
                result += x
                x = self.read(2).decode('utf-16le')
        else:
            data = self.read(length * 2)
            result = data.decode('utf-16le')
            result = result.rstrip('\0')
        return result

    def write_wstr(self, value: str, length: int = -1) -> None:
        if length == -1:
            value += '\0'
        else:
            value = value[:length]
            value += (length - len(value)) * '\0'
        self.write(value.encode('utf-16le'))

    def read_obj(self, dcls: DataClass[T]) -> T:
        return dcls.read(self)

    def write_obj(self, dcls: DataClass[T], obj: T) -> None:
        dcls.write(self, obj)

BaseBuffer = Buffer
IBuffer = Buffer
OBuffer = Buffer
