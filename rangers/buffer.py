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
            # print(b.decode('utf-16le'))
            if b.decode('utf-16le') in _str_rus_chars:
                result.append(b.decode('utf-16le'))
                nxt = ' '
                continue

        except:
            pass

        if chr(byte) in _str_readable_chars:
            result.append(chr(byte))
        elif chr(byte) in _str_char_conv:
            result.append(_str_char_conv[chr(byte)])
        else:
            result.append('.')
    return ''.join(result)


def _part(s: str, n: int) -> list[str]:
    res: list[str] = []
    while s:
        res.append(s[:n])
        s = s[n:]
    return res


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

    def __repr__(self) -> str:
        return f'Buffer({self.data!r}, pos={self._pos})'

    def __eq__(self, other) -> bool:
        if isinstance(other, Buffer):
            return self.data == other.data
        return NotImplemented

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

    def read(self, n: int = None, pos: int = None) -> bytes:
        if pos is not None:
            self.push_pos(pos)

        if n is None:
            n = len(self.data) - self._pos
        elif n < 0:
            n = len(self.data) - self._pos + n

        assert n >= 0

        if not 0 <= self._pos <= len(self.data) - n:
            raise ValueError(
                f'Cannot read {n} bytes from buffer (pos={self._pos} len={len(self.data)})'
            )

        result = bytes(self.data[self._pos : self._pos + n])
        self._pos += n

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
        except struct.error as e:
            raise Exception(f'Error in struct.pack: fmt={fmt!r}, values={values!r}') from e
        if pos is not None:
            self.pop_pos()

    def read_format(self, fmt: str, pos: int = None) -> Any:
        if pos is not None:
            self.push_pos(pos)

        try:
            result = struct.unpack(fmt, self.read(struct.calcsize(fmt)))
        except struct.error as e:
            raise Exception(f'Error in struct.unpack: fmt={fmt!r}') from e

        if pos is not None:
            self.pop_pos()
        return result

    def read_byte(self, pos: int = None) -> int:
        return self.read_format('B', pos=pos)[0]

    def write_byte(self, value: int, pos: int = None) -> None:
        return self.write_format('B', value, pos=pos)

    def read_bool(self, pos: int = None) -> bool:
        return self.read_format('?', pos=pos)[0]

    def write_bool(self, value: bool, pos: int = None) -> None:
        return self.write_format('?', value, pos=pos)

    def read_char(self, pos: int = None) -> int:
        return self.read_format('b', pos=pos)[0]

    def write_char(self, value: int, pos: int = None) -> None:
        return self.write_format('b', value, pos=pos)

    def read_uchar(self, pos: int = None) -> int:
        return self.read_format('B', pos=pos)[0]

    def write_uchar(self, value: int, pos: int = None) -> None:
        return self.write_format('B', value, pos=pos)

    def read_short(self, pos: int = None) -> int:
        return self.read_format('<h', pos=pos)[0]

    def write_short(self, value: int, pos: int = None) -> None:
        return self.write_format('<h', value, pos=pos)

    def read_ushort(self, pos: int = None) -> int:
        return self.read_format('<H', pos=pos)[0]

    def write_ushort(self, value: int, pos: int = None) -> None:
        return self.write_format('<H', value, pos=pos)

    def read_int(self, pos: int = None) -> int:
        return self.read_format('<i', pos=pos)[0]

    def write_int(self, value: int, pos: int = None) -> None:
        return self.write_format('<i', value, pos=pos)

    def read_uint(self, pos: int = None) -> int:
        return self.read_format('<I', pos=pos)[0]

    def write_uint(self, value: int, pos: int = None) -> None:
        return self.write_format('<I', value, pos=pos)

    def read_long(self, pos: int = None) -> int:
        return self.read_format('<q', pos=pos)[0]

    def write_long(self, value: int, pos: int = None) -> None:
        return self.write_format('<q', value, pos=pos)

    def read_ulong(self, pos: int = None) -> int:
        return self.read_format('<Q', pos=pos)[0]

    def write_ulong(self, value: int, pos: int = None) -> None:
        return self.write_format('<Q', value, pos=pos)

    def read_float(self, pos: int = None) -> float:
        return self.read_format('<f', pos=pos)[0]

    def write_float(self, value: float, pos: int = None) -> None:
        return self.write_format('<f', value, pos=pos)

    def read_double(self, pos: int = None) -> float:
        return self.read_format('<d', pos=pos)[0]

    def write_double(self, value: float, pos: int = None) -> None:
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
