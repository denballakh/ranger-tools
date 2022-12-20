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



__all__ = (
    'BaseBuffer',
    'IBuffer',
    'OBuffer',
    'Buffer',
)

BT = TypeVar('BT', bound='BaseBuffer')

_hex_char_conv: dict[str, str] = {
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

_str_rus_chars: set[str] = set('абвгдеёжзийклмонпрстуфхцчшщъыьэюя' + 'АБВГДЕЁЖЗИЙКЛМОНПРСТУФХЦЧШЩЪЫЬЭЮЯ')

_str_readable_chars: set[str] = set(
    '!"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
)

_str_char_conv: dict[int | str, str] = {
    ' ': '_',
    '\0': ' ',
    # '\xFF': '#',
}

# _pg = [
#     ['│', '─'],
#     ['┌', '┬', '┐'],
#     ['├', '┼', '┤'],
#     ['└', '┴', '┘'],
# ]


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
            self.data = obj  # note: bytearray is mutable

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
        # check if buffer is not exhausted
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
        """
        Format buffer representation like this:
        ┌──────┬─────────────────────────────────────────────────┬──────────────────┐
        │ 0x00 │ .. .1 .2 .3 .4 .5 .6 .7 .8 .9 .A .B .C .D .E .F │  ............... │
        │ 0x10 │ 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F │ ................ │
        │ 0x20 │ 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F │ _!"#$%&'()*+,-./ │
        │ 0x30 │ 30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F │ 0123456789:;<=>? │
        │ 0x40 │ 40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F │ @ABCDEFGHIJKLMNO │
        │ 0x48 ├─────────────────────────╨╨──────────────────────┼─────────╨────────┤
        │ 0x50 │ 50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F │ PQRSTUVWXYZ[\]^_ │
        │ 0x60 │ 60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F │ `abcdefghijklmno │
        │ 0x70 │ 70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F │ pqrstuvwxyz{|}~. │
        │ 0x80 │ 80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F │ ................ │
        └──────┴─────────────────────────────────────────────────┴──────────────────┘

        from rangers.std.buffer import Buffer; b = Buffer(bytes(range(256))); b.pos = 72; print(b)
        """
        assert width > 0, width
        assert before is None or before > 0, before
        assert after is None or after > 0, after
        n = width
        lines = []
        rpos = self.pos // n * n

        if before is None:
            before = rpos // n

        if after is None:
            after = (len(self.data) // n * n - rpos) // n

        hexlen = max(len(hex(rpos + n * after)[2:]), 1)

        def addr_to_hex(addr: int) -> str:
            return f'0x{addr:0{hexlen}X}'

        def top_bottom_line(*, top: bool = False, bottom: bool = False) -> str:
            assert top ^ bottom, f'Exactly one of "top" and "bottom" must be True'
            l = '┌' if top else '└'
            m = '┬' if top else '┴'
            r = '┐' if top else '┘'

            return l + '─' * (hexlen + 4) + m + '─' * (3 * n + 1) + m + '─' * (n + 2) + r

        lines.append(top_bottom_line(top=True))

        for line_no in range(-before, after + 1):
            line_start = rpos + line_no * n
            if line_start < 0 or line_start > len(self.data):
                continue
            line = '│ '
            line += addr_to_hex(line_start)
            line += ' │ '

            chunk = self.data[line_start : line_start + n]
            line += _bytes_to_hex(chunk).ljust(3 * n - 1)
            line += ' │ '
            line += _bytes_to_str(chunk).ljust(n)
            line += ' │'
            line_len = len(line)
            lines.append(line)

            if cursor and line_no == 0:
                cursor_s = '╨╨'

                line = '│ '
                line += addr_to_hex(self.pos)
                line += ' ├─'
                cursor_pos = self.pos % n * 3
                line += '─' * cursor_pos + cursor_s
                line += '───' * (n - self.pos % n - 1)
                line += '─┼─'
                line += '─' * (self.pos % n) + '╨'
                line = line.ljust(line_len - 2, '─')
                line += '─┤'
                lines.append(line)

        lines.append(top_bottom_line(bottom=True))

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
        pos: int | None = None,
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


class IBuffer(BaseBuffer):
    __slots__ = ()
    data: bytes

    # def __init__(self, obj: BaseBuffer | bytes | bytearray, /) -> None:
    #     if isinstance(obj, bytes):
    #         BaseBuffer.__init__(self, bytes(obj))
    #     else:
    #         BaseBuffer.__init__(self, obj)

    def read(self, n: int | None = None, /) -> bytearray | bytes:

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

    def read_format(self, fmt: str, /) -> Any:
        return struct.unpack(fmt, self.read(struct.calcsize(fmt)))[0]

    def read_struct(self, s: Struct, /) -> Any:
        return s.unpack(self.read(s.size))[0]

    def read_byte(self, /) -> int:
        return self.read(1)[0]

    def read_bool(self, /, *, _s: Struct = Struct('?')) -> bool:
        return _s.unpack(self.read(_s.size))[0]

    def read_i8(self, /, *, _s: Struct = Struct('b')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_u8(self, /, *, _s: Struct = Struct('B')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_i16(self, /, *, _s: Struct = Struct('<h')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_u16(self, /, *, _s: Struct = Struct('<H')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_i32(self, /, *, _s: Struct = Struct('<i')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    def read_u32(self, /, *, _s: Struct = Struct('<I')) -> int:
        return _s.unpack(self.read(_s.size))[0]

    # def read_long(self, /, *, _s: Struct = Struct('<q')) -> int:
    #     return _s.unpack(self.read(_s.size))[0]

    # def read_ulong(self, /, *, _s: Struct = Struct('<Q')) -> int:
    #     return _s.unpack(self.read(_s.size))[0]

    def read_f32(self, /, *, _s: Struct = Struct('<f')) -> float:
        return _s.unpack(self.read(_s.size))[0]

    def read_f64(self, /, *, _s: Struct = Struct('<d')) -> float:
        return _s.unpack(self.read(_s.size))[0]

    def read_str(self, /, length: int | None = None) -> str:
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

    def read_wstr(self, /, length: int | None = None) -> str:
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

class OBuffer(BaseBuffer):
    __slots__ = ()
    data: bytearray

    def __init__(self, obj: BaseBuffer | bytes | bytearray = b'', /) -> None:
        if isinstance(obj, bytes):
            BaseBuffer.__init__(self, bytearray(obj))
        elif isinstance(obj, BaseBuffer) and isinstance(obj.data, bytes):
            BaseBuffer.__init__(self, bytearray(obj.data))
        else:
            BaseBuffer.__init__(self, obj)

    def push_pos(
        self,
        pos: int | None = None,
        /,
        *,
        expand: bool = False,
    ) -> int:
        if expand and pos is not None:
            self.data.extend(bytes(pos - len(self.data)))
        return super().push_pos(pos)

    def write(self, data: Collection[int], /) -> None:
        if self._pos == len(self.data):
            # TODO: benchmark it to make sure that `bytearray.extend(x)` is faster than `bytearray[a:b]=x`
            self.data.extend(data)
        else:
            self.data[self._pos : self._pos + len(data)] = data
        self._pos += len(data)

    def write_format(
        self,
        fmt: str,
        *values: Any,
    ) -> None:
        return self.write(struct.pack(fmt, *values))

    def write_struct(self, s: Struct, value: Any, /) -> None:
        return self.write(s.pack(value))

    def write_byte(self, value: int, /) -> None:
        return self.write((value,))

    def write_bool(self, value: bool, /, *, _s: Struct = Struct('?')) -> None:
        return self.write(_s.pack(value))

    def write_i8(self, value: int, /, *, _s: Struct = Struct('b')) -> None:
        return self.write(_s.pack(value))

    def write_u8(self, value: int, /, *, _s: Struct = Struct('B')) -> None:
        return self.write(_s.pack(value))

    def write_i16(self, value: int, /, *, _s: Struct = Struct('<h')) -> None:
        return self.write(_s.pack(value))

    def write_u16(self, value: int, /, *, _s: Struct = Struct('<H')) -> None:
        return self.write(_s.pack(value))

    def write_i32(self, value: int, /, *, _s: Struct = Struct('<i')) -> None:
        return self.write(_s.pack(value))

    def write_u32(self, value: int, /, *, _s: Struct = Struct('<I')) -> None:
        return self.write(_s.pack(value))

    # def write_long(self, value: int, /, *, _s: Struct = Struct('<q')) -> None:
    #     return self.write(_s.pack(value))

    # def write_ulong(self, value: int, /, *, _s: Struct = Struct('<Q')) -> None:
    #     return self.write(_s.pack(value))

    def write_f32(self, value: float, /, *, _s: Struct = Struct('<f')) -> None:
        return self.write(_s.pack(value))

    def write_f64(self, value: float, /, *, _s: Struct = Struct('<d')) -> None:
        return self.write(_s.pack(value))

    def write_str(self, value: str, length: int | None = None) -> None:
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

    def write_wstr(self, value: str, length: int | None = None) -> None:
        if length is None:
            value += '\0'
        else:
            value = value[:length].ljust(length, '\0')
        self.write(value.encode('utf-16le'))


class Buffer(OBuffer, IBuffer):
    __slots__ = ()
    data: bytearray

