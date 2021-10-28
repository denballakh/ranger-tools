from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Type,
    Generic,
    Callable,
    Generator,
    final,
)

import zlib
import random

from ..buffer import Buffer, IBuffer, OBuffer

T = TypeVar('T')
G = TypeVar('G')


# class DataFrame:
#     pass


class DataClass(Generic[T]):
    def before(self, buf: Buffer) -> None:
        pass

    def after(self, buf: Buffer) -> None:
        pass

    def read(self, buf: IBuffer) -> T:
        raise NotImplementedError(f'Class {type(self).__name__} cannot read data.')

    def write(self, buf: OBuffer, obj: T) -> None:
        raise NotImplementedError(f'Class {type(self).__name__} cannot write data.')

    @final
    def read_bytes(self, data: bytes | bytearray) -> T:
        return self.read(IBuffer(data))

    @final
    def write_bytes(self, obj: T) -> bytes:
        buf = OBuffer()
        self.write(buf, obj)
        return bytes(buf)


# @final
class Bool(DataClass[bool]):
    @staticmethod
    def read(buf: IBuffer) -> bool:
        return buf.read_bool()

    @staticmethod
    def write(buf: OBuffer, obj: bool) -> None:
        buf.write_bool(obj)


# @final
class Byte(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_byte()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_byte(obj)


# @final
class Int8(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_char()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_char(obj)


# @final
class UInt8(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_uchar()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_uchar(obj)


# @final
class Int16(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_short()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_short(obj)


# @final
class UInt16(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_short()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_short(obj)


# @final
class Int32(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_int()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_int(obj)


# @final
class UInt32(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_uint()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_uint(obj)


# @final
class Int64(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_long()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_long(obj)


# @final
class UInt64(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer) -> int:
        return buf.read_ulong()

    @staticmethod
    def write(buf: OBuffer, obj: int) -> None:
        buf.write_ulong(obj)


# @final
class Float(DataClass[float]):
    @staticmethod
    def read(buf: IBuffer) -> float:
        return buf.read_float()

    @staticmethod
    def write(buf: OBuffer, obj: float) -> None:
        buf.write_float(obj)


# @final
class Double(DataClass[float]):
    @staticmethod
    def read(buf: IBuffer) -> float:
        return buf.read_double()

    @staticmethod
    def write(buf: OBuffer, obj: float) -> None:
        buf.write_double(obj)


# @final
class Str(DataClass[str]):
    def __init__(self, length: int = -1) -> None:
        self.length = length

    def read(self, buf: IBuffer) -> str:
        return buf.read_str(self.length)

    def write(self, buf: OBuffer, obj: str) -> None:
        buf.write_str(obj, self.length)


# @final
class WStr(DataClass[str]):
    def __init__(self, length: int = -1) -> None:
        self.length = length

    def read(self, buf: IBuffer) -> str:
        return buf.read_wstr(self.length)

    def write(self, buf: OBuffer, obj: str) -> None:
        buf.write_wstr(obj, self.length)


class Bytes(DataClass[bytes]):
    def __init__(self, size: int = None) -> None:
        self.size = size

    def read(self, buf: IBuffer) -> bytes:
        assert self.size is not None
        return buf.read(self.size)

    def write(self, buf: OBuffer, obj: bytes) -> None:
        if self.size is not None:
            assert len(obj) == self.size
        buf.write(obj)


class List(DataClass[list[T]]):
    def __init__(self, dcls: DataClass[T], lensize: int = 4, byteorder: str = 'little') -> None:
        self.dcls = dcls
        self.lensize = lensize
        self.byteorder = byteorder

    def read(self, buf: IBuffer) -> list[T]:
        length = int.from_bytes(buf.read(self.lensize), self.byteorder)
        result: list[T] = []
        for _ in range(length):
            obj = self.dcls.read(buf)
            result.append(obj)
        return result

    def write(self, buf: OBuffer, obj: list[T]) -> None:
        buf.write(len(obj).to_bytes(self.lensize, self.byteorder))
        for item in obj:
            self.dcls.write(buf, item)


class Sequence(DataClass[tuple[Any, ...]]):  # type: ignore[misc]
    def __init__(self, *dclss: DataClass[Any]) -> None:
        self.dclss = dclss

    def read(self, buf: IBuffer) -> tuple[Any, ...]:
        result = []
        for dcls in self.dclss:
            item = dcls.read(buf)
            result.append(item)
        return tuple(result)

    def write(self, buf: OBuffer, obj: tuple[Any, ...]) -> None:
        assert len(self.dclss) == len(obj)
        for item, writer in zip(obj, self.dclss):
            writer.write(buf, item)


class Pair(DataClass[tuple[T, T]]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer) -> tuple[T, T]:
        return self.dcls.read(buf), self.dcls.read(buf)

    def write(self, buf: OBuffer, obj: tuple[T, T]) -> None:
        self.dcls.write(buf, obj[0])
        self.dcls.write(buf, obj[1])


class Converted(DataClass[G], Generic[T, G]):
    def __init__(
        self,
        dcls: DataClass[T],
        *,
        decode: Callable[[T], G] = None,
        encode: Callable[[G], T] = None,
    ) -> None:
        self.decode = decode
        self.encode = encode
        self.dcls = dcls

    def read(self, buf: IBuffer) -> G:
        assert self.decode is not None
        return self.decode(self.dcls.read(buf))

    def write(self, buf: OBuffer, obj: G) -> None:
        assert self.encode is not None
        self.dcls.write(buf, self.encode(obj))


class NamedSequence(DataClass[dict[str, Any]]):
    def __init__(self, **kwargs: DataClass[Any]) -> None:
        self.dclss = kwargs

    def read(self, buf: IBuffer) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name, dcls in self.dclss.items():
            result[name] = dcls.read(buf)
        return result

    def write(self, buf: OBuffer, obj: dict[str, Any]) -> None:
        for name, dcls in self.dclss.items():
            dcls.write(buf, obj[name])


class Const(DataClass[T]):
    def __init__(self, dcls: DataClass[T], value: T) -> None:
        self.dcls = dcls
        self.value = value

    def read(self, buf: IBuffer) -> T:
        obj = self.dcls.read(buf)
        if obj != self.value:
            raise ValueError(f'Object {obj!r} should be equal to const {self.value!r}')
        return obj

    def write(self, buf: OBuffer, obj: T):
        if obj != self.value:
            raise ValueError(f'Object {obj!r} should be equal to const {self.value!r}')
        self.dcls.write(buf, obj)


# @final
class NONE(DataClass[None]):
    def read(self, buf: IBuffer) -> None:
        return None

    def write(self, buf: OBuffer, obj: Any) -> None:
        assert obj is None


class Skip(DataClass[None]):
    def __init__(self, n: int) -> None:
        self.n = n

    def read(self, buf: IBuffer) -> None:
        buf.read(self.n)

    def write(self, buf: OBuffer, obj: Any) -> None:
        assert obj is None
        buf.write(bytes(self.n))


class Nested(DataClass[T]):
    def __init__(self, dcls1: DataClass[bytes], dcls2: DataClass[T]) -> None:
        self.dcls1 = dcls1
        self.dcls2 = dcls2

    def read(self, buf: IBuffer) -> T:
        data = self.dcls1.read(buf)
        obj = self.dcls2.read(Buffer(data))
        return obj

    def write(self, buf: OBuffer, obj: T) -> None:
        buf2 = Buffer()
        self.dcls2.write(buf2, obj)
        data = bytes(buf2)
        self.dcls1.write(buf, data)


class BufEC(DataClass[bytes]):
    def read(self, buf: IBuffer) -> bytes:
        size = buf.read_uint()
        data = buf.read(size)
        return data

    def write(self, buf: OBuffer, obj: bytes) -> None:
        buf.write_uint(len(obj))
        buf.write(obj)


class CryptedRand31pm(DataClass[bytes]):
    def __init__(self, key: int, seed: int = None, length: int = None) -> None:
        self.key = key
        self.seed = random.randint(-(2 ** 31), 2 ** 31 - 1) if seed is None else seed
        self.length = length

    @staticmethod
    def _rand31pm(seed: int) -> Generator[int, None, None]:
        while True:
            hi, lo = divmod(seed, 0x1F31D)
            seed = lo * 0x41A7 - hi * 0xB14
            if seed < 1:
                seed += 0x7FFFFFFF
            yield seed - 1

    def read(self, buf: IBuffer) -> bytes:
        content_hash = buf.read_uint()
        rnd = self._rand31pm(buf.read_int() ^ self.key)
        dout = Buffer()
        while buf:
            dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))
        result = bytes(dout)
        assert zlib.crc32(result) == content_hash
        return result

    def write(self, buf: OBuffer, obj: bytes) -> None:
        rnd = self._rand31pm(self.seed)
        buf.write_uint(zlib.crc32(obj))
        buf.write_int(self.seed ^ self.key)
        din = Buffer(obj)
        while din:
            buf.write_byte(din.read_byte() ^ (next(rnd) & 0xFF))

class ZL(DataClass[bytes]):
    def __init__(self, mode, **kwargs) -> None:
        assert mode in {1, 2, 3}
        self.mode = mode
        self.kwargs = kwargs

    def read(self, buf: IBuffer) -> bytes:
        if self.mode == 1:
            if 'length' in self.kwargs:
                size = self.kwargs['length']
            else:
                size = buf.read_uint()

            magic = buf.read(4)
            assert magic == b'ZL01'
            decompressed_size = buf.read_uint()
            compressed_data = buf.read(size - 8)
            data = zlib.decompress(compressed_data)
            assert len(data) == decompressed_size
            return data


        if self.mode == 2:
            pass

        if self.mode == 3:
            pass

        raise ValueError(self.mode)

    def write(self, buf: OBuffer, obj: bytes) -> None:
        if self.mode == 1:
            return

        if self.mode == 2:
            return

        if self.mode == 3:
            return

        raise ValueError(f'Unknown ZL mode: {self.mode}')




# class BinaryObject(Generic[T]):
#     __dcls__: DataClass[T]

#     def read(self, obj: T) -> None:
#         pass

#     def write(self) -> T:
#         pass

