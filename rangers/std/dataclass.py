from __future__ import annotations
import struct

from typing import (
    Any,
    Container,
    Sized,
    TypeVar,
    Literal,
    Generic,
    Callable,
    final,
    NoReturn,
    Hashable,
    ClassVar,
    Sequence as Sequence_,
)

from types import EllipsisType

import zlib
import random
from pprint import pprint

from mypy_extensions import trait

from ..buffer import IBuffer, OBuffer
from ..common import assert_, rand31pm
from .bidict import bidict


T = TypeVar('T')
G = TypeVar('G')
TSO = TypeVar('TSO', bound='SerializableObject')
# Namespace = dict[str, Any]


class DataClassError(Exception):
    pass


class Memo(dict[Hashable, Any]):
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

        obj: dict[str, Any] = {}
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
        if obj is not None:
            raise ValueError(obj)


class SizedInt(DataClass[int]):
    __slots__ = ('size', 'byteorder', 'signed')
    size: int
    byteorder: Literal['big', 'little']
    signed: bool

    def __init__(
        self,
        size: int = 4,
        byteorder: Literal['big', 'little'] = 'little',
        signed: bool = True,
    ) -> None:
        self.size = size
        self.byteorder = byteorder
        self.signed = signed

    def read(self, buf: IBuffer, *, memo: Memo) -> int:
        return int.from_bytes(
            buf.read(self.size),
            byteorder=self.byteorder,
            signed=self.signed,
        )

    def write(self, buf: OBuffer, obj: int, *, memo: Memo) -> None:
        buf.write(
            obj.to_bytes(
                self.size,
                byteorder=self.byteorder,
                signed=self.signed,
            )
        )


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


class StructFormat(DataClass[T]):
    __slots__ = ('struct',)
    struct: struct.Struct

    def __init__(self, fmt: str) -> None:
        self.struct = struct.Struct(fmt)

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        return buf.read_struct(self.struct)[0]

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        buf.write_struct(self.struct, obj)
def SizedStr(length: int = None) -> DataClass[str]:
    return CustomCallable(
        decode=lambda buf, memo: buf.read_str(length),
        encode=lambda buf, obj, memo: buf.write_str(obj, length),
    )


def SizedWStr(length: int = None) -> DataClass[str]:
    return CustomCallable(
        decode=lambda buf, memo: buf.read_wstr(length),
        encode=lambda buf, obj, memo: buf.write_wstr(obj, length),
    )


DNone = NullDataClass()

Byte = StructFormat[int]('B')
Bool = StructFormat[bool]('?')

Int8 = StructFormat[int]('b')
UInt8 = StructFormat[int]('B')

Int16 = StructFormat[int]('<h')
UInt16 = StructFormat[int]('<H')

Int32 = StructFormat[int]('<i')
UInt32 = StructFormat[int]('<I')

Int64 = StructFormat[int]('<q')
UInt64 = StructFormat[int]('<Q')

Float = StructFormat[int]('<f')
Double = StructFormat[int]('<d')

Bool32 = UInt32  # FIXME

Str = SizedStr()
WStr = SizedWStr()


class Bytes(DataClass[bytes]):
    __slots__ = ('size',)

    def __init__(self, size: int = None) -> None:
        self.size = size

    def read(self, buf: IBuffer, *, memo: Memo) -> bytes:
        return buf.read(self.size)

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        if self.size is not None and len(obj) != self.size:
            raise ValueError(len(obj), self.size)
        buf.write(obj)


class Maybe(DataClass[T | None]):
    __slots__ = ('dcls', 'base')
    dcls: DataClass[T]
    base: DataClass[bool]

    def __init__(
        self,
        dcls: DataClass[T],
        base: DataClass[bool] = Bool,
    ) -> None:
        self.dcls = dcls
        self.base = base

    def read(self, buf: IBuffer, *, memo: Memo) -> T | None:
        b = self.base.read(buf, memo=memo)
        if not b:
            return None
        obj = self.dcls.read(buf, memo=memo)
        assert obj is not None
        return obj

    def write(self, buf: OBuffer, obj: T | None, *, memo: Memo) -> None:
        if obj is None:
            self.base.write(buf, False, memo=memo)
        else:
            self.base.write(buf, True, memo=memo)
            self.dcls.write(buf, obj, memo=memo)


