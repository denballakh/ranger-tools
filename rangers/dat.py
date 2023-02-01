# TODO: переписать все
# TODO: change str to Path

from __future__ import annotations
from typing import Any, Final, ClassVar, Generic, Literal, TypeVar

import zlib
import json
from pathlib import Path

from .std.buffer import Buffer
from .common import rand31pm
from .std.dataclass import CryptedRand31pm, ZL, Nested

T = TypeVar('T')

SIGN_KEY_1 = 0xC83FCBF3
SIGN_KEY_2 = 0x7DB6C99D


def get_sign(data: bytes, /) -> bytes:
    d0_3 = len(data) ^ SIGN_KEY_1 ^ SIGN_KEY_2
    d4_7 = zlib.crc32((zlib.crc32(data) ^ SIGN_KEY_2).to_bytes(4, 'little') + data) ^ SIGN_KEY_1
    return d0_3.to_bytes(4, 'little') + d4_7.to_bytes(4, 'little')


def check_signed(data: bytes, /) -> bool:
    return data[:8] == get_sign(data[8:])


__all__ = [
    'DAT',
    'DATItem',
    'ENCRYPTION_KEYS',
    'FORMAT_DEFAULT_SEEDS',
    # 'DatFormat',
    'get_sign',
    'check_signed',
]

# DatDictVal = Union[str, list['DatDictVal'], 'DatDict']  # type: ignore[misc]
# DatDict = dict[str, DatDictVal]  # type: ignore[misc]

DatDict = Any
DatDictVal = Any
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
def guess_format(
    data: bytes, check_hash: bool = True, *, _sign_removed: bool = False
) -> str | None:
    buf = Buffer(data)
    if check_signed(data):
        buf.pos += 8
    content_hash = buf.read_u32()
    seed_ciphered = buf.read_i32()
    zl01_ciphered = buf.read(4)

    buf = Buffer(zl01_ciphered)
    dout = Buffer()

    for keyname, key in ENCRYPTION_KEYS.items():
        buf.pos = 0
        dout.pos = 0

        rnd = rand31pm(seed_ciphered ^ key)

        while buf:
            dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))

        if bytes(dout) != b'ZL01':
            continue

        if not check_hash:
            return keyname

        fbuf = Buffer(data)
        if check_signed(data):
            fbuf.pos += 8
        _ = fbuf.read_u32()
        _ = fbuf.read_i32()
        rnd = rand31pm(seed_ciphered ^ key)

        dout = Buffer()
        while fbuf:
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


class AbstractIBuffer(Generic[T]):
    data: list[T]
    pos: int

    def __init__(self, data: list[T]) -> None:
        self.data = data
        self.pos = 0

    def get(self) -> T:
        assert 0 <= self.pos < len(self.data)
        result = self.data[self.pos]
        self.pos += 1
        return result

    def end(self) -> bool:
        return 0 <= self.pos < len(self.data)


class DAT:
    root: DATItem
    fmt: str | None

    def __init__(self, root: DATItem | None = None) -> None:
        self.root = DATItem() if root is None else root
        self.fmt: str | None = None

    def __repr__(self) -> str:
        return self.to_str()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DAT):
            return self.root == other.root
        return NotImplemented

    def copy(self) -> DAT:
        dat = self.__class__()
        dat.root = self.root.copy()
        dat.fmt = self.fmt
        return dat

    def merge(self, other: DAT) -> None:
        self.root.merge(other.root)

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str | None = None) -> DAT:
        data = unsign_data(data)

        if fmt not in ENCRYPTION_KEYS:
            fmt = guess_format(data)
        assert fmt is not None
        assert fmt in ENCRYPTION_KEYS, f'Invalid dat format: {fmt}'
        data_d = Nested(
            CryptedRand31pm(key=ENCRYPTION_KEYS[fmt]),
            ZL(mode=1, length=-1),
        ).read_bytes(data)

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

        data = Nested(
            CryptedRand31pm(key=ENCRYPTION_KEYS[fmt], seed=FORMAT_DEFAULT_SEEDS[fmt]),
            ZL(mode=1, length=-1),
        ).write_bytes(data)

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
    def from_dat(cls, path: Path, fmt: str | None = None) -> DAT:
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data, fmt=fmt)

    def to_dat(self, path: Path, fmt: str, sign: bool = False) -> None:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        with open(path, 'wb') as file:
            file.write(self.to_bytes(fmt=fmt, sign=sign))

    @classmethod
    def from_txt(cls, path: Path) -> DAT:
        for encoding in ['utf8', 'utf16']:
            try:
                with open(path, 'rt', encoding=encoding) as file:
                    s = file.read()
                return cls.from_str(s)
            except UnicodeDecodeError:
                pass
        raise NotImplementedError

    def to_txt(self, path: Path) -> None:
        with open(path, 'wt', encoding='utf-8') as file:
            file.write(self.to_str())

    @classmethod
    def from_dict(cls, data: DatDict) -> DAT:
        return cls(DATItem.from_dict(data))

    def to_dict(self) -> DatDict:
        return self.root.to_dict()

    @classmethod
    def from_json(cls, path: Path) -> DAT:
        raise NotImplementedError

    def to_json(self, path: Path, indent: int = 4) -> None:
        with open(path, 'wt', encoding='utf-8') as file:
            json.dump(self.root.to_dict(), file, indent=indent)

    @classmethod
    def from_file(cls, path: Path) -> DAT:
        if path.suffix == '.txt':
            return cls.from_txt(path)

        if path.suffix == '.json':
            return cls.from_json(path)

        if path.suffix == '.dat':
            return cls.from_dat(path)

        try:
            return cls.from_txt(path)
        except Exception:
            pass

        try:
            return cls.from_json(path)
        except Exception:
            pass

        try:
            return cls.from_dat(path)
        except Exception:
            pass

        raise NotImplementedError(path)

    def to_file(self, path: Path, fmt: str = 'HDMain', sign: bool = False) -> None:
        if path.suffix == '.txt':
            return self.to_txt(path)

        if path.suffix == '.json':
            return self.to_json(path)

        if path.suffix == '.dat':
            return self.to_dat(path, fmt=fmt, sign=sign)

        raise NotImplementedError(path)


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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DATItem):
            return (
                self.type == other.type
                and self.name == other.name
                and self.value == other.value
                and self.childs == other.childs
            )
        return NotImplemented

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
            # assert ' ' not in name
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
                item.sorted = True  # default
                # raise ValueError

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

            childs_cnt = buf.read_u32()

            for _ in range(childs_cnt):
                if item.sorted:
                    _ = buf.read_u32()
                    _ = buf.read_u32()

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

            buf.write_u32(len(self.childs))

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

                    buf.write_u32(loc_index)
                    buf.write_u32(glo_index)
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
                result[child.name].append(child.to_dict())

        return result

    @classmethod
    def from_dict(cls, data: DatDict) -> DATItem:
        self = cls()
        assert isinstance(data, dict)
        for key, value_ in data.items():
            for value in (value_,) if not isinstance(value_, list) else value_:
                if isinstance(value, dict):
                    child = cls.from_dict(value)
                    child.name = key
                    child.type = cls.BLOCK
                    self.childs.append(child)

                elif isinstance(value, str):
                    child = cls()
                    child.name = key
                    child.type = cls.PAR
                    child.value = value
                    self.childs.append(child)

                else:
                    raise TypeError(value)

        return self
