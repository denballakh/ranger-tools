from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Sized,
    TypeVar,
    Literal,
    Generic,
    Callable,
    # Iterator,
    final,
    NoReturn,
    # Protocol,
    Hashable,
    ClassVar,
    overload,
    Collection,
)

from types import EllipsisType

import zlib
import random
from pprint import pprint

from mypy_extensions import trait

from ..buffer import IBuffer, OBuffer
from ..common import rand31pm
from .bidict import bidict


T = TypeVar('T')
G = TypeVar('G')
TSO = TypeVar('TSO', bound='SerializableObject')


class DataClassError(Exception):
    pass


class Memo(dict):
    pass


class SerializableObject:
    __dcls__: ClassVar[DataClass[dict[str, Any]]]
    __dcls_map__: ClassVar[bidict[str, str]]  # key to attr

    @classmethod
    def __dcls_new__(cls: type[TSO]) -> TSO:
        return cls()

    def __dcls_before_save__(self) -> None:
        pass

    def __dcls_after_load__(self) -> None:
        pass

    @classmethod
    def __dcls_from_dict__(cls: type[TSO], obj: dict[str, Any]) -> TSO:
        self = cls.__dcls_new__()
        for key, attr in cls.__dcls_map__.proxy.items():
            assert key in obj
            setattr(self, attr, obj[key])

        self.__dcls_after_load__()
        return self

    def __dcls_to_dict__(self: TSO) -> dict[str, Any]:
        self.__dcls_before_save__()

        obj = dict[str, Any]()
        for key, attr in self.__class__.__dcls_map__.proxy.items():
            obj[key] = getattr(self, attr)

        return obj

    @classmethod
    def __dcls_from_buffer__(cls: type[TSO], buf: IBuffer) -> TSO:
        return cls.__dcls_from_dict__(buf.read_dcls(cls.__dcls__))

    def __dcls_to_buffer__(self, buf: OBuffer) -> None:
        buf.write_dcls(self.__class__.__dcls__, self.__dcls_to_dict__())


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
class ReadOnlyDataClass(DataClass[T]):
    __slots__ = ()

    @final
    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> NoReturn:
        raise DataClassError(f'Cannot write read-only {self.__class__.__name__} object')


@trait
class WriteOnlyDataClass(DataClass[T]):
    __slots__ = ()

    @final
    def read(self, buf: IBuffer, *, memo: Memo) -> NoReturn:
        raise DataClassError(f'Cannot read write-only {self.__class__.__name__} object')


