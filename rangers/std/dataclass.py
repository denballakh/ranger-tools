from __future__ import annotations

from typing import (
    # TYPE_CHECKING,
    Any,
    TypeVar,
    Literal,
    Generic,
    Callable,
    Iterator,
    final,
    NoReturn,
    # Protocol,
    Hashable,
)
from types import EllipsisType

import zlib
import random
from pprint import pprint

from mypy_extensions import trait

from ..buffer import IBuffer, OBuffer
from ..common import rand31pm

T = TypeVar('T')
G = TypeVar('G')


class DataClassError(Exception):
    pass


class Memo(dict):
    pass


# protocols:
class DataClass(Generic[T]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        raise NotImplementedError(f'Class {type(self).__name__} cannot read data.')

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        raise NotImplementedError(f'Class {type(self).__name__} cannot write data.')

    @final
    def read_bytes(self, data: bytes | bytearray) -> T:
        return self.read(IBuffer(data), memo=Memo())

    @final
    def write_bytes(self, obj: T) -> bytes:
        buf = OBuffer()
        self.write(buf, obj, memo=Memo())
        return bytes(buf)


@trait
class ReadOnlyDataClass(Generic[T]):
    @final
    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> NoReturn:
        raise DataClassError(f'Cannot write read-only {self.__class__.__name__} object')


@trait
class WriteOnlyDataClass(Generic[T]):
    @final
    def read(self, buf: IBuffer, *, memo: Memo) -> NoReturn:
        raise DataClassError(f'Cannot read write-only {self.__class__.__name__} object')


# @trait
class NullDataClass(DataClass[None]):
    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        return None

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None


# atomic dataclasses:
class Bool(DataClass[bool]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> bool:
        return buf.read_bool()

    @staticmethod
    def write(buf: OBuffer, obj: bool, *, memo: Memo) -> None:
        buf.write_bool(obj)


# @final
class Byte(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_byte()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_byte(obj)


class Int8(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_char()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_char(obj)


class UInt8(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_uchar()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_uchar(obj)


class Int16(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_short()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_short(obj)


class UInt16(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_ushort()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_ushort(obj)


class Int32(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_int()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_int(obj)


class UInt32(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_uint()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_uint(obj)


class Int64(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_long()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_long(obj)


class UInt64(DataClass[int]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_ulong()

    @staticmethod
    def write(buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_ulong(obj)


class Float(DataClass[float]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> float:
        return buf.read_float()

    @staticmethod
    def write(buf: OBuffer, obj: float, *, memo: Memo) -> None:
        buf.write_float(obj)


class Double(DataClass[float]):
    @staticmethod
    def read(buf: IBuffer, *, memo: Memo) -> float:
        return buf.read_double()

    @staticmethod
    def write(buf: OBuffer, obj: float, *, memo: Memo) -> None:
        buf.write_double(obj)


class Str(DataClass[str]):
    def __init__(self, length: int = -1) -> None:
        self.length = length

    def read(self, buf: IBuffer, *, memo: Memo) -> str:
        return buf.read_str(self.length)

    def write(self, buf: OBuffer, obj: str, *, memo: Memo) -> None:
        buf.write_str(obj, self.length)


class WStr(DataClass[str]):
    def __init__(self, length: int = -1) -> None:
        self.length = length

    def read(self, buf: IBuffer, *, memo: Memo) -> str:
        return buf.read_wstr(self.length)

    def write(self, buf: OBuffer, obj: str, *, memo: Memo) -> None:
        buf.write_wstr(obj, self.length)


class Bytes(DataClass[bytes]):
    def __init__(self, size: int = None) -> None:
        self.size = size

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        if self.size is None:
            return buf.read()
        return buf.read(self.size)

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        if self.size is not None:
            assert len(obj) == self.size
        buf.write(obj)


# compositions of dataclasses:
class Const(DataClass[T]):
    def __init__(
        self,
        dcls: DataClass[T],
        value: T,
        msg: str = None,
    ) -> None:
        self.dcls = dcls
        self.value = value
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        obj = self.dcls.read(buf, memo=memo)
        if obj != self.value:
            raise DataClassError(
                f'Object {obj!r} should be equal to const {self.value!r}'
                + f' ({self.msg})' * (self.msg is not None)
            )
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        if obj != self.value:
            raise DataClassError(
                f'Object {obj!r} should be equal to const {self.value!r}'
                + f' ({self.msg})' * (self.msg is not None)
            )
        self.dcls.write(buf, obj, memo=memo)


class List(DataClass[list[T]]):
    def __init__(
        self,
        dcls: DataClass[T],
        lensize: int = 4,
        byteorder: Literal['little', 'big'] = 'little',
        lencorrection: int = 0,
    ) -> None:
        self.dcls = dcls
        self.lensize = lensize
        self.byteorder = byteorder
        self.lencorrection = lencorrection

    def read(self, buf: IBuffer, *, memo: Memo) -> list[T]:
        length = int.from_bytes(buf.read(self.lensize), self.byteorder) + self.lencorrection
        if length > 2000:
            raise DataClassError(f'List too long: {length}')  # FIXME
        # print(f'Length of list is {length}') # FIXME
        result: list[T] = []
        for _ in range(length):
            try:
                obj = self.dcls.read(buf, memo=memo)
            except Exception as exc:
                print(f'Error in List dataclass. Partially readed data ({_}/{length} items):')
                # pprint(result, sort_dicts=False)
                print()
                raise DataClassError(
                    f'Error in reading {self.dcls.__class__} item at index {_+1}/{length}'
                ) from exc
            result.append(obj)
        return result

    def write(self, buf: OBuffer, obj: list[T], *, memo: Memo) -> None:
        buf.write((len(obj) - self.lencorrection).to_bytes(self.lensize, self.byteorder))
        for i, item in enumerate(obj):
            try:
                self.dcls.write(buf, item, memo=memo)
            except Exception as exc:
                print(f'Error in List dataclass. Partially readed data ({i}/{len(obj)} items):')
                # pprint(result, sort_dicts=False)
                print()
                raise DataClassError(
                    f'Error in reading {self.dcls.__class__} item at index {i+1}/{len(obj)}'
                ) from exc


class Sequence(DataClass[tuple[Any, ...]]):  # type: ignore[misc]
    def __init__(self, *dclss: DataClass[Any]) -> None:
        self.dclss = dclss

    def read(self, buf: IBuffer, *, memo: Memo) -> tuple[Any, ...]:
        result = []
        for dcls in self.dclss:
            item = dcls.read(buf, memo=memo)
            result.append(item)
        return tuple(result)

    def write(self, buf: OBuffer, obj: tuple[Any, ...], *, memo: Memo) -> None:
        assert len(self.dclss) == len(obj)
        for item, writer in zip(obj, self.dclss):
            writer.write(buf, item, memo=memo)


class Pair(DataClass[tuple[T, T]]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> tuple[T, T]:
        return self.dcls.read(buf, memo=memo), self.dcls.read(buf, memo=memo)

    def write(self, buf: OBuffer, obj: tuple[T, T], *, memo: Memo) -> None:
        self.dcls.write(buf, obj[0], memo=memo)
        self.dcls.write(buf, obj[1], memo=memo)


class Repeat(DataClass[list[T]]):
    def __init__(self, dcls: DataClass[T], n: int = None) -> None:
        self.dcls = dcls
        self.n = n

    def read(self, buf: IBuffer, *, memo: Memo) -> list[T]:
        res: list[T] = []
        assert self.n is not None
        for _ in range(self.n):
            res.append(self.dcls.read(buf, memo=memo))
        return res

    def write(self, buf: OBuffer, obj: list[T], *, memo: Memo) -> None:
        if self.n is not None:
            assert len(obj) == self.n
        for item in obj:
            self.dcls.write(buf, item, memo=memo)


class NamedSequence(DataClass[dict[str, Any]]):
    def __init__(self, **kwargs: DataClass[Any]) -> None:
        self.kwargs = kwargs

    def read(self, buf: IBuffer, *, memo: Memo) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name, dcls in self.kwargs.items():
            try:
                obj = dcls.read(buf, memo=memo)
                if not name.startswith('__'):
                    result[name] = obj
            except Exception as exc:
                pprint(result, sort_dicts=False)
                input('wait after crash')
                raise DataClassError(f'Error in item {name} of type {dcls.__class__}') from exc
        return result

    def write(self, buf: OBuffer, obj: dict[str, Any], *, memo: Memo) -> None:
        for name, dcls in self.kwargs.items():
            try:
                if name not in obj and name.startswith('__'):
                    dcls.write(buf, None, memo=memo)
                else:
                    dcls.write(buf, obj[name], memo=memo)
            except Exception as exc:
                # pprint(result, sort_dicts=False)
                input('wait after crash')
                raise DataClassError(f'Error in item {name} of type {dcls.__class__}') from exc


class DerivedNamedSequence(DataClass[dict[str, Any]]):
    def __init__(
        self, dcls: NamedSequence | DerivedNamedSequence, **kwargs: DataClass[Any]
    ) -> None:
        self.dcls = dcls
        self.kwargs = kwargs

    def read(self, buf: IBuffer, *, memo: Memo) -> dict[str, Any]:
        result: dict[str, Any] = self.dcls.read(buf, memo=memo)

        for name, dcls in self.kwargs.items():
            try:
                obj = dcls.read(buf, memo=memo)
                if not name.startswith('__'):
                    result[name] = obj
            except Exception as exc:
                print(
                    f'error in DerivedNamedSequence at item {name} of type {dcls.__class__.__name__}: {exc}'
                )
                print('readed data:')
                pprint(result, sort_dicts=False)
                raise

        return result

    def write(self, buf: OBuffer, obj: dict[str, Any], *, memo: Memo) -> None:
        self.dcls.write(buf, obj, memo=memo)
        for name, dcls in self.kwargs.items():
            try:
                if name not in obj and name.startswith('__'):
                    dcls.write(buf, None, memo=memo)
                else:
                    dcls.write(buf, obj[name], memo=memo)
            except Exception as exc:
                print(
                    f'error in DerivedNamedSequence at item {name} of type {dcls.__class__.__name__}: {exc}'
                )
                raise


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

    def read(self, buf: IBuffer, *, memo: Memo) -> G:
        assert self.decode is not None
        return self.decode(self.dcls.read(buf, memo=memo))

    def write(self, buf: OBuffer, obj: G, *, memo: Memo) -> None:
        assert self.encode is not None
        self.dcls.write(buf, self.encode(obj), memo=memo)


class CustomCallable(DataClass[T]):
    def __init__(
        self,
        *,
        decode: Callable[[IBuffer], T],
        encode: Callable[[OBuffer, T], None],
    ) -> None:
        self.decode = decode
        self.encode = encode

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return self.decode(buf)

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        self.encode(buf, obj)


class Nested(DataClass[T]):
    def __init__(self, dcls1: DataClass[bytes], dcls2: DataClass[T]) -> None:
        self.dcls1 = dcls1
        self.dcls2 = dcls2

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        data = self.dcls1.read(buf, memo=memo)
        obj = self.dcls2.read(IBuffer(data), memo=memo)
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        buf2 = OBuffer()
        self.dcls2.write(buf2, obj, memo=memo)
        data = bytes(buf2)
        self.dcls1.write(buf, data, memo=memo)


class Selector(DataClass[tuple[int, T]]):
    def __init__(self, base: DataClass[int], dclss: dict[int | EllipsisType, DataClass[T]]) -> None:
        self.base = base
        self.dclss = dclss

    def read(self, buf: IBuffer, *, memo: Memo) -> tuple[int, T]:
        n = self.base.read(buf, memo=memo)
        if n not in self.dclss:
            if ... not in self.dclss:
                raise DataClassError(
                    f'Selector value not in dict: value={n} keys={self.dclss.keys()}'
                )
            return n, self.dclss[...].read(buf, memo=memo)
        return n, self.dclss[n].read(buf, memo=memo)

    def write(self, buf: OBuffer, obj: tuple[int, T], *, memo: Memo) -> None:
        n = obj[0]
        if n not in self.dclss:
            if ... not in self.dclss:
                raise DataClassError(
                    f'Selector value not in dict: value={n} keys={self.dclss.keys()}'
                )
            self.dclss[...].write(buf, obj[1], memo=memo)
        else:
            self.dclss[n].write(buf, obj[1], memo=memo)


# SR-specific dataclasses:
class BufEC(DataClass[bytes]):
    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        size = buf.read_uint()
        data = buf.read(size)
        return data

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        buf.write_uint(len(obj))
        buf.write(obj)


class CryptedRand31pm(DataClass[bytes]):
    def __init__(self, key: int, seed: int = None, prepend_size: bool = False) -> None:
        self.key = key
        self.seed = random.randint(-(2 ** 31), 2 ** 31 - 1) if seed is None else seed
        self.prepend_size = prepend_size

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        content_hash = buf.read_uint()
        rnd = rand31pm(buf.read_int() ^ self.key)
        dout = OBuffer()

        if self.prepend_size:
            size = buf.read_uint()
            print(f'{size = }')
            dout.write_uint(size)
            for _ in range(size):
                dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))

        else:
            while buf:
                dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))

        print(dout.pos, '/', len(dout))
        result = bytes(dout)
        if self.prepend_size:
            actual_hash = zlib.crc32(result[4:])
        else:
            actual_hash = zlib.crc32(result)
        # print(f'hash = {actual_hash}')
        print(f'len of readed data = {len(result)}')
        # input('...')
        if actual_hash != content_hash:
            raise ValueError(
                f'Content hash 0x{content_hash:x} dont match actual hash 0x{actual_hash:x}'
            )
        return result

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        rnd = rand31pm(self.seed)
        if self.prepend_size:
            buf.write_uint(zlib.crc32(obj[4:]))
        else:
            buf.write_uint(zlib.crc32(obj))

        buf.write_int(self.seed ^ self.key)

        din = IBuffer(obj)

        if self.prepend_size:
            buf.write_uint(din.read_uint())
            # buf.write_uint(len(obj))

        while din:
            buf.write_byte(din.read_byte() ^ (next(rnd) & 0xFF))


class ZL(DataClass[bytes]):
    def __init__(self, mode: int, **kwargs) -> None:
        # FIXME fix kwargs
        assert mode in {1, 2, 3}
        self.mode = mode
        self.kwargs = kwargs

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        if self.mode == 1:
            # print(buf.format_str(10, 10))
            # breakpoint()

            if 'length' in self.kwargs:
                size = self.kwargs['length']
                if size == -1:
                    size = buf.bytes_remains()
            else:
                size = buf.read_uint()

            if 'optional' in self.kwargs:
                optional = self.kwargs['optional']
            else:
                optional = False

            magic = buf.read(4)
            if optional and magic == b'\0\0\0\0':
                return b''

            # print(buf)
            assert magic == b'ZL01', magic
            decompressed_size = buf.read_uint()
            compressed_data = buf.read(size - 8)
            data = zlib.decompress(compressed_data)
            assert len(data) == decompressed_size
            print(f'{decompressed_size = }')
            return data

        if self.mode == 2:
            pass

        if self.mode == 3:
            pass

        raise ValueError(f'Unknown ZL mode: {self.mode}')

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        if self.mode == 1:
            if 'length' in self.kwargs:
                if self.kwargs['length'] != -1:
                    buf.write_uint(self.kwargs['length'])


            if 'optional' in self.kwargs:
                optional = self.kwargs['optional']
            else:
                optional = False

            if optional and not obj:
                buf.write(b'\0\0\0\0')
                return

            compressed = zlib.compress(obj, level=9)
            if 'length' not in self.kwargs:
                buf.write_uint(len(compressed) + 8)

            buf.write(b'ZL01')
            buf.write_uint(len(obj))
            data = zlib.compress(obj, level=9)
            buf.write(data)
            return

        if self.mode == 2:
            return

        if self.mode == 3:
            return

        raise ValueError(f'Unknown ZL mode: {self.mode}')


class ConstValue(DataClass[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return self.value

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        if obj != self.value:
            raise ValueError(f'Object {obj!r} should be equal to const {self.value!r}')


class AddToMemo(DataClass[T]):
    def __init__(self, name: Hashable, dcls: DataClass[T]) -> None:
        self.dcls = dcls
        self.name = name

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        obj = self.dcls.read(buf, memo=memo)
        memo[self.name] = obj
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        memo[self.name] = obj
        self.dcls.write(buf, obj, memo=memo)


# dataclasses for debugging:
class Skip(NullDataClass):
    def __init__(self, n: int) -> None:
        self.n = n

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        buf.pos += self.n

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        buf.pos += self.n


class Raise(NullDataClass):
    def __init__(
        self,
        exc: Exception | type[Exception] | None = None,
        cnt=1,
    ) -> None:
        self.exc = (
            exc
            if exc is not None
            else DataClassError(f'Exception from {self.__class__.__name__} dataclass')
        )
        self.cnt = cnt

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        self.cnt -= 1
        if self.cnt == 0:
            raise self.exc

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        self.cnt -= 1
        if self.cnt == 0:
            raise self.exc


class Log(NullDataClass):
    def __init__(self, msg: str = '<log>', before=170, after=10) -> None:
        self.msg = msg
        self.before = before
        self.after = after

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        print(self.msg)
        print(buf.format_str(self.before, self.after), flush=True)
        print()

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        print(self.msg)
        print(buf.format_str(self.before, self.after), flush=True)
        print()


class DumpTo(NullDataClass):
    def __init__(self, filename: str, mode: Literal['t', 'b'] = 't') -> None:
        self.filename = filename
        self.mode = mode

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        print('dumping...')
        buf.dump_to_file(self.filename, self.mode)
        print('ok')

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        print('dumping...')
        buf.dump_to_file(self.filename, self.mode)
        print('ok')


class PrintMsg(NullDataClass):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        print(self.msg)

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        print(self.msg)


class PrintMemo(NullDataClass):
    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        pprint(memo, sort_dicts=False)

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        pprint(memo, sort_dicts=False)


class Print(DataClass[T]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        obj = self.dcls.read(buf, memo=memo)
        pprint(obj, sort_dicts=False)
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        pprint(obj, sort_dicts=False)
        self.dcls.write(buf, obj, memo=memo)


class Hide(DataClass[str]):
    def __init__(self, dcls: DataClass) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> str:
        res = self.dcls.read(buf, memo=memo)
        if isinstance(res, (bytes, str, list, tuple)):
            return f'<hidden {len(res)} items>'
        return '<hidden>'

    def write(self, buf: OBuffer, obj: str, *, memo: Memo) -> NoReturn:
        raise DataClassError(f'Cannot write read-only dataclass {self.__class__.__name__}')


class LogOnException(DataClass[T]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        try:
            return self.dcls.read(buf, memo=memo)
        except:
            print(f'Exception in dataclass {self.dcls.__class__.__name__} occured. Buffer:')
            print(buf.format_str(50, 50))
            raise

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        try:
            self.dcls.write(buf, obj, memo=memo)
        except:
            print(f'Exception in dataclass {self.dcls.__class__.__name__} occured. Buffer:')
            print(buf.format_str(50, 50))
            raise


class Lookup(DataClass[T]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return self.dcls.read(buf, memo=memo)

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        self.dcls.write(buf, obj, memo=memo)


class Wait(NullDataClass):
    def __init__(self, msg: str = '') -> None:
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        print(f'Wait dcls: {self.msg}')
        # print(buf.format_str(3, 20))
        input()

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        print(f'Wait dcls: {self.msg}')
        # print(buf.format_str(3, 20))
        input()


class Breakpoint(NullDataClass):
    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        breakpoint()

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        breakpoint()
