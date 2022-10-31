from __future__ import annotations
from typing import (
    Iterator,
    Any,
    TypeVar,
    TYPE_CHECKING,
    Literal,
    Collection,
)
from pathlib import Path
import struct
from struct import Struct

try:
    from mypy_extensions import trait
except ImportError:
    _T = TypeVar('_T')

    def trait(cls: _T) -> _T:
        return cls


if TYPE_CHECKING:
    from .dataclass import DataClass, Memo

from .._drafts.inline import inline_builtins, inline_method, inline_var, inline_attr

__all__ = (
    'BaseBuffer',
    'IBuffer',
    'OBuffer',
    'Buffer',
)

T = TypeVar('T')
BT = TypeVar('BT', bound='BaseBuffer')
# FBT = TypeVar('FBT', bound='FastBuffer')
TData_co = TypeVar('TData_co', bound=bytes | bytearray, covariant=True)

_s: struct.Struct = Struct('?')

_hex_char_conv: dict[int | str, str] = {
    '\x00': '..',
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


def _bytes_to_hex(d: bytes | bytearray, /) -> str:
    result: list[str] = []
    for byte in d:
        result.append(_hex_char_conv.get(chr(byte), f'{byte:02X}'))
    return ' '.join(result)


def _bytes_to_str(d: bytes | bytearray, /) -> str:
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

        except (UnicodeError, IndexError):
            pass

        if chr(byte) in _str_readable_chars:
            result.append(chr(byte))
        elif chr(byte) in _str_char_conv:
            result.append(_str_char_conv[chr(byte)])
        else:
            result.append('.')
    return ''.join(result)



class BaseBuffer:
    __slots__ = ('data', '_pos', '_position_stack')

    data: bytearray | bytes
    _pos: int
    _position_stack: list[int]

    def __init__(self, obj: BaseBuffer | bytes | bytearray = b'', /) -> None:
        if isinstance(obj, (bytes, bytearray)):
            self.data = obj  # bytearray is mutable

        elif isinstance(obj, BaseBuffer):
            self.data = obj.data  # it will share instances of data between instances of Buffer

        else:
            raise TypeError(type(obj))

        self.pos = 0
        self._position_stack = []

    def __iter__(self, /) -> Iterator[int]:
        return iter(self.data)

    def __bytes__(self, /) -> bytes:
        return bytes(self.data)

    def __str__(self, /) -> str:
        return self.format_str()

    def __bool__(self, /) -> bool:
        return self._pos < len(self.data)

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__}({self.data!r}, pos={self._pos!r})'

    def __len__(self, /) -> int:
        return len(self.data)

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

    @property
    def pos(self, /) -> int:
        assert (
            0 <= self._pos <= len(self.data)
        ), f'Internal buffer position error (len={len(self.data)} pos={self._pos})'
        return self._pos

    @pos.setter
    def pos(self, newpos: int, /) -> None:
        if newpos < 0 or newpos > len(self.data):  # allow set pos right after the end of data
            raise ValueError(f'Cannot set buffer position on {newpos} (len={len(self.data)})')
        self._pos = newpos

    def pop_pos(self, /) -> int:
        result = self._pos
        self._pos = self._position_stack.pop()
        return result

    def push_pos(
        self,
        pos: int = None,
        /,
    ) -> int:
        if pos is None:
            pos = self._pos
        result = self._pos
        self._position_stack.append(self._pos)
        self.pos = pos
        return result

    @classmethod
    def from_file(cls: type[BT], path: Path, /) -> BT:
        with open(path, 'rb') as file:
            data = file.read()
        return cls(data)

    def dump_to_file(self, filename: Path, fmt: Literal['t', 'b']) -> None:
        if fmt == 't':
            with open(filename, 'wt', encoding='utf-8') as file:
                file.write(self.format_str(None, None, 32, cursor=False))

        elif fmt == 'b':
            with open(filename, 'wb') as fileb:
                fileb.write(self.data)


