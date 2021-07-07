import zlib
import random

from .io import IBuffer, OBuffer, AbstractIBuffer
# from .common import bytes_to_uint, bytes_to_int, bytes_xor, int_to_bytes

__all__ = ['DAT']

class DAT:
    keys = {
        'SR1': 0,
        'ReloadMain': 1050086386,
        'ReloadCache': 1929242201,
        'HDMain': -1310144887,
        'HDCache': -359710921,
    }
    format_seeds = {
        'ReloadMain': 955121797,
        'ReloadCache': 1954868526,
        'HDMain': -1215181314,
        'HDCache': -319409088,
    }

    def __init__(self, root):
        self.root = root
        self.fmt = None

    def __repr__(self):
        return self.to_str()

    @staticmethod
    def _rand31pm(seed: int) -> int:
        while True:
            hi, lo = divmod(seed, 0x1f31d)
            seed = lo * 0x41a7 - hi * 0xb14
            if seed < 1:
                seed += 0x7fffffff
            yield seed - 1

    @staticmethod
    def decipher(data: bytes, key: int) -> bytes:
        din = IBuffer.from_bytes(data)
        content_hash = din.read_uint()
        seed = din.read_int() ^ key
        print(seed)
        rnd = DAT._rand31pm(seed)
        dout = OBuffer()
        while not din.end():
            dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
        result = dout.to_bytes()
        assert zlib.crc32(result) == content_hash
        return result

    @staticmethod
    def cipher(data: bytes, fmt: str) -> bytes:
        seed = DAT.format_seeds[fmt]
        key = DAT.keys[fmt]

        rnd = DAT._rand31pm(seed)
        dout = OBuffer()
        dout.write_uint(zlib.crc32(data))
        dout.write_int(seed ^ key)
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
        assert zl01 == b'ZL01', f'Invalid ZL01 header: {zl01}'
        buf = zlib.decompress(buf)
        assert size == len(buf), f'Invalid decompressed size: {size} != {len(buf)}'
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

    @staticmethod
    def guess_format(data: bytes, check_hash: bool = False) -> int:
        din = IBuffer.from_bytes(data)
        content_hash = din.read(4) # content hash
        seed_ciphered = din.read_int()
        zl01_ciphered = din.read(4)

        for keyname, key in DAT.keys.items():
            din = IBuffer.from_bytes(zl01_ciphered)
            rnd = DAT._rand31pm(seed_ciphered ^ key)

            dout = OBuffer()
            while not din.end():
                dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
            zl01 = dout.to_bytes()

            if zl01 != b'ZL01':
                continue
            if not check_hash:
                return keyname

            din = IBuffer.from_bytes(data)
            _ = din.read_uint()
            _ = din.read_int()
            rnd = DAT._rand31pm(seed_ciphered ^ key)

            dout = OBuffer()
            while not din.end():
                dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
            result = dout.to_bytes()

            if zlib.crc32(result) == content_hash:
                return keyname

        return None

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str = None) -> 'DAT':
        if fmt not in cls.keys:
            fmt = cls.guess_format(data)
        assert fmt in cls.keys, f'Invalid dat format: {fmt}'
        data_d = cls.decompress(cls.decipher(data, key=cls.keys[fmt]))
        # print(data_d)
        # b'\2\0\0' - метка блока (2) и название корня (пустая строка = 0 0)
        root = DATItem.from_bytes(b'\2\0\0' + data_d, fmt=fmt)
        dat = cls(root)
        dat.fmt = fmt
        return dat

    def to_bytes(self, fmt: str) -> bytes:
        prefixlen = (len(self.root.name) + 1) * 2 + 1
        data = self.root.to_bytes(fmt=fmt)[prefixlen : ]
        # print(data)
        data = self.compress(data)
        if fmt is None:
            fmt = self.fmt
        assert fmt in self.keys, f'Invalid dat format: {fmt}'
        data = self.cipher(data, fmt=fmt)
        return data

    @classmethod
    def from_str(cls, s: str) -> 'DAT':
        wrapped = ' ^{\n' + s + '\n}\n'
        root = DATItem.from_str(wrapped)
        return cls(root)

    def to_str(self) -> str:
        return self.root.to_str(isroot=True)

    @classmethod
    def from_dat(cls, path: str, fmt: str = None) -> 'DAT':
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data, fmt=fmt)

    def to_dat(self, path: str, fmt: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes(fmt=fmt))

    @classmethod
    def from_txt(cls, path: str) -> 'DAT':
        with open(path, 'rt') as file:
            s = file.read()
        return cls.from_str(s)

    def to_txt(self, path: str):
        with open(path, 'wt') as file:
            file.write(self.to_str())


