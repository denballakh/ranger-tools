"""!
@file
@brief Реализует работу с игровыми датниками
"""
from __future__ import annotations
from typing import Final, ClassVar, Literal, TypeVar, Union

import zlib
import json

# import random
# import enum

from .buffer import Buffer
from .io import AbstractIBuffer
from .common import rand31pm
from .std.dataclass import CryptedRand31pm, ZL, Nested

T = TypeVar('T')

DAT_SIGN_AVAILABLE: bool
try:
    from .dat_sign import get_sign, check_signed

    DAT_SIGN_AVAILABLE = True

except ImportError:

    def get_sign(data: bytes, /) -> bytes:
        return b''

    def check_signed(data: bytes, /) -> bool:
        return False

    DAT_SIGN_AVAILABLE = False


__all__ = [
    'DAT',
    'DATItem',
    'ENCRYPTION_KEYS',
    'FORMAT_DEFAULT_SEEDS',
    'DAT_SIGN_AVAILABLE',
    # 'DatFormat',
    'get_sign',
    'check_signed',
]

DatDictVal = Union[str, list['DatDictVal'], dict[str, 'DatDictVal']]  # type: ignore[misc]
DatDict = dict[str, DatDictVal]  # type: ignore[misc]

# class DatFormat(enum.Flag):
#     SR1 = 0
#     HDMain = 1
#     ReloadMain = 2
#     HDCache = 3
#     ReloadCache = 4

#     @property
#     def main(self):
#         return self in (DatFormat.HDMain, DatFormat.ReloadMain)

#     @property
#     def cache(self):
#         return self in (DatFormat.HDCache, DatFormat.ReloadCache)

#     @property
#     def reload(self):
#         return self in (DatFormat.ReloadMain, DatFormat.ReloadCache)

#     @property
#     def hd(self):
#         return self in (DatFormat.HDMain, DatFormat.HDCache)

#     @property
#     def sr1(self):
#         return self == DatFormat.SR1


ENCRYPTION_KEYS: Final = {
    'SR1': 0,
    'ReloadMain': 1050086386,
    'ReloadCache': 1929242201,
    'HDMain': -1310144887,
    'HDCache': -359710921,
}

FORMAT_DEFAULT_SEEDS: Final = {
    'SR1': 0,
    'ReloadMain': 955121797,
    'ReloadCache': 1954868526,
    'HDMain': -1215181314,
    'HDCache': -319409088,
}

# приписывает к данным подпись, если данные не подписаны, иначе возвращает исходные данные
def sign_data(data: bytes) -> bytes:
    if not check_signed(data):
        return get_sign(data) + data
    return data


# удаляет подпись данных, если данные подписаны, иначе возвращает исходные данные
def unsign_data(data: bytes) -> bytes:
    if check_signed(data):
        return data[8:]
    return data


# пытается угадать формат датника, подбирая ключ шифрования
def guess_format(data: bytes, check_hash: bool = True) -> str | None:
    buf = Buffer(data)
    if check_signed(data):
        buf.skip(8)
    content_hash = buf.read_uint()
    seed_ciphered = buf.read_int()
    zl01_ciphered = buf.read(4)

    buf = Buffer(zl01_ciphered)
    dout = Buffer()

    for keyname, key in ENCRYPTION_KEYS.items():
        buf.pos = 0
        dout.pos = 0

        rnd = rand31pm(seed_ciphered ^ key)

        while not buf.is_end():
            dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))

        if bytes(dout) != b'ZL01':
            continue

        if not check_hash:
            return keyname

        fbuf = Buffer(data)
        if check_signed(data):
            fbuf.skip(8)
        _ = fbuf.read_uint()
        _ = fbuf.read_int()
        rnd = rand31pm(seed_ciphered ^ key)

        dout = Buffer()
        while not fbuf.is_end():
            dout.write_byte(fbuf.read_byte() ^ (next(rnd) & 0xFF))
        result = bytes(dout)

        if zlib.crc32(result) == content_hash:
            return keyname

    return None


# вызывает guess_format для содержимого файла
def guess_file_format(filename: str) -> str | None:
    with open(filename, 'rb') as file:
        data = file.read()
    return guess_format(data)


