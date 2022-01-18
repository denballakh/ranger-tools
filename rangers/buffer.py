"""!
@file
"""
from __future__ import annotations

from typing import (
    Iterable,
    Iterator,
    # Sized,
    Any,
    TypeVar,
    TYPE_CHECKING,
    IO,
    # overload,
    Literal,
    # Protocol,
    Collection,
)
import struct
from struct import Struct


if TYPE_CHECKING:
    from .std.dataclass import DataClass, Memo


__all__ = [
    'Buffer',
    'IBuffer',
    'OBuffer',
    'BaseBuffer',
    'IDCBuffer',
    'ODCBuffer',
    'DCBuffer',
]

T = TypeVar('T')


# _hex_readable_chars: set[int] = {
#     ord(c)
#     for c in (
#         # '!"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~'
#         # + 'abcdefghijklmnopqrstuvwxyz'
#         # + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     )
# }
_hex_readable_chars = set[int]()

_hex_char_conv: dict[int | str, str] = {
    '\0': '..',
    '\x01': '.1',
    '\x02': '.2',
    '\x03': '.3',
    '\x04': '.4',
    '\x05': '.5',
    '\x06': '.6',
    '\x07': '.7',
    '\x08': '.8',
    '\x09': '.9',
    '\x0A': '.A',
    '\x0B': '.B',
    '\x0C': '.C',
    '\x0D': '.D',
    '\x0E': '.E',
    '\x0F': '.F',
    '\xFF': '##',
}

_str_rus_chars: str = 'абвгдеёжзийклмонпрстуфхцчшщъыьэюя' + 'АБВГДЕЁЖЗИЙКЛМОНПРСТУФХЦЧШЩЪЫЬЭЮЯ'

_str_readable_chars: str = (
    '!"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
)

_str_char_conv: dict[int | str, str] = {
    ' ': '_',
    '\0': ' ',
    # '\xFF': '#',
}

_pg = [
    ['│', '─'],
    ['┌', '┬', '┐'],
    ['├', '┼', '┤'],
    ['└', '┴', '┘'],
]


def _bytes_to_hex(d: bytes | bytearray) -> str:
    result: list[str] = []
    for byte in d:
        if byte in _hex_readable_chars:
            result.append(' ' + chr(byte))
        elif chr(byte) in _hex_char_conv:
            result.append(_hex_char_conv[chr(byte)])
        else:
            result.append(f'{byte:02X}')
    return ' '.join(result)


def _bytes_to_str(d: bytes | bytearray) -> str:
    result: list[str] = []
    nxt = ''
    for i, byte in enumerate(d):
        if nxt:
            result.append(nxt)
            nxt = ''
            continue

        try:
            b = bytes([byte, d[i + 1]])
            if b.decode('utf-16le') in _str_rus_chars:
                result.append(b.decode('utf-16le'))
                nxt = ' '
                continue

        except UnicodeDecodeError:
            pass

        if chr(byte) in _str_readable_chars:
            result.append(chr(byte))
        elif chr(byte) in _str_char_conv:
            result.append(_str_char_conv[chr(byte)])
        else:
            result.append('.')
    return ''.join(result)