# compositions of dataclasses:


class AnyOf(DataClass[T]):
    __slots__ = ('dcls', 'values', 'msg')
    dcls: DataClass[T]
    values: Container[T]
    msg: str | None

    def __init__(
        self,
        dcls: DataClass[T],
        values: Container[T],
        msg: str = None,
    ) -> None:
        self.dcls = dcls
        self.values = values
        self.msg = msg

    def read(self, buf: IBuffer, *, memo: Memo) -> T:
        obj = self.dcls.read(buf, memo=memo)
        if obj not in self.values:
            raise ValueError(
                f'Value {obj!r} should be in this set of values: {self.values!r}'
                + f'\n\t{self.msg}' * (self.msg is not None)
            )
        return obj

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        if obj not in self.values:
            raise ValueError(
                f'Value {obj!r} should be in this set of values: {self.values!r}'
                + f'\n\t{self.msg}' * (self.msg is not None)
            )
        self.dcls.write(buf, obj, memo=memo)


def Const(dcls: DataClass[T], value: T, msg: str = None) -> AnyOf[T]:
    return AnyOf(dcls, (value,), msg=msg)


def ConstValue(value: T) -> DataClass[T]:
    return CustomCallable(
        decode=lambda buf, memo: value,
        encode=lambda buf, obj, memo: assert_(
            obj == value, f'Object {obj!r} should be equal to const {value!r}'
        ),
    )


def ShadowedConst(dcls: DataClass[T], value: T) -> DataClass[T]:
    return Converted(
        dcls,
        decode=lambda obj: value,
        encode=lambda obj: value,
    )


class List(DataClass[list[T]]):
    __slots__ = ('dcls', 'sizedcls')
    dcls: DataClass[T]
    sizedcls: DataClass[int]

    def __init__(
        self,
        dcls: DataClass[T],
        size: DataClass[int] = UInt32,
    ) -> None:
        self.dcls = dcls
        self.sizedcls = size

    def read(self, buf: IBuffer, *, memo: Memo) -> list[T]:
        length = self.sizedcls.read(buf, memo=memo)
        assert length >= 0, length
        result: list[T] = []
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

    def write(self, buf: OBuffer, obj: Sequence_[T], *, memo: Memo) -> None:
        self.sizedcls.write(buf, len(obj), memo=memo)

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
        for i, dcls in enumerate(self.dclss):
            try:
                item = dcls.read(buf, memo=memo)
            except Exception as exc:
                raise DataClassError(
                    f'error in item of type {dcls.__class__} at index {i}/{len(self.dclss)}'
                ) from exc
            result.append(item)
        return tuple[Any, ...](result)

    def write(self, buf: OBuffer, obj: Sequence_[Any], *, memo: Memo) -> None:
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

    def __init__(
        self,
        base: DataClass[dict[Any, Any]] = None,
        /,
        **kwargs: DataClass[Any],
    ) -> None:
        self.base = base
        self.kwargs = kwargs

    def read(self, buf: IBuffer, *, memo: Memo) -> dict[str, Any]:
        result: dict[str, Any] = self.base.read(buf, memo=memo) if self.base is not None else {}
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


