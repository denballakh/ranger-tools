"""!
@file
@brief Реализует работу с игровыми датниками
"""

import zlib
import random

from .io import Buffer, AbstractIBuffer

try:
    from .dat_sign import get_sign, check_signed
    DAT_SIGN_AVAILABLE = True

except ImportError as e:
    def get_sign(_: bytes) -> bytes: return b''
    def check_signed(_: bytes) -> bool: return False
    DAT_SIGN_AVAILABLE = False


# __all__ = [
#     'DAT',
#     'DATItem',
# ]

ENCRYPTION_KEYS = {
    'SR1': 0,
    'ReloadMain': 1050086386,
    'ReloadCache': 1929242201,
    'HDMain': -1310144887,
    'HDCache': -359710921,
}

FORMAT_DEFAULT_SEEDS = {
    'SR1': 0,
    'ReloadMain': 955121797,
    'ReloadCache': 1954868526,
    'HDMain': -1215181314,
    'HDCache': -319409088,
}

# генератор псевдо-случайных чисел, использующийся для шифрования данных
def _rand31pm(seed: int) -> int:
    while True:
        hi, lo = divmod(seed, 0x1f31d)
        seed = lo * 0x41a7 - hi * 0xb14
        if seed < 1:
            seed += 0x7fffffff
        yield seed - 1

# расшифровывает данные и сверяет хеш расшифрованных данных
def decipher(data: bytes, key: int) -> bytes:
    din = Buffer(data)
    content_hash = din.read_uint()
    seed = din.read_int() ^ key
    rnd = _rand31pm(seed)
    dout = Buffer()
    while din:
        dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
    result = bytes(dout)
    assert zlib.crc32(result) == content_hash
    return result

# зашифровывывает данные, приписывает к ним хеш исходных данных и сид шифрования
# если параметр fmt есть в словаре FORMAT_DEFAULT_SEEDS, то ключ берется оттуда, иначе генерируется случайный
def cipher(data: bytes, fmt: str = None) -> bytes:
    seed = FORMAT_DEFAULT_SEEDS[fmt] if fmt in FORMAT_DEFAULT_SEEDS else random.randint(-2**31, 2**31-1)
    key = ENCRYPTION_KEYS[fmt]

    rnd = _rand31pm(seed)
    dout = Buffer()
    dout.write_uint(zlib.crc32(data))
    dout.write_int(seed ^ key)
    din = Buffer(data)
    while din:
        dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
    result = bytes(dout)
    return result

# приписывает к данным подпись, если данные не подписаны, иначе возвращает исходные данные
def sign(data: bytes):
    if not check_signed(data):
        return get_sign(data) + data
    return data


# удаляет подпись данных, если данные подписаны, иначе возвращает исходные данные
def unsign(data: bytes):
    if check_signed(data):
        return data[8:]
    return data

# распаковывает данные из формата ZL01
def decompress(data: bytes) -> bytes:
    din = Buffer(data)
    zl01 = din.read(4)
    size = din.read_uint()
    buf = din.read()
    assert zl01 == b'ZL01', f'Invalid ZL01 header: {zl01}'
    buf = zlib.decompress(buf)
    assert size == len(buf), f'Invalid decompressed size: {size} != {len(buf)}'
    return buf

# запаковывает данные в формат ZL01
def compress(data: bytes) -> bytes:
    size = len(data)
    data = zlib.compress(data, level=9)
    dout = Buffer()
    dout.write(b'ZL01')
    dout.write_uint(size)
    dout.write(data)
    return bytes(dout)

# пытается угадать формат датника, подбирая ключ шифрования
def guess_format(data: bytes, check_hash: bool = False) -> str:
    din = Buffer(data)
    if check_signed(data):
        din.skip(8)
    content_hash = din.read(4)
    seed_ciphered = din.read_int()
    zl01_ciphered = din.read(4)

    for keyname, key in ENCRYPTION_KEYS.items():
        din = Buffer(zl01_ciphered)
        rnd = _rand31pm(seed_ciphered ^ key)

        dout = Buffer()
        while not din.is_end():
            dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
        zl01 = bytes(dout)

        if zl01 != b'ZL01':
            print(zl01)
            continue
        if not check_hash:
            return keyname

        din = Buffer(data)
        _ = din.read_uint()
        _ = din.read_int()
        rnd = _rand31pm(seed_ciphered ^ key)

        dout = Buffer()
        while not din.end():
            dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
        result = bytes(dout)

        if zlib.crc32(result) == content_hash:
            return keyname

    return None