class Buffer:
    __slots__ = ('data', '_pos', '_position_stack')

    data: bytearray | bytes
    _pos: int
    _position_stack: list[int]

    def __init__(self, obj: Buffer | Iterable[int] | int = b'', *, pos: int = 0) -> None:
        if isinstance(obj, bytearray):
            self.data = obj  # bytearray is mutable

        elif isinstance(obj, bytes):
            self.data = bytearray(obj)

        elif isinstance(obj, Buffer):
            self.data = obj.data  # it will share instances of data between instances of Buffer

        elif isinstance(obj, int):
            self.data = bytearray(obj)

        else:
            self.data = bytearray(obj)

        assert isinstance(self.data, (bytearray, bytes))

        self.pos = pos
        self._position_stack = []

    def __iter__(self) -> Iterator[int]:
        return iter(self.data)

    def __str__(self) -> str:
        return self.format_str()

    def __repr__(self) -> str:
        return f'Buffer({self.data!r}, pos={self._pos})'

    def format_str(
        self,
        before: int | None = 4,
        after: int | None = 4,
        width: int = 16,
        cursor: bool | int = True,
    ) -> str:
        # FIXME: very slow and ugly
        assert width > 0
        s = width
        lines: list[str] = []
        rpos: int = self._pos // s * s

        if before is None:
            before = rpos // s

        if after is None:
            after = (len(self.data) // s * s - rpos) // s

        hexlen = max(len(hex(rpos + s * after)[2:]), 5)
        line_len = hexlen + 4 + 4 * s + 6
        lines.append('┌' + '─' * (hexlen + 4) + '┬' + '─' * (3 * s + 1) + '┬' + '─' * (s + 2) + '┐')

        for line_no in range(-before, after + 1):
            line_start = rpos + line_no * s
            if line_start < 0 or line_start > len(self.data):
                continue
            line = '│ '
            line += f'0x{line_start:0{hexlen}X}'
            line += ' │ '

            chunk = self.data[line_start : line_start + s]
            line += _bytes_to_hex(chunk).ljust(3 * s - 1)
            line += ' │ '
            line += _bytes_to_str(chunk).ljust(s)
            line += ' │'
            line_len = len(line)
            lines.append(line)

            if cursor and line_no == 0:
                cursor_s = '╨╨'

                line = '│ '
                line += f'0x{self.pos:0{hexlen}X}'
                line += ' ├─'
                cursor_pos = self.pos % s * 3
                line += '─' * cursor_pos + cursor_s
                line += '───' * (s - self.pos % s - 1)
                line += '─┼─'
                line += '─' * (self.pos % s) + '╨'
                line = line.ljust(line_len - 2, '─')
                line += '─┤'
                lines.append(line)
        lines.append('└' + '─' * (hexlen + 4) + '┴' + '─' * (3 * s + 1) + '┴' + '─' * (s + 2) + '┘')

        return '\n'.join(lines)

    def dump_to_file(self, filename: str, fmt: Literal['t', 'b']) -> None:
        if fmt == 't':
            with open(filename, 'wt', encoding='utf-8') as file:
                file.write(self.format_str(None, None, 32, cursor=False))

        elif fmt == 'b':
            with open(filename, 'wb') as fileb:
                fileb.write(self.data)

    def __eq__(self, other: Buffer | object) -> bool:
        if isinstance(other, Buffer):
            return self.data == other.data
        return False

    def __bool__(self) -> bool:
        return not self.is_end()

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> int:
        return self.data[index]

    def __setitem__(self, index: int, value: int) -> None:
        assert isinstance(self.data, bytearray)
        self.data[index] = value

    def __bytes__(self) -> bytes:
        return bytes(self.data)

    @property
    def pos(self) -> int:
        assert (
            0 <= self._pos <= len(self.data)
        ), f'Internal buffer position error (len={len(self.data)} pos={self._pos})'
        return self._pos

    @pos.setter
    def pos(self, newpos: int) -> None:
        if newpos < 0 or newpos > len(self.data):  # allow set pos right after the end of data
            raise ValueError(f'Cannot set buffer position on {newpos} (len={len(self.data)})')
        self._pos = newpos

    def to_bytes(self) -> bytes:
        return bytes(self.data)

    def is_end(self) -> bool:
        return self._pos == len(self.data)

    def bytes_remains(self) -> int:
        return len(self.data) - self._pos

    def pop_pos(self) -> int:
        result = self._pos
        self._pos = self._position_stack.pop()
        return result

    def push_pos(self, pos: int = None) -> int:
        if pos is None:
            pos = self._pos
        result = self._pos
        self._position_stack.append(self._pos)
        self.pos = pos
        return result

    def read(self, n: int = None, pos: int = None) -> bytearray | bytes:
        if pos is not None:
            self.push_pos(pos)

        data = self.data
        _pos = self._pos

        if n is None:
            n = len(data) - _pos
        elif n < 0:
            n = len(data) - _pos + n

        assert n >= 0

        if _pos > len(data) - n:
            raise ValueError(
                f'Cannot read {n!r} bytes from buffer (pos={self._pos!r} len={len(self.data)!r})',
            )

        result = data[_pos : _pos + n]
        self._pos = _pos + n

        if pos is not None:
            self.pop_pos()
        return result

    def write(self, data: Collection[int], pos: int = None) -> None:
        assert isinstance(self.data, bytearray)
        if pos is not None:
            self.push_pos(pos)
        self.data[self._pos : self._pos + len(data)] = data
        self._pos += len(data)
        if pos is not None:
            self.pop_pos()

    def seek(self, pos: int) -> None:
        self.pos = pos

    def reset(self) -> None:
        self.pos = 0

    def skip(self, n: int) -> None:
        self.pos += n

    def load(self, buf: Buffer | IO[bytes]) -> None:
        self.write(buf.read())

    def save(self, buf: Buffer | IO[bytes]) -> None:
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

    def write_format(self, fmt: str, *values: Any, pos: int = None) -> None:
        return self.write(struct.pack(fmt, *values), pos=pos)

    def read_format(self, fmt: str, pos: int = None) -> tuple[Any, ...]:
        return struct.unpack(fmt, self.read(struct.calcsize(fmt), pos=pos))

    def write_struct(self, s: Struct, *values: Any, pos: int = None) -> None:
        return self.write(s.pack(*values), pos=pos)

    def read_struct(self, s: Struct, pos: int = None) -> tuple[Any, ...]:
        return s.unpack(self.read(s.size, pos=pos))

    def read_byte(self, pos: int = None) -> int:
        return self.read(1, pos=pos)[0]

    def write_byte(self, value: int, pos: int = None) -> None:
        return self.write(bytes((value,)), pos=pos)

    def read_bool(self, pos: int = None, *, __s: Struct = Struct('?')) -> bool:
        return self.read_struct(__s, pos=pos)[0]

    def write_bool(self, value: bool, pos: int = None, *, __s: Struct = Struct('?')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_char(self, pos: int = None, *, __s: Struct = Struct('b')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_char(self, value: int, pos: int = None, *, __s: Struct = Struct('b')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_uchar(self, pos: int = None, *, __s: Struct = Struct('B')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_uchar(self, value: int, pos: int = None, *, __s: Struct = Struct('B')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_short(self, pos: int = None, *, __s: Struct = Struct('<h')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_short(self, value: int, pos: int = None, *, __s: Struct = Struct('<h')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_ushort(self, pos: int = None, *, __s: Struct = Struct('<H')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_ushort(self, value: int, pos: int = None, *, __s: Struct = Struct('<H')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_int(self, pos: int = None, *, __s: Struct = Struct('<i')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_int(self, value: int, pos: int = None, *, __s: Struct = Struct('<i')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_uint(self, pos: int = None, *, __s: Struct = Struct('<I')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_uint(self, value: int, pos: int = None, *, __s: Struct = Struct('<I')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_long(self, pos: int = None, *, __s: Struct = Struct('<q')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_long(self, value: int, pos: int = None, *, __s: Struct = Struct('<q')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_ulong(self, pos: int = None, *, __s: Struct = Struct('<Q')) -> int:
        return self.read_struct(__s, pos=pos)[0]

    def write_ulong(self, value: int, pos: int = None, *, __s: Struct = Struct('<Q')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_float(self, pos: int = None, *, __s: Struct = Struct('<f')) -> float:
        return self.read_struct(__s, pos=pos)[0]

    def write_float(self, value: float, pos: int = None, *, __s: Struct = Struct('<f')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_double(self, pos: int = None, *, __s: Struct = Struct('<d')) -> float:
        return self.read_struct(__s, pos=pos)[0]

    def write_double(self, value: float, pos: int = None, *, __s: Struct = Struct('<d')) -> None:
        return self.write_struct(__s, value, pos=pos)

    def read_str(self, length: int = None) -> str:
        """
        length = None - read null-terminated string
        length = n - read n chars
        """
        if length is not None:
            return self.read(length).decode('utf-8')
        parts: list[str] = []
        while (x := self.read(1).decode('utf-8')) != '\0':
            parts.append(x)
        return ''.join(parts)

    def write_str(self, value: str, length: int = None) -> None:
        """
        length = None - write null-terminated string
        length = n - write string, filled with zeros
            if len(value) > length, string is truncated
        """
        if length is None:
            value += '\0'
        else:
            value = value[:length].ljust(length, '\0')
        self.write(value.encode('utf-8'))

    def read_wstr(self, length: int = None) -> str:
        if length is not None:
            return self.read(length * 2).decode('utf-16le')
        parts: list[str] = []
        while (x := self.read(2).decode('utf-16le')) != '\0':
            parts.append(x)
        return ''.join(parts)

    def write_wstr(self, value: str, length: int = None) -> None:
        if length is None:
            value += '\0'
        else:
            value = value[:length].ljust(length, '\0')
        self.write(value.encode('utf-16le'))

    def read_dcls(self, dcls: DataClass[T], *, memo: Memo = None) -> T:
        if memo is None:
            from .std.dataclass import Memo

            memo = Memo()
        return dcls.read(self, memo=memo)

    def write_dcls(self, dcls: DataClass[T], obj: T, *, memo: Memo = None) -> None:
        if memo is None:
            from .std.dataclass import Memo

            memo = Memo()
        dcls.write(self, obj, memo=memo)


BaseBuffer = Buffer
IBuffer = Buffer
OBuffer = Buffer
IDCBuffer = IBuffer
ODCBuffer = OBuffer
DCBuffer = IDCBuffer

#           BaseBuffer
#            |      |
#            |      |
#            V      V
#        IBuffer  OBuffer
#         |   |    |   |
#         |   |    |   |
#         V   V    V   V
#  IDCBuffer  Buffer  ODCBuffer
#           \        /
#            \      /
#             V    V
#            DCBuffer