class DATItem:
    PAR = 1
    BLOCK = 2

    def __init__(self):
        self.type = None
        self.name: str = ''
        self.value: str = ''
        self.childs: list[DATItem] = []
        self.sorted: int = None

    def __repr__(self) -> str:
        return self.to_str()

    @classmethod
    def from_str_buffer(cls, buf: AbstractIBuffer) -> 'DATItem':
        s = buf.get()
        assert '\n' not in s
        s, _, comment = s.partition('//')
        s = s.strip()

        if '=' in s:
            name, _, value = s.partition('=')
            assert ' ' not in name
            item = cls()
            item.type = cls.PAR
            item.name = name
            item.value = value
            return item

        if '{' in s:
            name = s.rstrip(' ~^{')
            item = cls()
            item.type = cls.BLOCK
            item.name = name
            if '~' in s:
                item.sorted = 0
            elif '^' in s:
                item.sorted = 1
            else:
                raise ValueError

            while True:
                if buf.get().partition('//')[0].strip() == '}':
                    break
                buf.pos -= 1

                child = cls.from_str_buffer(buf)
                if child is not None:
                    item.childs.append(child)

            return item

        return None


    @classmethod
    def from_str(cls, s: str) -> 'DATItem':
        buf = AbstractIBuffer(s.split('\n'))
        return cls.from_str_buffer(buf)

    def to_str(self, isroot=False) -> str:
        if self.type == self.PAR:
            return f'{self.name}={self.value}'

        if self.type == self.BLOCK:
            result = ''
            if isroot:
                tab = ''
            else:
                tab = '    '
                result += self.name + ' ' + ('~', '^')[self.sorted] + '{\n'

            for child in self.childs:
                chs = repr(child)
                for s in chs.split('\n'):
                    result += tab + s + '\n'

            if not isroot:
                result += '}'

            return result

        raise TypeError

    @classmethod
    def from_buffer(cls, din: IBuffer, fmt: str) -> 'DATItem':
        item = cls()
        item.type = din.read_byte()


        if item.type not in {cls.PAR, cls.BLOCK}:
            din.pos -= 1
            a = din.read(8)
            assert a == b'\0\0\0\0\1\0\0\0', f'Invalid sorted item prefix: {a}'
            item = cls.from_buffer(din, fmt=fmt)

        elif item.type == cls.PAR:
            item.name = din.read_wstr()
            item.value = din.read_wstr()

        elif item.type == cls.BLOCK:
            item.name = din.read_wstr()
            if fmt in {'HDMain', 'ReloadMain'}:
                item.sorted = din.read_byte()
            else:
                item.sorted = 0
            childs_cnt = din.read_uint()

            for _ in range(childs_cnt):
                child = cls.from_buffer(din, fmt=fmt)
                item.childs.append(child)

        return item

    def to_buffer(self, dout: OBuffer, fmt: str):
        dout.write_byte(self.type)
        if self.type == self.PAR:
            dout.write_wstr(self.name)
            dout.write_wstr(self.value)
        elif self.type == self.BLOCK:
            dout.write_wstr(self.name)
            if fmt in {'HDMain', 'ReloadMain'}:
                dout.write_byte(self.sorted)
            dout.write_uint(len(self.childs))

            for child in self.childs:
                if fmt in {'HDMain', 'ReloadMain'} and self.sorted:
                    dout.write_bytes(b'\0\0\0\0\1\0\0\0')
                child.to_buffer(dout, fmt=fmt)
        else:
            raise TypeError

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str) -> 'DATItem':
        return cls.from_buffer(IBuffer.from_bytes(data), fmt=fmt)

    def to_bytes(self, fmt: str) -> bytes:
        dout = OBuffer()
        self.to_buffer(dout, fmt=fmt)
        data = dout.to_bytes()
        return data




