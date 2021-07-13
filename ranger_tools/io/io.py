from struct import pack, unpack

__all__ = [
    'IBuffer',
    'OBuffer',
    'AbstractIBuffer',
]

class IBuffer:
    data: bytes
    pos: int

    def __init__(self, data: bytes = b'', pos: int = 0):
        self.data: bytes = data
        self.pos: int = pos

    def __repr__(self) -> str:
        return f'IBuffer({self.data},{self.pos})'

    @classmethod
    def from_bytes(cls, data: bytes) -> 'IBuffer':
        """синоним конструктора, надо вырезать"""
        return cls(data)

    @classmethod
    def from_file(cls, path: str) -> 'IBuffer':
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def end(self) -> bool:
        return self.pos == len(self.data)

    def __len__(self) -> int:
        return len(self.data) - self.pos

    def skip(self, n: int = 1):
        self.pos += n

    def read(self, n: int = -1) -> bytes:
        if n == -1:
            n = len(self.data) - self.pos
        assert n >= 0
        assert self.pos + n <= len(self.data), '[IBuffer.read] Invalid size'
        result = self.data[self.pos : self.pos + n]
        self.pos += n
        return result

    def read_byte(self) -> int:
        return self.read(1)[0]

    def read_int(self, byteorder='little') -> int:
        return int.from_bytes(self.read(4), byteorder=byteorder, signed=True)

    def read_uint(self, byteorder='little') -> int:
        return int.from_bytes(self.read(4), byteorder=byteorder, signed=False)

    def read_char(self) -> str:
        return self.read(1).decode('utf-8')

    def read_wchar(self) -> str:
        return self.read(2).decode('utf-16le')

    def read_str(self, size: int = -1) -> str:
        result = ''

        c = self.read_char()
        while c != '\0':
            result += c
            c = self.read_char()

        if size != -1 and size is not None:
            self.pos += size - len(result) - 1

        return result

    def read_wstr(self, size: int = -1) -> str:
        result = ''

        c = self.read_wchar()
        while c != '\0':
            result += c
            c = self.read_wchar()

        if size != -1 and size is not None:
            self.pos += (size - len(result) - 1) * 2

        return result

    def read_float(self) -> float:
        data = self.read(4)
        return unpack('<f', data)[0]

    def read_double(self) -> float:
        data = self.read(8)
        return unpack('<d', data)[0]

    def read_bool(self) -> bool:
        return bool(self.read_byte())

    def read_unknown(self, typename: str, param = None) -> ...:
        if typename == 'int':
            return self.read_int()

        if typename == 'uint':
            return self.read_uint()

        if typename == 'byte':
            return self.read_byte()

        if typename == 'char':
            return self.read_char()

        if typename == 'wchar':
            return self.read_wchar()

        if typename == 'str':
            return self.read_str(param)

        if typename == 'wstr':
            return self.read_wstr(param)

        if typename == 'float':
            return self.read_float()

        if typename == 'double':
            return self.read_double()

        if typename == 'bool':
            return self.read_bool()

        if typename == 'bytes':
            return self.read(param)

        raise TypeError(f'Unknown value type: {typename!r}')



class OBuffer:
    data: bytearray

    def __init__(self, data: bytes = b''):
        if isinstance(data, OBuffer):
            self.data = OBuffer.data

        if isinstance(data, bytes):
            self.data = bytearray(data)

        if isinstance(data, bytearray):
            self.data = data

    def __repr__(self) -> str:
        return f'OBuffer({self.data!r})'

    def __len__(self) -> int:
        return len(self.data)

    def to_bytes(self) -> bytes:
        return bytes(self.data)

    def to_file(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())

    def write_byte(self, n: int = 0):
        assert 0 <= n <= 255
        self.data.append(n)

    def write_bytes(self, data: bytes):
        self.data.extend(data)

    def write_int(self, n: int, byteorder: str = 'little'):
        self.write_bytes(n.to_bytes(4, byteorder=byteorder, signed=True))

    def write_uint(self, n: int, byteorder: str = 'little'):
        assert n >= 0
        self.write_bytes(n.to_bytes(4, byteorder=byteorder, signed=False))

    def write_char(self, s: str):
        assert len(s) == 1
        self.write_bytes(s.encode('utf-8'))

    def write_wchar(self, s: str):
        assert len(s) == 1
        self.write_bytes(s.encode('utf-16le'))

    def write_str(self, s: str, size: int = -1):
        if size == -1 or size is None:
            self.write_bytes(s.encode('utf-8') + b'\0')
        else:
            self.write_bytes(s[:size].encode('utf-8') + (size - len(s)) * b'\0')

    def write_wstr(self, s: str, size: int = -1):
        if size == -1 or size is None:
            self.write_bytes(s.encode('utf-16le') + b'\0\0')
        else:
            self.write_bytes(s[:size].encode('utf-16le') + (size - len(s)) * b'\0\0')

    def write_float(self, f: float):
        self.write_bytes(pack('<f', f))

    def write_double(self, f: float):
        self.write_bytes(pack('<d', f))

    def write_bool(self, b: bool):
        self.write_byte(int(b))

    def write_unknown(self, typename: str, value: object, param = None):
        if typename == 'int':
            assert isinstance(value, int)
            self.write_int(value)
            return

        if typename == 'uint':
            assert isinstance(value, int)
            assert value >= 0
            self.write_uint(value)
            return

        if typename == 'byte':
            assert isinstance(value, int)
            assert 0 <= value < 256
            self.write_byte(value)
            return

        if typename == 'char':
            assert isinstance(value, str)
            assert len(value) == 1
            self.write_char(value)
            return

        if typename == 'wchar':
            assert isinstance(value, str)
            assert len(value) == 1
            self.write_wchar(value)
            return

        if typename == 'str':
            assert isinstance(value, str)
            self.write_str(value, param)
            return

        if typename == 'wstr':
            assert isinstance(value, str)
            self.write_wstr(value, param)
            return

        if typename == 'float':
            assert isinstance(value, float), (value, self)
            self.write_float(value)
            return

        if typename == 'double':
            assert isinstance(value, float)
            self.write_double(value)
            return

        if typename == 'bool':
            assert isinstance(value, bool)
            self.write_bool(value)
            return

        if typename == 'bytes':
            assert isinstance(value, bytes)
            self.write_bytes(value)
            return

        raise TypeError(f'Unknown value type: {typename!r}')



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

from typing import Union

class Buffer:
    data: bytearray
    pos: int

    def __init__(self, obj: Union[bytes, bytearray, 'Buffer', 'Iterable'] = b'', *, pos: int = 0):
        if isinstance(obj, bytearray):
            self.data = obj

        elif isinstance(obj, Buffer):
            self.data = obj.data

        else:
            self.data = bytearray(obj)

        self.pos = pos

    def read(self, n: Union[int, None] = None) -> bytearray:
        if n is None:
            n = len(self.data) - self.pos
        elif n < 0:
            n = len(self.data) - self.pos + n
        return self.data[self.pos : self.pos + n]

    def write(self, data: Union[bytes, bytearray]):
        self.data[self.pos : self.pos + len(data)] = data
        self.pos += len(data)

    def __iter__(self):
        i = self.pos
        while i < len(self.data):
            yield self.data[i]
            i += 1

    def load(self, buf: 'Buffer'):
        self.write(buf.read())

    def save(self, buf: 'Buffer'):
        buf.write(self.read())


    def load_file(self, path: str):
        with open(path, 'rb') as file:
            self.write(file.read())

    def save_file(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.read())