class NullDataClass(DataClass[None]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        return None

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None


# atomic dataclasses:
class Bool(DataClass[bool]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> bool:
        return buf.read_bool()

    def write(self, buf: OBuffer, obj: bool, *, memo: Memo) -> None:
        buf.write_bool(obj)


class Byte(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_byte()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_byte(obj)


class Int8(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_char()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_char(obj)


class UInt8(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_uchar()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_uchar(obj)


class Int16(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_short()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_short(obj)


class UInt16(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_ushort()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_ushort(obj)


class Int32(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_int()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_int(obj)


class UInt32(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_uint()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_uint(obj)


class Int64(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_long()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_long(obj)


class UInt64(DataClass[int]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return buf.read_ulong()

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write_ulong(obj)


class Float(DataClass[float]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> float:
        return buf.read_float()

    def write(self, buf: OBuffer, obj: float, *, memo: Memo) -> None:
        buf.write_float(obj)


class Double(DataClass[float]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> float:
        return buf.read_double()

    def write(self, buf: OBuffer, obj: float, *, memo: Memo) -> None:
        buf.write_double(obj)


class Str(DataClass[str]):
    __slots__ = ('length',)

    def __init__(self, length: int = -1) -> None:
        self.length = length

    def read(self, buf: IBuffer, *, memo: Memo) -> str:
        return buf.read_str(self.length)

    def write(self, buf: OBuffer, obj: str, *, memo: Memo) -> None:
        buf.write_str(obj, self.length)


class WStr(DataClass[str]):
    __slots__ = ('length',)

    def __init__(self, length: int = -1) -> None:
        self.length = length

    def read(self, buf: IBuffer, *, memo: Memo) -> str:
        return buf.read_wstr(self.length)

    def write(self, buf: OBuffer, obj: str, *, memo: Memo) -> None:
        buf.write_wstr(obj, self.length)


class Bytes(DataClass[bytes]):
    __slots__ = ('size',)

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


class AnyOf(DataClass[T]):
    __slots__ = ('dcls', 'values', 'msg')

    def __init__(
        self,
        dcls: DataClass[T],
        values: Collection[T],
        msg: str = None,
    ) -> None:
        self.dcls = dcls
        self.values = set(values)
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        obj = self.dcls.read(buf, memo=memo)
        if obj not in self.values:
            raise DataClassError(
                f'Object {obj!r} should be in {self.values!r}'
                + f' ({self.msg})' * (self.msg is not None)
            )
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        if obj not in self.values:
            raise DataClassError(
                f'Object {obj!r} should be in {self.values!r}'
                + f' ({self.msg})' * (self.msg is not None)
            )
        self.dcls.write(buf, obj, memo=memo)


def Const(dcls: DataClass[T], value: T, msg: str = None) -> AnyOf[T]:
    return AnyOf(dcls, (value,), msg)


class ConstValue(DataClass[T]):
    __slots__ = ('value',)

    def __init__(self, value: T) -> None:
        self.value = value

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return self.value

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        if obj != self.value:
            raise ValueError(f'Object {obj!r} should be equal to const {self.value!r}')


class ShadowedConst(DataClass[T]):
    __slots__ = ('dcls', 'value')

    def __init__(self, dcls: DataClass[T], value: T) -> None:
        self.dcls = dcls
        self.value = value

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        self.dcls.read(buf, memo=memo)
        return self.value

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        self.dcls.write(buf, self.value, memo=memo)


class List(DataClass[list[T]]):
    __slots__ = ('dcls', 'lensize', 'byteorder')

    def __init__(
        self,
        dcls: DataClass[T],
        lensize: int = 4,
        byteorder: Literal['little', 'big'] = 'little',
    ) -> None:
        self.dcls = dcls
        self.lensize = lensize
        self.byteorder: Literal['little', 'big'] = byteorder

    def read(self, buf: IBuffer, *, memo: Memo) -> list[T]:
        length = int.from_bytes(buf.read(self.lensize), self.byteorder)
        result = list[T]()
        for i in range(length):
            try:
                obj = self.dcls.read(buf, memo=memo)
            except Exception as exc:
                print(buf.format_str(10, 10))
                print(f'Error in List dataclass. Partially readed data ({i}/{length} items):')
                # pprint(result, sort_dicts=False)
                print()
                raise DataClassError(
                    f'Error in reading {self.dcls.__class__} item at index {i+1}/{length}'
                ) from exc
            result.append(obj)
        return result

    def write(self, buf: OBuffer, obj: list[T], *, memo: Memo) -> None:
        buf.write((len(obj)).to_bytes(self.lensize, self.byteorder))
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


class Sequence(DataClass[tuple[Any, ...]]):
    __slots__ = ('dclss',)

    def __init__(self, *dclss: DataClass[Any]) -> None:
        self.dclss = dclss

    def read(self, buf: IBuffer, *, memo: Memo) -> tuple[Any, ...]:
        result: list[Any] = []
        for dcls in self.dclss:
            item = dcls.read(buf, memo=memo)
            result.append(item)
        return tuple[Any, ...](result)

    def write(self, buf: OBuffer, obj: tuple[Any, ...] | list[Any], *, memo: Memo) -> None:
        assert len(self.dclss) == len(obj)
        for item, writer in zip(obj, self.dclss):
            writer.write(buf, item, memo=memo)


def Pair(dcls: DataClass[T]) -> DataClass[tuple[T, T]]:
    return Sequence(dcls, dcls)  # type: ignore[return-value]


def Repeat(dcls: DataClass[T], n: int) -> DataClass[tuple[T, ...]]:
    return Sequence(*[dcls] * n)


class NamedSequence(DataClass[dict[str, Any]]):
    __slots__ = (
        'base',
        'kwargs',
    )

    def __init__(self, base: NamedSequence = None, /, **kwargs: DataClass[Any]) -> None:
        self.base = base
        self.kwargs = kwargs

    def read(self, buf: IBuffer, *, memo: Memo) -> dict[str, Any]:
        result = self.base.read(buf, memo=memo) if self.base is not None else dict[str, Any]()
        for name, dcls in self.kwargs.items():
            try:
                obj = dcls.read(buf, memo=memo)
                if not name.startswith('__'):
                    result[name] = obj
            except Exception as exc:
                raise DataClassError(f'Error in item {name} of type {dcls.__class__}') from exc
        return result

    def write(self, buf: OBuffer, obj: dict[str, Any], *, memo: Memo) -> None:
        if self.base is not None:
            self.base.write(buf, obj, memo=memo)

        for name, dcls in self.kwargs.items():
            try:
                if name not in obj and name.startswith('__'):
                    dcls.write(buf, None, memo=memo)
                else:
                    dcls.write(buf, obj[name], memo=memo)
            except Exception as exc:
                raise DataClassError(f'Error in item {name} of type {dcls.__class__}') from exc


class CustomCallable(DataClass[T]):
    __slots__ = ('decode', 'encode')

    def __init__(
        self,
        *,
        decode: Callable[[IBuffer, Memo], T],
        encode: Callable[[OBuffer, T, Memo], Any],
    ) -> None:
        self.decode = decode
        self.encode = encode

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return self.decode(buf, memo)

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        self.encode(buf, obj, memo)


def Converted(
    dcls: DataClass[T],
    *,
    decode: Callable[[T], G],
    encode: Callable[[G], T],
) -> CustomCallable[G]:
    return CustomCallable(
        decode=lambda buf, memo: decode(dcls.read(buf, memo=memo)),
        encode=lambda buf, obj, memo: dcls.write(buf, encode(obj), memo=memo),
    )


class Nested(DataClass[T]):
    __slots__ = ('dcls1', 'dcls2')

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


class Selector(DataClass[tuple[G, T]]):
    __slots__ = ('base', 'dclss')

    def __init__(
        self: Selector[G, T], base: DataClass[G], dclss: dict[G | EllipsisType, DataClass[Any]]
    ) -> None:
        self.base = base
        self.dclss = dclss

    def read(self: Selector[G, T], buf: IBuffer, *, memo: Memo) -> tuple[G, T]:
        n = self.base.read(buf, memo=memo)
        if n not in self.dclss:
            if ... not in self.dclss:
                print(buf.format_str(10, 10))
                raise DataClassError(
                    f'Selector value not in dict: value={n} keys={self.dclss.keys()}'
                )
            return n, self.dclss[...].read(buf, memo=memo)
        return n, self.dclss[n].read(buf, memo=memo)

    def write(self: Selector[G, T], buf: OBuffer, obj: tuple[G, T] | list, *, memo: Memo) -> None:
        n = obj[0]
        self.base.write(buf, n, memo=memo)
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
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        size = buf.read_uint()
        data = buf.read(size)
        return data

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        buf.write_uint(len(obj))
        buf.write(obj)


class CryptedRand31pm(DataClass[bytes]):
    __slots__ = ('key', 'seed', 'prepend_size')

    def __init__(self, key: int, seed: int = None, prepend_size: bool = False) -> None:
        self.key = key
        self.seed = random.randint(-0x80000000, 0x7FFFFFFF) if seed is None else seed
        self.prepend_size = prepend_size

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        content_hash = buf.read_uint()
        rnd = rand31pm(buf.read_int() ^ self.key)
        dout = OBuffer()

        if self.prepend_size:
            size = buf.read_uint()
            dout.write_uint(size)
            for _ in range(size):
                dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))

        else:
            while buf:
                dout.write_byte(buf.read_byte() ^ (next(rnd) & 0xFF))

        result = bytes(dout)
        if self.prepend_size:
            actual_hash = zlib.crc32(result[4:])
        else:
            actual_hash = zlib.crc32(result)
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

        while din:
            buf.write_byte(din.read_byte() ^ (next(rnd) & 0xFF))


class ZL(DataClass[bytes]):
    __slots__ = ('mode', 'length', 'optional')

    def __init__(self, mode: int, length: int = None, optional: bool = False) -> None:
        assert mode in {1, 2, 3}
        self.mode = mode
        self.length = length
        self.optional = optional

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        if self.mode == 1:
            if self.length is None:
                size = buf.read_uint()
            else:
                size = self.length
                if size == -1:
                    size = buf.bytes_remains()

            magic = buf.read(4)
            if self.optional and magic == b'\0\0\0\0':
                return b''

            assert magic == b'ZL01', magic
            decompressed_size = buf.read_uint()
            compressed_data = buf.read(size - 8)
            data = zlib.decompress(compressed_data)
            assert len(data) == decompressed_size
            return data

        if self.mode == 2:
            raise NotImplementedError

        if self.mode == 3:
            raise NotImplementedError

        raise ValueError(f'Unknown ZL mode: {self.mode}')

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        if self.mode == 1:
            if self.length is not None:
                if self.length != -1:
                    buf.write_uint(self.length)

            if self.optional and not obj:
                buf.write(b'\0\0\0\0')
                return

            compressed = zlib.compress(obj, level=9)
            if self.length is None:
                buf.write_uint(len(compressed) + 8)

            buf.write(b'ZL01')
            buf.write_uint(len(obj))
            buf.write(compressed)
            return

        if self.mode == 2:
            raise NotImplementedError

        if self.mode == 3:
            raise NotImplementedError

        raise ValueError(f'Unknown ZL mode: {self.mode}')


class CRC(DataClass[bytes]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        crc = buf.read_uint()
        data = buf.read()
        if crc != zlib.crc32(data):
            raise DataClassError('Content hash dont match actual hash')
        return data

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        buf.write_uint(zlib.crc32(obj))
        buf.write(obj)


# dataclasses for consistency testing
class AssertOnEnd(DataClass[None]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        if not buf.pos == len(buf):
            raise DataClassError

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        pass


class Raise(NullDataClass):
    __slots__ = ('exc', 'cnt')

    def __init__(
        self,
        exc: Exception | type[Exception] | None = None,
        cnt: int = 1,
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


# memo-related:
class AddToMemo(DataClass[T]):
    __slots__ = ('dcls', 'name')

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


class GetFromMemo(DataClass[T]):
    __slots__ = ('name',)

    def __init__(self, name: Hashable) -> None:
        self.name = name

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return memo[self.name]

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        pass


# dataclasses for debugging:
class _Skip(NullDataClass):
    def __init__(self, n: int) -> None:
        self.n = n

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        buf.pos += self.n

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        buf.pos += self.n


class _Log(NullDataClass):
    def __init__(self, msg: str = '<log>', before: int = 170, after: int = 10) -> None:
        self.msg = msg
        self.before = before
        self.after = after

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        print(self.msg)
        print(buf.format_str(self.before, self.after))
        print()

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        print(self.msg)
        print(buf.format_str(self.before, self.after))
        print()


class _DumpTo(NullDataClass):
    def __init__(self, filename: str, mode: Literal['t', 'b'] = 't') -> None:
        self.filename = filename
        self.mode: Literal['t', 'b'] = mode

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        buf.dump_to_file(self.filename, self.mode)

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        buf.dump_to_file(self.filename, self.mode)


class _PrintMsg(NullDataClass):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        print(self.msg)

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        assert obj is None
        print(self.msg)


class _PrintMemo(NullDataClass):
    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        pprint(memo, sort_dicts=False)

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        pprint(memo, sort_dicts=False)


class _Print(DataClass[T]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        obj = self.dcls.read(buf, memo=memo)
        pprint(obj, sort_dicts=False)
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        pprint(obj, sort_dicts=False)
        self.dcls.write(buf, obj, memo=memo)


class _Hide(ReadOnlyDataClass[str]):
    def __init__(self, dcls: DataClass[object]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> str:
        res = self.dcls.read(buf, memo=memo)
        if isinstance(res, Sized):
            return f'<hidden {res.__class__.__name__}[{len(res)}]>'
        return f'<hidden {res.__class__.__name__}>'


class _LogOnException(DataClass[T]):
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


class _Wait(NullDataClass):
    def __init__(self, msg: str = '') -> None:
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        input(f'Wait: {self.msg}')

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        input(f'Wait: {self.msg}')


class _Breakpoint(NullDataClass):
    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        breakpoint()

    def write(self, buf: OBuffer, obj: Any, *, memo: Memo) -> None:
        breakpoint()