@trait
class IBuffer(BaseBuffer):
    __slots__ = ()
    data: bytes

    # def __init__(self, obj: BaseBuffer | bytes | bytearray, /) -> None:
    #     if isinstance(obj, bytes):
    #         BaseBuffer.__init__(self, bytes(obj))
    #     else:
    #         BaseBuffer.__init__(self, obj)

    # @inline_builtins
    # @inline_method('self', 'push_pos', BaseBuffer.push_pos)
    # @inline_method('self', 'pop_pos', BaseBuffer.pop_pos)
    def read(self, n: int = None, /) -> bytearray | bytes:

        data = self.data
        first = self._pos

        if n is None:
            last = len(data)
        elif n < 0:
            last = len(data) + n
        else:
            last = first + n

        if last > len(data):
            raise ValueError(
                f'Cannot read {n!r} bytes from buffer (pos={self._pos!r} len={len(self.data)!r})',
            )

        self._pos = last
        return data[first:last]

    # @inline_method('self', 'read', read)
    # @inline_attr('struct', 'unpack', struct.unpack)
    # @inline_attr('struct', 'calcsize', struct.calcsize)
    def read_format(self, fmt: str, /) -> Any:
        return struct.unpack(fmt, self.read(struct.calcsize(fmt)))[0]

    # @inline_method('self', 'read', read)
    # @inline_method('s', 'unpack', Struct.unpack)
    def read_struct(self, s: Struct, /) -> Any:
        return s.unpack(self.read(s.size))[0]

    # @inline_method('self', 'read', read)
    def read_byte(self, /) -> int:
        return self.read(1)[0]

    def read_bool(self, /, *, _s: Struct = Struct('?')) -> bool:
        return _s.unpack(self.read(_s.size))[0]

    def read_char(self, /, *, _s: Struct = Struct('b')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_uchar(self, /, *, _s: Struct = Struct('B')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_short(self, /, *, _s: Struct = Struct('<h')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_ushort(self, /, *, _s: Struct = Struct('<H')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_int(self, /, *, _s: Struct = Struct('<i')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_uint(self, /, *, _s: Struct = Struct('<I')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_long(self, /, *, _s: Struct = Struct('<q')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_ulong(self, /, *, _s: Struct = Struct('<Q')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_float(self, /, *, _s: Struct = Struct('<f')) -> float:
        return _s.unpack(self.read(_s.size))[0]

    def read_double(self, /, *, _s: Struct = Struct('<d')) -> float:
        return _s.unpack(self.read(_s.size))[0]

    # @inline_method('self', 'read', read)
    def read_str(self, /, length: int = None) -> str:
        if length is not None:
            return self.read(length).decode('utf-8')

        pos = self.pos
        while self.read(1) != b'\0':
            pass
        length = self.pos - pos - 1
        self.pos = pos

        res = self.read(length).decode('utf-8')
        self.pos += 1
        return res

    # @inline_method('self', 'read', read)
    def read_wstr(self, /, length: int = None) -> str:
        if length is not None:
            return self.read(length << 1).decode('utf-16le')

        pos = self.pos
        while self.read(2) != b'\0\0':
            pass
        length = self.pos - pos - 2
        self.pos = pos

        res = self.read(length).decode('utf-16le')
        self.pos += 2
        return res

    def read_dcls(self, dcls: DataClass[T], *, memo: Memo = None) -> T:
        if memo is None:
            from .dataclass import Memo

            memo = Memo()
        return dcls.read(self, memo=memo)


@trait
class OBuffer(BaseBuffer):
    __slots__ = ()
    data: bytearray

    def __init__(self, obj: BaseBuffer | bytes | bytearray = b'', /) -> None:
        if isinstance(obj, bytes):
            BaseBuffer.__init__(self, bytearray(obj))
        elif isinstance(obj, BaseBuffer) and isinstance(obj.data, bytes):
            BaseBuffer.__init__(self, bytearray(obj.data))
        else:
            BaseBuffer.__init__(self, obj)  # type: ignore[unreachable]

    def push_pos(
        self,
        pos: int = None,
        /,
        *,
        expand: bool = False,
    ) -> int:
        if expand and pos is not None:
            self.data.extend(bytes(pos - len(self.data)))
        return super().push_pos(pos)

    # @inline_builtins
    # @inline_method('self', 'push_pos', BaseBuffer.push_pos)
    # @inline_method('self', 'pop_pos', BaseBuffer.pop_pos)
    def write(self, data: Collection[int], /) -> None:
        self.data[self._pos : self._pos + len(data)] = data
        self._pos += len(data)

    # @inline_method('self', 'write', write)
    # @inline_method('struct', 'pack', struct.pack)
    def write_format(
        self,
        fmt: str,
        *values: Any,
    ) -> None:
        return self.write(struct.pack(fmt, *values))

    # @inline_method('self', 'write', write)
    # @inline_method('s', 'pack', Struct.pack)
    def write_struct(self, s: Struct, value: Any, /) -> None:
        return self.write(s.pack(value))

    # @inline_method('self', 'write', write)
    def write_byte(self, value: int, /) -> None:
        return self.write((value,))

    def write_bool(self, value: bool, /, *, _s: Struct = Struct('?')) -> None:
        return self.write(_s.pack(value))

    def write_char(self, value: int, /, *, _s: Struct = Struct('b')) -> None:
        return self.write(_s.pack(value))

    def write_uchar(self, value: int, /, *, _s: Struct = Struct('B')) -> None:
        return self.write(_s.pack(value))

    def write_short(self, value: int, /, *, _s: Struct = Struct('<h')) -> None:
        return self.write(_s.pack(value))

    def write_ushort(self, value: int, /, *, _s: Struct = Struct('<H')) -> None:
        return self.write(_s.pack(value))

    def write_int(self, value: int, /, *, _s: Struct = Struct('<i')) -> None:
        return self.write(_s.pack(value))

    def write_uint(self, value: int, /, *, _s: Struct = Struct('<I')) -> None:
        return self.write(_s.pack(value))

    def write_long(self, value: int, /, *, _s: Struct = Struct('<q')) -> None:
        return self.write(_s.pack(value))

    def write_ulong(self, value: int, /, *, _s: Struct = Struct('<Q')) -> None:
        return self.write(_s.pack(value))

    def write_float(self, value: float, /, *, _s: Struct = Struct('<f')) -> None:
        return self.write(_s.pack(value))

    def write_double(self, value: float, /, *, _s: Struct = Struct('<d')) -> None:
        return self.write(_s.pack(value))

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

    def write_wstr(self, value: str, length: int = None) -> None:
        if length is None:
            value += '\0'
        else:
            value = value[:length].ljust(length, '\0')
        self.write(value.encode('utf-16le'))

    def write_dcls(self, dcls: DataClass[T], obj: T, *, memo: Memo = None) -> None:
        if memo is None:
            from .dataclass import Memo

            memo = Memo()
        dcls.write(self, obj, memo=memo)


class Buffer(OBuffer, IBuffer):
    __slots__ = ()
    data: bytearray
