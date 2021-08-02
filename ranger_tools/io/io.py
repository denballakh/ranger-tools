from typing import Union, Iterable
import struct

__all__ = [
    'AbstractIBuffer',
    'Buffer',
]

class AbstractIBuffer:
    def __init__(self, data: list):
        self.data = data
        self.pos = 0

    def get(self):
        assert 0 <= self.pos < len(self.data)
        result = self.data[self.pos]
        self.pos += 1
        return result

    def end(self) -> bool:
        return 0 <= self.pos < len(self.data)


class Buffer:
    data: bytearray
    pos: int
    _position_stack: list[int]

    def __init__(self, obj: Union['Buffer', Iterable[int]] = b'', *, pos: int = 0):
        if isinstance(obj, bytearray):
            self.data = obj
        elif isinstance(obj, Buffer):
            self.data = obj.data
        else:
            self.data = bytearray(obj)

        self.pos = pos
        self._position_stack = []

    def __iter__(self):
        return iter(self.data)
        # i = 0
        # while i < len(self.data):
        #     yield self.data[i]
        #     i += 1

    def __str__(self) -> str:
        offset = 16
        return (
            f'Buffer('
            f'before={bytes(self.data[max(0, self.pos - offset): self.pos])!r}, '
            f'current={bytes(self.data[self.pos : self.pos + 1])!r} ({self.data[self.pos]}),'
            f'after={bytes(self.data[self.pos + 1 : min(self.pos + offset, len(self.data))])!r}), '
            f'len={len(self.data)}'
        )

    def __repr__(self) -> str:
        return f'Buffer({self.data!r}, pos={self.pos})'

    def __bool__(self) -> bool:
        return not self.is_end()

    def __len__(self) -> int:
        return len(self.data)

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
        if pos is None: pos = self.pos
        assert 0 <= pos <= len(self.data), f'Invalid buffer position: {self.pos}, len={len(self.data)}'
        result = self.pos
        self._position_stack.append(self.pos)
        self.pos = pos
        return result


    def read(self, n: Union[int, None] = None) -> bytearray:
        if n is None:
            n = len(self.data) - self.pos
        elif n < 0:
            n = len(self.data) - self.pos + n
        assert 0 <= self.pos <= len(self.data) - n, f'Invalid buffer position: {self.pos}, len={len(self.data)}'

        result = bytes(self.data[self.pos : self.pos + n])
        self.pos += n
        return result

    def write(self, data: Iterable[int]):
        assert 0 <= self.pos <= len(self.data), f'Invalid buffer position: {self.pos}, len={len(self.data)}'
        self.data[self.pos : self.pos + len(data)] = data
        self.pos += len(data)

    def seek(self, pos: int):
        self.pos = pos
        assert 0 <= self.pos <= len(self.data)

    def reset(self):
        self.pos = 0

    def skip(self, n):
        self.pos += n

    def load(self, buf: 'Buffer'):
        self.write(buf.read())

    def save(self, buf: 'Buffer'):
        buf.write(self.read())


    def load_file(self, path: str):
        with open(path, 'rb') as file:
            self.load(file)

    def save_file(self, path: str):
        with open(path, 'wb') as file:
            self.save(file)

    @classmethod
    def from_file(cls, path: str) -> 'Buffer':
        buf = cls()
        buf.load_file(path)
        return buf


    def write_format(self, fmt: str, *values: list['Any']):
        self.write(struct.pack(fmt, *values))

    def read_format(self, fmt: str) -> list['Any']:
        return struct.unpack(fmt, self.read(struct.calcsize(fmt)))


    def read_byte(self) -> int: return self.read_format('B')[0]
    def write_byte(self, value: int): return self.write_format('B', value)

    def read_bool(self) -> bool: return self.read_format('?')[0]
    def write_bool(self, value: bool): return self.write_format('?', value)

    def read_char(self) -> int: return self.read_format('b')[0]
    def write_char(self, value: int): return self.write_format('b', value)

    def read_uchar(self) -> int: return self.read_format('B')[0]
    def write_uchar(self, value: int): return self.write_format('B', value)

    def read_short(self) -> int: return self.read_format('<h')[0]
    def write_short(self, value: int): return self.write_format('<h', value)

    def read_ushort(self) -> int: return self.read_format('<H')[0]
    def write_ushort(self, value: int): return self.write_format('<H', value)

    def read_int(self) -> int: return self.read_format('<i')[0]
    def write_int(self, value: int): return self.write_format('<i', value)

    def read_uint(self) -> int: return self.read_format('<I')[0]
    def write_uint(self, value: int): return self.write_format('<I', value)

    def read_long(self) -> int: return self.read_format('<q')[0]
    def write_long(self, value: int): return self.write_format('<q', value)

    def read_ulong(self) -> int: return self.read_format('<Q')[0]
    def write_ulong(self, value: int): return self.write_format('<Q', value)

    def read_float(self) -> float: return self.read_format('<f')[0]
    def write_float(self, value: float): return self.write_format('<f', value)

    def read_double(self) -> float: return self.read_format('<d')[0]
    def write_double(self, value: float): return self.write_format('<d', value)

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
    def write_str(self, value: str, length: int = -1):
        if length == -1:
            value += '\0'
        else:
            value = value[ : length - 1]
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
    def write_wstr(self, value: str, length: int = -1):
        if length == -1:
            value += '\0'
        else:
            value = value[ : length - 1]
            value += (length - len(value)) * '\0'
        self.write(value.encode('utf-16le'))



