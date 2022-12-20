from __future__ import annotations
from pathlib import Path
from typing import Any, Final, cast

import zlib
import os

from .std.buffer import Buffer, IBuffer, OBuffer
from .std.mixin import DataMixin

__all__ = ('PKG',)

MIN_SIZE_TO_COMPRESS: Final = 32
COMPRESS_PNG: Final = False
COMPRESS_CHUNK_SIZE: Final = 2**16
COMPRESS_CHUNK_MAX_SIZE: Final = 2**16  # 64 KB
DEFAULT_COMPRESSION_LEVEL: Final = 9

PKG_RAW: Final = 1
PKG_COMP: Final = 2
PKG_DIR: Final = 3


class PKG(DataMixin):
    name: str
    type: int
    data: bytes | list[PKG]
    metadata: bytes

    def __init__(
        self,
        name: str,
        type_: int,
        data: bytes | list[PKG],
        metadata: bytes = b'',
    ) -> None:
        self.name = name
        self.type = type_
        self.data = data
        self.metadata = metadata

    @staticmethod
    def _compress(data: bytes, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
        assert (
            0 < COMPRESS_CHUNK_SIZE <= COMPRESS_CHUNK_MAX_SIZE
        ), f'Invalid COMPRESS_CHUNK_SIZE: {COMPRESS_CHUNK_SIZE}. Should be in range from 1 to {COMPRESS_CHUNK_MAX_SIZE}'
        chunks = []
        din = Buffer(data)
        while din:
            buf = din.read(min(COMPRESS_CHUNK_SIZE, len(din) - din.pos))
            chunks.append(buf)
        dout = Buffer()
        for chunk in chunks:
            comp = zlib.compress(chunk, level=compression_level)
            dout.write_u32(len(comp) + 8)
            dout.write(b'ZL02')
            dout.write_u32(len(chunk))
            dout.write(comp)

        return bytes(dout)

    @staticmethod
    def _decompress(data: bytes) -> bytes:
        din = Buffer(data)
        dout = Buffer()

        while din:
            bufsize = din.read_u32()
            buf = din.read(bufsize)

            bufin = Buffer(buf)

            zl02 = bufin.read(4)
            assert zl02 == b'ZL02', f'Invalid ZL signature: {zl02!r}'
            unpacked_size = bufin.read_u32()
            unpacked = zlib.decompress(bufin.read())
            assert len(unpacked) == unpacked_size
            dout.write(unpacked)

        return bytes(dout)

    def compress(self, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> None:
        if self.type == PKG_RAW:
            if not COMPRESS_PNG and self.name.endswith('.png'):
                return
            if len(self.data) < MIN_SIZE_TO_COMPRESS:
                return
            assert isinstance(self.data, (bytes, bytearray))
            self.data = self._compress(self.data, compression_level=compression_level)
            self.type = PKG_COMP

        elif self.type == PKG_DIR:
            assert isinstance(self.data, list)
            for child in self.data:
                child.compress(compression_level=compression_level)

    def decompress(self) -> None:
        if self.type == PKG_DIR:
            assert isinstance(self.data, list)
            for item in self.data:
                item.decompress()

        elif self.type == PKG_COMP:
            assert isinstance(self.data, (bytes, bytearray))
            self.data = self._decompress(self.data)
            self.type = PKG_RAW

    def decompressed_size(self) -> int:
        assert self.type != PKG_DIR
        if self.type == PKG_RAW:
            return len(self.data)

        assert isinstance(self.data, (bytes, bytearray))
        result = 0
        buf = IBuffer(self.data)
        while buf:
            bufsize = buf.read_u32()
            buf.pos += 4
            result += buf.read_u32()
            buf.pos += bufsize - 8
        return result

    def calculate_offsets(self, offset: int, offsets: dict[int, int], sr1: bool = False) -> int:
        size = 0
        if self.type == PKG_DIR:
            assert isinstance(self.data, list)
            size += 12 + len(self.data) * (32 + (2 * len(self.name) + 2 if sr1 else 126))
            offsets[id(self)] = offset
            for child in self.data:
                size += child.calculate_offsets(offset + size, offsets, sr1=sr1)
        else:
            offsets[id(self)] = offset + size
            size += 4 + len(self.data)
        return size

    @classmethod
    def from_buffer(
        cls,
        buf: IBuffer,
        root: bool = False,
        sr1: bool = False,
        **kwargs: Any,
    ) -> PKG:
        if root:
            offset = buf.read_u32()
            assert offset >= 4
            metadata = buf.read(offset - 4)
            buf.pos = offset
            return cls(
                name='<root>',
                type_=PKG_DIR,
                data=cls.read_childs(buf, sr1=sr1),
                metadata=metadata,
            )

        size = buf.read_u32()
        _ = buf.read_u32()
        _ = buf.read_str(63).rstrip('\0')
        name = buf.read_str(63).rstrip('\0')
        assert name.upper() == _, (name, _)
        datatype = buf.read_u32()
        assert datatype in {PKG_DIR, PKG_COMP, PKG_RAW}
        _ = buf.read_u32()
        assert _ == datatype
        _ = buf.read_u32()
        assert _ == 0
        _ = buf.read_u32()
        assert _ == 0
        offset = buf.read_u32()
        _ = buf.read_u32()
        assert _ == 0

        self = cls(
            name=name,
            type_=datatype,
            data=[] if datatype == PKG_DIR else b'',
        )

        buf.push_pos(offset)
        if datatype == PKG_DIR:
            assert size == 0
            assert isinstance(self.data, list)
            self.data = cls.read_childs(buf, sr1=sr1)

        else:
            buf_size = buf.read_u32()
            assert buf_size == size - 4
            self.data = buf.read(buf_size)

        buf.pop_pos()
        return self

    @classmethod
    def read_childs(cls, buf: IBuffer, sr1: bool = False) -> list[PKG]:
        childs: list[PKG] = []
        _ = buf.read_u32()
        assert _ == 0xAA
        cnt = buf.read_u32()
        _ = buf.read_u32()
        assert _ == 0x9E
        for _ in range(cnt):
            childs.append(cls.from_buffer(buf, sr1=sr1))
        return childs

    def to_buffer(
        self,
        buf: OBuffer,
        root: bool = False,
        offsets: dict[int, int] | None = None,
        sr1: bool = False,
        **kwargs: Any,
    ) -> None:
        if root:
            assert offsets is None
            assert self.type == PKG_DIR
            data_start_pos = len(self.metadata) + 4
            offsets = {}
            self.calculate_offsets(
                data_start_pos,
                offsets,
                sr1=sr1,
            )
            buf.write_u32(data_start_pos)
            buf.write(self.metadata)
            self.write_childs(buf, offsets, sr1=sr1)
            return
        assert offsets is not None
        assert id(self) in offsets
        buf.write_u32(len(self.data) + 4 if self.type != PKG_DIR else 0)
        buf.write_u32(
            self.decompressed_size() if self.type != PKG_DIR else 0
        )  # FIXME decompressed size
        buf.write_str(self.name.upper(), 63)
        buf.write_str(self.name, 63)

        buf.write_u32(self.type)
        buf.write_u32(self.type)
        buf.write_u32(0)
        buf.write_u32(0)
        buf.write_u32(offsets[id(self)])
        buf.write_u32(0)

        buf.push_pos(offsets[id(self)], expand=True)
        if self.type == PKG_DIR:
            self.write_childs(buf, offsets=offsets, sr1=sr1)

        else:
            assert isinstance(self.data, (bytes, bytearray))
            buf.write_u32(len(self.data))
            buf.write(self.data)
        buf.pop_pos()

    def write_childs(self, buf: OBuffer, offsets: dict[int, int], sr1: bool = False) -> None:
        assert self.type == PKG_DIR
        assert isinstance(self.data, list)
        buf.write_u32(0xAA)
        buf.write_u32(len(self.data))
        buf.write_u32(0x9E)
        for child in self.data:
            child.to_buffer(buf, offsets=offsets, sr1=sr1)

    @classmethod
    def from_file(cls, path: Path, sr1: bool = False, **kwargs: Any) -> PKG:
        return super().from_file(path, root=True, sr1=sr1, **kwargs)

    def to_file(self, path: Path, sr1: bool = False, **kwargs: Any) -> None:
        super().to_file(path, root=True, sr1=sr1, **kwargs)

    @classmethod
    def from_folder(cls, path: Path) -> PKG:
        self = cls('<root>', PKG_DIR, [])
        assert isinstance(self.data, list)

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        dirs = [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]

        for file in files:
            filename = os.path.join(path, file)
            with open(filename, 'rb') as fp:
                data = fp.read()
            self.data.append(cls(file, PKG_RAW, data))

        for directory in dirs:
            dirname = os.path.join(path, directory)
            item = cls.from_folder(dirname)  # type: ignore[arg-type]
            item.name = directory
            self.data.append(item)

        return self

    def to_folder(self, path: Path) -> None:
        self.decompress()
        assert isinstance(self.data, list)
        for item in self.data:
            assert item.type != PKG_COMP

            if item.type == PKG_DIR:
                directory = os.path.join(path, item.name)
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                item.to_folder(directory)  # type: ignore[arg-type]

            else:
                filename = os.path.join(path, item.name)
                assert isinstance(item.data, (bytes, bytearray))
                with open(filename, 'wb') as fp:
                    fp.write(item.data)

    def __json__(self) -> dict[str, object]:
        return {
            'name': self.name,
            'type': self.type,
            'data': len(self.data)
            if self.type != PKG_DIR
            else [cast(PKG, i).__json__() for i in self.data],
        }

    def copy(self) -> PKG:
        if self.type == PKG_DIR:
            assert isinstance(self.data, list)
            return PKG(self.name, self.type, [child.copy() for child in self.data], self.metadata)
        else:
            return PKG(self.name, self.type, self.data, self.metadata)

    def __copy__(self) -> PKG:
        return PKG(self.name, self.type, self.data, self.metadata)

    def __deepcopy__(self, memo: object) -> PKG:
        return self.copy()
