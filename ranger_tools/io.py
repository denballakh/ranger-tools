__all__ = ['IBuffer', 'OBuffer']

class IBuffer:
    def __init__(self):
        self.data: bytes = b''
        self.pos: int = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> 'IBuffer':
        buf = cls()
        buf.data = data
        return buf

    @classmethod
    def from_file(cls, path: str) -> 'IBuffer':
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def end(self) -> bool:
        return self.pos == len(self.data)

    def read(self, n: int = -1) -> bytes:
        if n == -1:
            n = len(self.data) - self.pos
        assert n >= 0
        assert self.pos + n <= len(self.data), 'Invalid size'
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
        return chr(self.read_byte())

    def read_wchar(self) -> str:
        a = self.read_char()
        b = self.read_char()
        assert b == '\x00'
        return a

    def read_str(self) -> str:
        result = ''

        c = self.read_char()
        while c != '\x00':
            result += c
            c = self.read_char()

        return result

    def read_wstr(self) -> str:
        result = ''

        c = self.read_wchar()
        while c != '\x00':
            result += c
            c = self.read_wchar()

        return result

class OBuffer:
    def __init__(self):
        self.data: bytearray = bytearray()

    def to_bytes(self) -> bytes:
        return bytes(self.data)

    def to_file(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())

    def write_byte(self, n: int):
        assert 0 <= n <= 255
        self.data.append(n)

    def write_bytes(self, data: bytes):
        for b in data:
            self.write_byte(b)

    def write_int(self, n: int, byteorder: str = 'little'):
        self.write_bytes(n.to_bytes(4, byteorder=byteorder, signed=True))

    def write_uint(self, n: int, byteorder: str = 'little'):
        self.write_bytes(n.to_bytes(4, byteorder=byteorder, signed=False))

    def write_str(self, s: str):
        for c in s:
            self.write_byte(ord(c))
        self.write_byte(0)

    def write_wstr(self, s: str):
        for c in s:
            self.write_byte(ord(c))
            self.write_byte(0)
        self.write_byte(0)
        self.write_byte(0)


