import zlib
import random

from .io import IBuffer, OBuffer
# from .common import bytes_to_uint, bytes_to_int, bytes_xor, int_to_bytes

__all__ = ['DAT', 'DATItem']

class DAT:
    _seed_xor = b'\x89\xc6\xe8\xb1' # 0xBE970BF1 4f5c0 reload

    _sr1_key =              b'\x00\x00\x00\x00'
    _reload_main_key =      b'\xfe\x77\x0a\xc9' # -922060802
    _reload_cache_key =     b'\x59\xe6\xfd\x72' # 1929242201
    _hd_main_key =          b'\x89\xc6\xe8\xb1' # -1310144887
    _hd_cache_key =         b'\x37\x3f\x8f\xea' # -359710921

    def __init__(self, root):
        self.root = root

    @staticmethod
    def _rand31pm(seed: int) -> int:
        while True:
            hi, lo = divmod(seed, 0x1f31d)
            seed = lo * 0x41a7 - hi * 0xb14
            if seed < 1:
                seed += 0x7fffffff
            yield seed - 1

    @staticmethod
    def decipher(data: bytes, seed: int) -> bytes:
        din = IBuffer.from_bytes(data)
        content_hash = din.read_uint()
        seed = din.read_int() ^ seed
        rnd = DAT._rand31pm(seed)
        dout = OBuffer()
        while not din.end():
            dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
        result = dout.to_bytes()
        assert zlib.crc32(result) == content_hash
        return result

    @staticmethod
    def cipher(data: bytes) -> bytes:
        seed = random.randint(0, 2**31 - 1)
        rnd = DAT._rand31pm(seed)
        dout = OBuffer()
        dout.write_uint(zlib.crc32(data))
        dout.write_int(seed ^ (-1310144887))
        din = IBuffer.from_bytes(data)
        while not din.end():
            dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
        result = dout.to_bytes()
        return result

    @staticmethod
    def decompress(data: bytes) -> bytes:
        din = IBuffer.from_bytes(data)
        zl01 = din.read(4)
        size = din.read_uint()
        buf = din.read()
        assert zl01 == b'ZL01'
        buf = zlib.decompress(buf)
        assert size == len(buf)
        return buf

    @staticmethod
    def compress(data: bytes) -> bytes:
        size = len(data)
        data = zlib.compress(data, level=9)
        dout = OBuffer()
        dout.write_bytes(b'ZL01')
        dout.write_uint(size)
        dout.write_bytes(data)
        return dout.to_bytes()

    @classmethod
    def from_bytes(cls, data: bytes) -> 'DAT':
        data = cls.decompress(cls.decipher(data, -1310144887))
        # b'\2\0\0' - метка блока (2) и название корня (пустая строка = 0 0)
        root = DATItem.from_bytes(b'\2\0\0' + data)
        return cls(root)

    def to_bytes(self) -> bytes:
        data = self.root.to_bytes()[len(self.root.name) * 2 + 3:]
        data = self.compress(data)
        data = self.cipher(data)
        return data

    def __repr__(self):
        return repr(self.root)

class DATItem:
    PAR = 1
    BLOCK = 2

    def __init__(self):
        self.type = None
        self.name: str = ''
        self.value: str = ''
        self.childs: list[DATItem] = []
        self.sort_type: int = None

    def __repr__(self) -> str:
        if self.type == self.PAR:
            return f'{self.name}={self.value}'

        if self.type == self.BLOCK:
            result = self.name
            result += ' ^{' if self.sort_type else ' ~{'
            result += '\n'
            for child in self.childs:
                chs = repr(child)
                for s in chs.split('\n'):
                    result += '    ' + s + '\n'
            result += '}'
            return result

        raise TypeError

    @classmethod
    def from_buffer(cls, din: IBuffer) -> 'DATItem':
        item = cls()
        item.type = din.read_byte()

        if item.type not in {cls.PAR, cls.BLOCK}:
            din.pos -= 1
            a = din.read(8)
            assert a == b'\0\0\0\0\1\0\0\0', f'Invalid sorted item prefix: {a}'
            item = cls.from_buffer(din)

        elif item.type == cls.PAR:
            item.name = din.read_wstr()
            item.value = din.read_wstr()

        elif item.type == cls.BLOCK:
            item.name = din.read_wstr()
            item.sort_type = din.read_byte()
            childs_cnt = din.read_uint()

            for _ in range(childs_cnt):
                child = cls.from_buffer(din)
                item.childs.append(child)

        return item

    @classmethod
    def from_bytes(cls, data: bytes) -> 'DATItem':
        return cls.from_buffer(IBuffer.from_bytes(data))

    def to_buffer(self, dout: OBuffer):
        dout.write_byte(self.type)
        if self.type == self.PAR:
            dout.write_wstr(self.name)
            dout.write_wstr(self.value)
        elif self.type == self.BLOCK:
            dout.write_wstr(self.name)
            dout.write_byte(self.sort_type)
            dout.write_uint(len(self.childs))

            for child in self.childs:
                if self.sort_type:
                    dout.write_bytes(b'\0\0\0\0\1\0\0\0')
                child.to_buffer(dout)
        else:
            raise TypeError

    def to_bytes(self) -> bytes:
        dout = OBuffer()
        self.to_buffer(dout)
        data = dout.to_bytes()
        return data




