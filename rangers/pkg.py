"""!
@file
"""
from __future__ import annotations
from typing import Callable, TypeVar

import zlib
import os
import time

from .buffer import Buffer
from .common import check_dir

__all__ = [
    'PKG',
    'PKGItem',
    'MIN_SIZE_TO_COMPRESS',
    'COMPRESS_PNG',
    'COMPRESS_CHUNK_SIZE',
]

MIN_SIZE_TO_COMPRESS = 32
COMPRESS_PNG = False
COMPRESS_CHUNK_SIZE = 2 ** 16
COMPRESS_CHUNK_MAX_SIZE = 2 ** 16  # 64 KB
DEFAULT_COMPRESSION_LEVEL = 9

PKG_DATATYPE_RAW = 1
PKG_DATATYPE_ZLIB = 2
PKG_DATATYPE_DIR = 3

T = TypeVar('T')


class PKGItem:
    def __init__(self) -> None:
        self.data: bytes = b''
        self.name: str = ''
        self.type: int = -1
        self.childs: list[PKGItem] = []
        self.parent: PKGItem | None = None

    @classmethod
    def _compress(cls, data: bytes, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
        assert (
            0 < COMPRESS_CHUNK_SIZE <= COMPRESS_CHUNK_MAX_SIZE
        ), f'Invalid COMPRESS_CHUNK_SIZE: {COMPRESS_CHUNK_SIZE}. Should be in range from 1 to {COMPRESS_CHUNK_MAX_SIZE}'
        chunks = []
        din = Buffer(data)
        while din:
            buf = din.read(min(COMPRESS_CHUNK_SIZE, din.bytes_remains()))
            chunks.append(buf)
        dout = Buffer()
        for chunk in chunks:
            comp = zlib.compress(chunk, level=compression_level)
            dout.write_uint(len(comp) + 8)
            dout.write(b'ZL02')
            dout.write_uint(len(chunk))
            dout.write(comp)
        result = bytes(dout)
        return result

    @classmethod
    def _decompress(cls, data: bytes) -> bytes:
        din = Buffer(data)
        dout = Buffer()

        while din:
            bufsize = din.read_uint()
            buf = din.read(bufsize)

            bufin = Buffer(buf)

            zl02 = bufin.read(4)
            assert zl02 == b'ZL02', f'Invalid ZL signature: {zl02!r}'
            unpacked_size = bufin.read_uint()
            unpacked = zlib.decompress(bufin.read())
            assert len(unpacked) == unpacked_size
            dout.write(unpacked)

        result = bytes(dout)
        return result

    def decompressed_size(self) -> int:
        if self.type == PKG_DATATYPE_ZLIB:
            result = 158
            din = Buffer(self.data)
            while din:
                bufsize = din.read_uint()
                din.read(4)
                result += din.read_uint()
                din.pos += bufsize - 8
            return result

        if self.type == PKG_DATATYPE_RAW:
            return len(self.data) + 158

        if self.type == PKG_DATATYPE_DIR:
            return 158

        raise TypeError(f'Unknown item type: {self.type}')

    def compress(self, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> None:
        if self.type == PKG_DATATYPE_RAW:
            if not COMPRESS_PNG and self.name.endswith('.png'):
                return
            if len(self.data) < MIN_SIZE_TO_COMPRESS:
                return
            self.data = self._compress(self.data, compression_level=compression_level)
            self.type = PKG_DATATYPE_ZLIB

        elif self.type == PKG_DATATYPE_DIR:
            for child in self.childs:
                child.compress(compression_level=compression_level)

    def decompress(self) -> None:
        if self.type == PKG_DATATYPE_ZLIB:
            self.data = self._decompress(self.data)
            self.type = PKG_DATATYPE_RAW

        elif self.type == PKG_DATATYPE_DIR:
            for child in self.childs:
                child.decompress()

    def copy(self) -> PKGItem:
        new = PKGItem()
        new.data = self.data
        new.name = self.name
        new.type = self.type
        new.childs = [child.copy() for child in self.childs]
        new.parent = self.parent
        return new

    def size(self) -> int:
        if self.type == PKG_DATATYPE_DIR:
            return sum(child.size() for child in self.childs)
        return len(self.data)

    def count(self) -> int:
        if self.type == PKG_DATATYPE_DIR:
            return 1 + sum(child.count() for child in self.childs)
        return 1

    def __getitem__(self, key: str) -> PKGItem:
        assert self.type == PKG_DATATYPE_DIR, f'Cannot get item of non-dir item: {self}'
        if '/' in key:
            key, *child_key_ = key.split('/')
            child_key = '/'.join(child_key_)
        else:
            child_key = ''

        for child in self.childs:
            if child.name == key:
                if child_key:
                    return child[child_key]
                return child

        raise KeyError(f'Invalid key: {key}')

    def full_path(self) -> str:
        result = self.name
        if self.parent:
            result = self.parent.full_path() + result
        if self.type == PKG_DATATYPE_DIR:
            result += '/'
        return result

    def find_in_childs(self, name: str) -> int:
        for i, child in enumerate(self.childs):
            if child.name == name:
                return i
        return -1

    def header(self, offsets: dict[str, int]) -> bytes:
        if self.type == PKG_DATATYPE_DIR:
            size = 0
        else:
            size = len(self.data) + 4

        original_size = self.decompressed_size()

        full_path = self.full_path()
        assert full_path in offsets, f'Unknown error while calculating offsets: {offsets}'
        offset = offsets[full_path]

        result = Buffer()
        result.write_uint(size)
        result.write_uint(original_size)
        result.write_str(self.name.upper(), 63)
        result.write_str(self.name, 63)
        result.write_uint(self.type)
        result.write_uint(self.type)
        result.write(b'\0\0\0\0')
        result.write(b'\0\0\0\0')
        result.write_uint(offset)
        result.write(b'\0\0\0\0')

        return bytes(result)

    def to_bytes(self, offsets: dict[str, int]) -> bytes:
        buf = Buffer()
        self.to_buffer(buf, offsets)
        return bytes(buf)

    def check_offsets(self, offset: int, offsets: dict[str, int]) -> int:
        size = 0
        if self.type == PKG_DATATYPE_DIR:
            size += 12 + len(self.childs) * 158
            offsets[self.full_path()] = offset
            for child in self.childs:
                size += child.check_offsets(offset + size, offsets)
        else:
            offsets[self.full_path()] = offset + size
            size += 4 + len(self.data)
        return size

    def to_buffer(self, buf: Buffer, offsets: dict[str, int]) -> Buffer:
        if self.type == PKG_DATATYPE_DIR:
            buf.write(b'\xaa\0\0\0')  # zero1
            buf.write_uint(len(self.childs))
            buf.write(b'\x9e\0\0\0')  # zero2

            for child in self.childs:
                data = child.header(offsets)
                buf.write(data)

            for child in self.childs:
                child.to_buffer(buf, offsets)

        else:
            buf.write_uint(len(self.data))
            buf.write(self.data)
        return buf

    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> list[PKGItem]:
        result = []

        din = Buffer(data)
        din.pos = offset

        din.skip(4)
        items_count = din.read_uint()
        din.skip(4)

        for i in range(items_count):
            child = PKGItem()
            result.append(child)

            din.pos = offset + 12 + 158 * i

            din.skip(4)
            din.skip(4)
            din.skip(63)
            child.name = din.read_str(63).rstrip('\0')
            child.type = din.read_uint()
            assert child.type in {
                PKG_DATATYPE_DIR,
                PKG_DATATYPE_RAW,
                PKG_DATATYPE_ZLIB,
            }, f'Invalid item type: {child.type}. Should be in {(PKG_DATATYPE_DIR, PKG_DATATYPE_RAW, PKG_DATATYPE_ZLIB)}'
            din.skip(4)
            din.skip(4)
            din.skip(4)
            child_offset = din.read_uint()
            din.skip(4)

            if child.type == PKG_DATATYPE_DIR:
                child.childs = cls.from_bytes(data, child_offset)
                for child_child in child.childs:
                    child_child.parent = child

            else:
                din.pos = child_offset
                size = din.read_uint()
                child.data = din.read(size)

        return result

    def items_list(self) -> list[PKGItem]:
        result: list[PKGItem] = []
        for child in self.childs:
            if child.type == PKG_DATATYPE_DIR and child.childs:
                result += child.items_list()
            else:
                result += [child]
        return result


class PKG:
    def __init__(self, root: PKGItem, metadata: bytes = None) -> None:
        self.root = root
        if metadata is None:
            self.metadata = b'[timestamp: ' + str(int(time.time())).encode() + b']'
        else:
            self.metadata = bytes(metadata)

    @classmethod
    def from_pkg(cls, filename: str) -> PKG:
        with open(filename, 'rb') as fp:
            data = fp.read()
        din = Buffer(data)
        offset = din.read_uint()
        metadata = din.read(offset - 4)

        root = PKGItem()
        root.type = PKG_DATATYPE_DIR
        root.childs = PKGItem.from_bytes(data, offset)
        for child in root.childs:
            child.parent = root

        pkg = cls(root, metadata=metadata)
        return pkg

    def to_pkg(self, filename: str) -> None:
        root = self.root

        result = Buffer()
        result.write_uint(4 + len(self.metadata))
        result.write(self.metadata)

        offsets: dict[str, int] = {}
        root.check_offsets(4 + len(self.metadata), offsets)
        root.to_buffer(result, offsets)

        check_dir(filename)
        with open(filename, 'wb') as fp:
            fp.write(bytes(result))

    @classmethod
    def from_dir(cls, path: str, f: Callable[[str], bool] = lambda _: True) -> PKG:
        '''
        f - лямбда для исключения файлов из включения в пакет
            для каждого файла вызывается f(file) [file -  имя файла, без пути]
            если значение истинно, то файл включается в пакет, иначе - нет
        '''
        root = PKGItem()
        root.type = PKG_DATATYPE_DIR

        pkg = cls(root)

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        dirs = [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]

        for file in files:
            if not f(file):
                continue

            filename = os.path.join(path, file)
            with open(filename, 'rb') as fp:
                data = fp.read()

            item = PKGItem()
            item.data = data
            item.name = file
            item.type = PKG_DATATYPE_RAW
            item.childs = []
            item.parent = root
            root.childs.append(item)

        for directory in dirs:
            dirname = os.path.join(path, directory)

            sub_item = cls.from_dir(dirname, f).root

            item = PKGItem()
            item.data = b''
            item.name = directory
            item.type = PKG_DATATYPE_DIR
            item.childs = sub_item.childs
            for child in item.childs:
                child.parent = item

            item.parent = root
            root.childs.append(item)

        return pkg

    def to_dir(self, path: str) -> None:
        self.decompress()
        for item in self.items_list():
            filename = path + '/' + item.full_path()
            check_dir(filename)
            if item.type == PKG_DATATYPE_DIR:
                if not os.path.isdir(filename):
                    os.mkdir(filename)
            else:
                with open(filename, 'wb') as fp:
                    fp.write(item.data)

    def size(self) -> int:
        return self.root.size() + len(self.metadata)

    def decompressed_size(self) -> int:
        return sum(item.decompressed_size() for item in self.items_list())

    def count(self) -> int:
        return self.root.count()

    def compress(self, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> None:
        self.root.compress(compression_level=compression_level)

    def decompress(self) -> None:
        self.root.decompress()

    def copy(self) -> PKGItem:
        return self.root.copy()

    def items_list(self) -> list[PKGItem]:
        return self.root.items_list()