def HexBytes(dcls: DataClass[bytes], *, sep: str = ' ', bytes_per_sep: int = -4) -> DataClass[str]:
    return Converted(
        dcls,
        decode=lambda b: b.hex(sep=sep, bytes_per_sep=bytes_per_sep),
        encode=bytes.fromhex,
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


class Pack(DataClass[list[T]]):
    __slots__ = ('dcls',)

    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, *, memo: Memo) -> list[T]:
        result: list[T] = []
        while buf:
            result.append(self.dcls.read(buf, memo=memo))
        return result

    def write(self, buf: OBuffer, obj: list[T], *, memo: Memo) -> None:
        for item in obj:
            self.dcls.write(buf, item, memo=memo)


class Selector(DataClass[tuple[G, T]]):
    __slots__ = ('base', 'dclss')

    def __init__(
        self: Selector[G, T],
        base: DataClass[G],
        dclss: dict[G | EllipsisType, DataClass[Any]],
    ) -> None:
        self.base = base
        self.dclss = dclss

    def read(self: Selector[G, T], buf: IBuffer, *, memo: Memo) -> tuple[G, T]:
        n = self.base.read(buf, memo=memo)
        if n not in self.dclss:
            if ... not in self.dclss:
                raise ValueError(f'Selector value not in dict: value={n} keys={self.dclss.keys()}')
            return n, self.dclss[...].read(buf, memo=memo)
        return n, self.dclss[n].read(buf, memo=memo)

    def write(
        self: Selector[G, T], buf: OBuffer, obj: tuple[G, T] | list[Any], *, memo: Memo
    ) -> None:
        n = obj[0]
        self.base.write(buf, n, memo=memo)
        if n not in self.dclss:
            if ... not in self.dclss:
                raise ValueError(f'Selector value not in dict: value={n} keys={self.dclss.keys()}')
            self.dclss[...].write(buf, obj[1], memo=memo)
        else:
            self.dclss[n].write(buf, obj[1], memo=memo)


class ReadOnlySelector(ReadOnlyDataClass[T], Generic[G, T]):
    __slots__ = ('base', 'dclss')

    def __init__(
        self: ReadOnlySelector[G, T],
        base: DataClass[G],
        dclss: dict[G | EllipsisType, DataClass[T]],
    ) -> None:
        self.base = base
        self.dclss = dclss

    def read(
        self: ReadOnlySelector[G, T],
        buf: IBuffer,
        *,
        memo: Memo,
    ) -> T:
        n = self.base.read(buf, memo=memo)
        if n not in self.dclss:
            if ... not in self.dclss:
                raise ValueError(f'Selector value not in dict: value={n} keys={self.dclss.keys()}')
            return self.dclss[...].read(buf, memo=memo)
        return self.dclss[n].read(buf, memo=memo)


def MemoSelectedDataClass(selector: Callable[[Memo], DataClass[T]]) -> DataClass[T]:
    return CustomCallable(
        decode=lambda buf, memo: selector(memo).read(buf, memo=memo),
        encode=lambda buf, obj, memo: selector(memo).write(buf, obj, memo=memo),
    )


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
            raise ValueError('Content hash dont match actual hash')
        return data

    def write(self, buf: OBuffer, obj: bytes, *, memo: Memo) -> None:
        buf.write_uint(zlib.crc32(obj))
        buf.write(obj)


# dataclasses for consistency testing
class AssertOnEnd(DataClass[None]):
    __slots__ = ()

    def read(self, buf: IBuffer, *, memo: Memo) -> None:
        if not buf.pos == len(buf):
            raise DataClassError(f'{buf.pos = }, {len(buf) = }')

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
            else DataClassError(f'Exception from {self.__class__.__name__!r} dataclass')
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
    def __init__(self, msg: str = '<log>', before: int | None = 20, after: int | None = 20) -> None:
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
    def __init__(self, dcls: DataClass[Any]) -> None:
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
        except Exception:
            print(f'Exception in dataclass {self.dcls.__class__.__name__} occured. Buffer:')
            print(buf.format_str(50, 50))
            raise

    def write(self, buf: OBuffer, obj: T, *, memo: Memo) -> None:
        try:
            self.dcls.write(buf, obj, memo=memo)
        except Exception:
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