# вызывает guess_format для содержимого файла
def guess_file_format(filename: str) -> str:
    with open(filename, 'rb') as file:
        data = file.read()
    return guess_format(data)


class DAT:

    def __init__(self, root=None):
        self.root = root or DATItem()
        self.fmt = None

    def __repr__(self):
        return self.to_str()

    def copy(self):
        dat = self.__class__()
        dat.root = self.root.copy()
        dat.fmt = self.fmt
        return dat

    def merge(self, other: 'DAT'):
        self.root.merge(other.root)

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str = None) -> 'DAT':
        if check_signed(data):
            data = data[8:]

        if fmt not in ENCRYPTION_KEYS:
            fmt = guess_format(data)
        assert fmt in ENCRYPTION_KEYS, f'Invalid dat format: {fmt}'
        data_d = decompress(decipher(data, key=ENCRYPTION_KEYS[fmt]))
        # print(data_d)
        # b'\2\0\0' - метка блока (2) и название корня (пустая строка = 0 0)
        data_d = b'\2\0\0' + data_d
        root = DATItem.from_bytes(data_d, fmt=fmt)
        dat = cls(root)
        dat.fmt = fmt
        return dat

    def to_bytes(self, fmt: str, sign: bool = False) -> bytes:
        prefixlen = (len(self.root.name) + 1) * 2 + 1
        data = self.root.to_bytes(fmt=fmt)[prefixlen : ]
        # print(data)
        data = compress(data)
        if fmt is None:
            fmt = self.fmt
        assert fmt in ENCRYPTION_KEYS, f'Invalid dat format: {fmt}'
        data = cipher(data, fmt=fmt)

        if sign:
            data = get_sign(data) + data

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

    def to_dat(self, path: str, fmt: str, sign: bool = False):
        with open(path, 'wb') as file:
            file.write(self.to_bytes(fmt=fmt, sign=sign))

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
        self.type = DATItem.BLOCK
        self.name: str = ''
        self.value: str = ''
        self.childs: list[DATItem] = []
        self.sorted: int = True

    def __repr__(self) -> str:
        return self.to_str()

    def copy(self):
        item = self.__class__()
        item.type = self.type
        item.name = self.name
        item.value = self.value
        item.childs = [ch.copy() for ch in self.childs]
        item.sorted = self.sorted

    def merge(self, other: 'DATItem'):
        print(f'merging {self} with {other}')
        raise NotImplementedError

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
    def from_buffer(cls, din: Buffer, fmt: str) -> 'DATItem':
        item = cls()
        item.type = din.read_byte()


        # if item.type not in {cls.PAR, cls.BLOCK}:
        #     din.pos -= 1
        #     a = din.read_uint()
        #     # assert a == 0, f'[DATItem.from_buffer] Invalid "a" value: {a}'
        #     b = din.read_uint()
        #     # assert b == 1, f'[DATItem.from_buffer] Invalid "b" value: {b}'
        #     # if b != 1:
        #     #     print(din.pos, b)
        #     # item = cls.from_buffer(din, fmt=fmt)

        #     item.type = din.read_byte()
        if type == 0:
            din.skip(7)
            return DATItem.from_buffer(din, fmt=fmt)

        if item.type == cls.PAR:
            item.name = din.read_wstr()
            item.value = din.read_wstr()

        elif item.type == cls.BLOCK:
            item.name = din.read_wstr()
            if fmt in {'HDMain', 'ReloadMain'}:
                item.sorted = din.read_byte()
            else:
                item.sorted = 0
            childs_cnt = din.read_uint()
            print(f'childs:{childs_cnt} pos:{hex(din.pos)}')

            for _ in range(childs_cnt):
                print(f'reading child at pos {hex(din.pos)}')
                child = cls.from_buffer(din, fmt=fmt)
                item.childs.append(child)
        else:
            raise Exception(f'Wrong item type: {item.type} [{din.pos}]')

        return item

    def to_buffer(self, dout: Buffer, fmt: str):
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
                    dout.write(b'\0\0\0\0\1\0\0\0')
                child.to_buffer(dout, fmt=fmt)
        else:
            raise TypeError

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str) -> 'DATItem':
        return cls.from_buffer(Buffer(data), fmt=fmt)

    def to_bytes(self, fmt: str) -> bytes:
        dout = Buffer()
        self.to_buffer(dout, fmt=fmt)
        data = bytes(dout)
        return data