class DAT:
    root: DATItem
    fmt: str | None

    def __init__(self, root: DATItem = None) -> None:
        self.root = DATItem() if root is None else root
        self.fmt: str | None = None

    def __repr__(self) -> str:
        return self.to_str()

    def copy(self) -> DAT:
        dat = self.__class__()
        dat.root = self.root.copy()
        dat.fmt = self.fmt
        return dat

    def merge(self, other: DAT) -> None:
        self.root.merge(other.root)

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str = None) -> DAT:
        data = unsign_data(data)

        if fmt not in ENCRYPTION_KEYS:
            fmt = guess_format(data)
        assert fmt is not None
        assert fmt in ENCRYPTION_KEYS, f'Invalid dat format: {fmt}'
        data_d = Buffer(data).read_dcls(
            Nested(
                CryptedRand31pm(key=ENCRYPTION_KEYS[fmt]),
                ZL(mode=1, length=-1),
            )
        )
        # b'\2\0\0' - тип элемента (блок == \2) и название корня (пустая строка == \0\0)
        data_d = b'\2\0\0' + data_d
        root = DATItem.from_bytes(data_d, fmt=fmt)
        dat = cls(root)
        dat.fmt = fmt
        return dat

    def to_bytes(self, fmt: str, sign: bool = False) -> bytes:
        prefixlen = (len(self.root.name) + 1) * 2 + 1
        data = self.root.to_bytes(fmt=fmt)[prefixlen:]
        # if fmt is None:
        #     fmt = self.fmt

        assert fmt is not None
        assert fmt in ENCRYPTION_KEYS, f'Invalid dat format: {fmt}'

        buf = Buffer()
        buf.write_dcls(
            Nested(
                CryptedRand31pm(key=ENCRYPTION_KEYS[fmt]),
                ZL(mode=1, length=-1),
            ),
            data,
        )
        data = bytes(buf)

        if sign:
            data = sign_data(data)

        return data

    @classmethod
    def from_str(cls, s: str) -> DAT:
        wrapped = ' ^{\n' + s + '\n}\n'
        root = DATItem.from_str(wrapped)
        return cls(root)

    def to_str(self) -> str:
        return self.root.to_str(isroot=True)

    @classmethod
    def from_dat(cls, path: str, fmt: str = None) -> DAT:
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data, fmt=fmt)

    def to_dat(self, path: str, fmt: str, sign: bool = False) -> None:
        with open(path, 'wb') as file:
            file.write(self.to_bytes(fmt=fmt, sign=sign))

    @classmethod
    def from_txt(cls, path: str) -> DAT:
        with open(path, 'rt', encoding='utf-8') as file:
            s = file.read()
        return cls.from_str(s)

    def to_txt(self, path: str) -> None:
        with open(path, 'wt', encoding='utf-8') as file:
            file.write(self.to_str())

    def to_dict(self) -> DatDict:
        return self.root.to_dict()  # type: ignore[return-value]

    def to_json(self, path: str, indent: int = 4) -> None:
        with open(path, 'wt', encoding='utf-8') as file:
            json.dump(self.root.to_dict(), file, indent=indent)


class DATItem:
    PAR: ClassVar[Literal[1]] = 1
    BLOCK: ClassVar[Literal[2]] = 2

    type: int
    name: str
    value: str
    childs: list[DATItem]
    sorted: bool

    def __init__(self) -> None:
        self.type = DATItem.BLOCK
        self.name = ''
        self.value = ''
        self.childs = []
        self.sorted = True

    def __repr__(self) -> str:
        return self.to_str()

    def copy(self) -> DATItem:
        item = self.__class__()
        item.type = self.type
        item.name = self.name
        item.value = self.value
        item.childs = [ch.copy() for ch in self.childs]
        item.sorted = self.sorted
        return item

    def merge(self, other: DATItem) -> None:
        # print(f'merging {self} with {other}')
        raise NotImplementedError

    @classmethod
    def from_str_buffer(cls, buf: AbstractIBuffer[str]) -> DATItem | None:
        s = buf.get()
        assert '\n' not in s
        s, _, _ = s.partition('//')
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
                item.sorted = False
            elif '^' in s:
                item.sorted = True
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
    def from_str(cls, s: str) -> DATItem | None:
        buf = AbstractIBuffer(s.split('\n'))
        return cls.from_str_buffer(buf)

    def to_str(self, isroot: bool = False) -> str:
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
                chs = child.to_str()
                for s in chs.split('\n'):
                    result += tab + s + '\n'

            if not isroot:
                result += '}'

            return result

        raise TypeError

    @classmethod
    def from_buffer(cls, buf: Buffer, fmt: str) -> DATItem:
        item: DATItem = cls()
        item.type = buf.read_byte()
        item.name = buf.read_wstr()

        if item.type == cls.PAR:
            item.value = buf.read_wstr()

        elif item.type == cls.BLOCK:
            if fmt in {'HDMain', 'ReloadMain', 'SR1'}:
                item.sorted = buf.read_bool()
            else:
                item.sorted = False

            childs_cnt = buf.read_uint()

            for _ in range(childs_cnt):
                if item.sorted:
                    _ = buf.read_uint()
                    _ = buf.read_uint()

                child = cls.from_buffer(buf, fmt=fmt)
                item.childs.append(child)

        else:
            raise ValueError(f'Wrong item type: {item.type} (pos={buf.pos})')

        return item

    def to_buffer(self, buf: Buffer, fmt: str) -> None:
        buf.write_byte(self.type)
        buf.write_wstr(self.name)

        assert self.type in (self.PAR, self.BLOCK), self.type

        if self.type == self.PAR:
            buf.write_wstr(self.value)

        elif self.type == self.BLOCK:
            if fmt in {'HDMain', 'ReloadMain', 'SR1'}:
                buf.write_byte(self.sorted)

            buf.write_uint(len(self.childs))

            if fmt in {'HDMain', 'ReloadMain', 'SR1'} and self.sorted:
                glo_index: int = 0
                loc_index: int = 1
                name = '\0'  # unused name
                for child in self.childs:
                    if child.name == name:
                        loc_index += 1
                        glo_index = 0
                    else:
                        loc_index = 0
                        glo_index = [c.name for c in self.childs].count(child.name)
                    name = child.name

                    buf.write_uint(loc_index)
                    buf.write_uint(glo_index)
                    child.to_buffer(buf, fmt=fmt)

            else:
                for child in self.childs:
                    child.to_buffer(buf, fmt=fmt)

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str) -> DATItem:
        return cls.from_buffer(Buffer(data), fmt=fmt)

    def to_bytes(self, fmt: str) -> bytes:
        buf = Buffer()
        self.to_buffer(buf, fmt=fmt)
        data = bytes(buf)
        return data

    def to_dict(self) -> DatDictVal:
        if self.type == self.PAR:
            return self.value

        result: DatDict = {}
        for child in self.childs:
            if child.name not in result:
                result[child.name] = child.to_dict()
            else:
                if not isinstance(result[child.name], list):
                    result[child.name] = [result[child.name]]

                assert isinstance(result[child.name], list)
                result[child.name].append(child.to_dict())  # type: ignore[union-attr]

        return result
