from __future__ import annotations
from typing import (
    Any,
    Iterable,
    Iterator,
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
import builtins

from pathlib import Path
import struct
import contextlib
import warnings
import pickle
from types import EllipsisType
import textwrap
import zlib
import random
from pprint import pprint
import itertools

from .buffer import IBuffer, OBuffer

T = TypeVar('T')
G = TypeVar('G')


class DataClassError(Exception):
    def __init__(
        self,
        msg: str = '',
        *,
        dcls: DataClass[T] | None = None,
        buf: IBuffer | OBuffer | None = None,
    ) -> None:
        pass


class Memo(dict[Hashable, Any]):
    pass


_memo_stack: list[Memo] = []


def get_memo() -> Memo:
    return _memo_stack[-1]


def push_memo(memo: Memo) -> None:
    _memo_stack.append(memo)


def pop_memo() -> Memo:
    return _memo_stack.pop()


def compile(d: DataClass[T]) -> CompiledDataClass[T]:
    return DataClassCompiler().compile(d)


class DataClassCompiler:
    buf_imports: list[str]
    buf_globals: list[str]
    buf: list[str]

    indent: int
    ns: dict[str, Any]
    vars: set[str]
    R: str
    R_oneline: bool

    memo: dict[int, CompiledDataClass[Any]]

    def __init__(self) -> None:
        self.buf = []
        self.buf_imports = []
        self.buf_globals = []
        self.indent = 0
        self.ns = {}
        self.memo = {}
        self.vars = {*()}
        self.R = ''
        self.R_oneline = False

        self.add_global('D, P = B.data, B._pos')

    def __str__(self) -> str:
        return self.flush()

    __repr__ = __str__

    def flush(self) -> str:
        self.buf = [''.join(self.buf)]
        self.buf_globals = ['\n'.join(self.buf_globals)]
        self.buf_imports = ['\n'.join(self.buf_imports)]
        return self.buf_imports[0] + '\n' + self.buf_globals[0] + '\n' + self.buf[0]

    def add(self, *s: str) -> None:
        self.buf.extend(map(str, s))

    @contextlib.contextmanager
    def clean(self) -> Iterator[None]:
        self.add_line('B._pos = P')
        yield
        self.add_line('P = B._pos')

    @contextlib.contextmanager
    def block(self, s: str = '') -> Iterator[None]:
        if s:
            self.add_line(s)
        self.indent += 1
        yield
        self.indent -= 1

    @contextlib.contextmanager
    def locals(self, n: int) -> Iterator[list[str]]:
        names = [self.new_var() for name in range(n)]
        yield names
        for name in names:
            self.vars.remove(name)

    def fill(self, s: str) -> None:
        self.add('    ' * self.indent + s)

    def add_line(self, s: str) -> None:
        self.fill(s + '\n')

    def add_result(self, s: str) -> None:
        self.R = s
        self.add_line(f'R = {s}')

    def get_result(self) -> str:
        if not self.R_oneline:
            return 'R'

        assert self.R
        assert self.buf[-1].strip() == f'R = {self.R}', (self.buf[-1], self.R)
        self.buf.pop()
        return self.R

    def new_var(self, name: str = 'var') -> str:
        i = 0
        while f'{name}_{i}' in self.vars:
            i += 1
        self.vars.add(f'{name}_{i}')
        # print(end=f'{name}_{i} ')
        # if f'{name}_{i}' == 'var_16':
        # self.add_line('# IT IS HERE!!!')
        return f'{name}_{i}'

    def add_import(self, s: str) -> None:
        if s not in self.buf_imports:
            self.buf_imports.append(s)

    def add_global(self, s: str) -> None:
        if s not in self.buf_globals:
            self.buf_globals.append(s)

    def add_global_struct(self, s: struct.Struct | str) -> str:
        if isinstance(s, struct.Struct):
            s = s.format

        name = s
        name = name.replace('@', 'native')
        for a, b in (
            ('@', 'native'),
            ('=', 'native'),
            ('<', 'le'),
            ('>', 'be'),
            ('!', 'network'),
            ('?', 'bool'),
        ):
            name = name.replace(a, b)

        name = ''.join(filter(str.isidentifier, name))
        name = f'S_{name}'

        self.add_import('import struct')
        self.add_global(f'{name} = struct.Struct({s!r})')
        self.vars.add(name)
        return name

    def compile_read(self, dcls: DataClass[Any]) -> None:
        self.R_oneline = dcls.compile_read(self)

    def compile_write(self, dcls: DataClass[Any]) -> None:
        dcls.compile_write(self)

    def add_ns(self, name: str, value: Any) -> None:
        self.vars.add(name)
        self.add_global(f'# {name} = {repr(value)}')
        self.ns[name] = value

    def _value_to_repr(self, value: Any) -> str:
        if isinstance(value, type) and value.__name__ in builtins.__dict__:
            return value.__name__

        try:
            if eval(r := repr(value)) == value:
                return r
        except Exception:
            pass

        try:
            pickled = pickle.dumps(value)
            value_loaded = pickle.loads(pickled)
            if value_loaded != value:
                raise ValueError
            var = self.new_var('pickle')
            self.add_import('import pickle')
            self.add_import(f'{var} = pickle.loads({pickled!r})')
            return var
        except Exception:
            pass

        return ''

    def add_const(self, name: str, value: Any) -> str:
        if s := self._value_to_repr(value):
            return s
        name = self.new_var(name)
        self.add_ns(name, value)
        return name

    def compile(self, d: DataClass[T]) -> CompiledDataClass[T]:

        if isinstance(d, CompiledDataClass):
            return d
        if id(d) in self.memo:
            return self.memo[id(d)]

        res: CompiledDataClass[Any] = CompiledDataClass(rd=None, wt=None)  # type: ignore[arg-type]
        self.memo[id(d)] = res

        c = DataClassCompiler()
        c.memo = self.memo
        c.compile_read(d)
        c.add_line(f'B._pos = P')
        c.add_line(f'return R')
        read_code = c.flush()
        func_name = f'read_{d.__class__.__name__}_{hex(id(d))}'
        read_func_code = f'def {func_name}(B): # {d}\n'
        read_func_code += textwrap.indent(read_code, '    ')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SyntaxWarning)
            exec(read_func_code, c.ns)
        read_func = c.ns[func_name]
        del c.ns['__builtins__']

        # print('Read code:')
        print(read_func_code)
        # print()

        c = DataClassCompiler()
        c.memo = self.memo
        c.compile_write(d)
        c.add_line('pass')
        write_code = c.flush()

        write_func_code = f'def write(B, R):\n'
        write_func_code += textwrap.indent(write_code, '    ')
        exec(write_func_code, c.ns)
        write_func = c.ns['write']
        del c.ns['__builtins__']

        # print('Write code:')
        # print(f'ns = {c.ns}')
        # print(write_func_code)
        # print()

        res.rd = read_func
        res.wt = write_func

        return res

    def traverse(self, dcls: DataClass) -> None:
        pass


# protocols:
class DataClass(Generic[T]):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> T:
        raise NotImplementedError(f'Class {type(self).__name__} cannot read data.')

    def write(self, buf: OBuffer, obj: T, /) -> None:
        raise NotImplementedError(f'Class {type(self).__name__} cannot write data.')

    @final
    def read_bytes(self, data: bytes | bytearray, memo: Memo | None = None, /) -> T:
        return self.read_with_memo(IBuffer(data), memo)

    @final
    def write_bytes(self, obj: T, memo: Memo | None = None, /) -> bytes:
        buf = OBuffer()
        self.write_with_memo(buf, obj, memo)
        return bytes(buf)

    @final
    def read_with_memo(self, buf: IBuffer, memo: Memo | None = None, /) -> T:
        push_memo(memo if memo is not None else Memo())
        result = self.read(buf)
        pop_memo()
        return result

    @final
    def write_with_memo(self, buf: OBuffer, obj: T, memo: Memo | None = None, /) -> None:
        push_memo(memo if memo is not None else Memo())
        self.write(buf, obj)
        pop_memo()

    def compile_read(self, c: DataClassCompiler) -> bool:
        var = c.add_const(f'dcls_{self.__class__.__name__}', self)
        with c.clean():
            c.add_result(f'{var}.read(B)')
        return False

    def compile_write(self, c: DataClassCompiler) -> None:
        var = c.add_const(f'dcls_{self.__class__.__name__}', self)
        with c.clean():
            c.add_line(f'{var}.write(B, R)')

    def compile_traverse(self, c: DataClassCompiler) -> None:
        c.traverse(self)


class CompiledDataClass(DataClass[T]):
    __slots__ = ('rd', 'wt')
    rd: Callable[[IBuffer], T]
    wt: Callable[[OBuffer, T], Any]

    def __init__(
        self,
        rd: Callable[[IBuffer], T],
        wt: Callable[[OBuffer, T], Any],
    ) -> None:
        self.rd = rd
        self.wt = wt

    def read(self, buf: IBuffer, /) -> T:
        return self.rd(buf)

    def write(self, buf: OBuffer, obj: T, /) -> None:
        self.wt(buf, obj)

    def compile_read(self, c: DataClassCompiler) -> bool:
        var = c.add_const(self.rd.__name__, self.rd)
        with c.clean():
            c.add_result(f'{var}(B)')
        return False


class SimpleDataclass(DataClass[Any]):
    __slots__ = ()

    @final
    def compile_traverse(self) -> Iterator[DataClass[Any]]:
        yield from ()


class ReadOnlyDataClass(DataClass[T]):
    __slots__ = ()

    @final
    def write(self, buf: OBuffer, obj: T, /) -> NoReturn:
        raise DataClassError(f'Cannot write read-only {self.__class__.__name__} object')


class WriteOnlyDataClass(DataClass[T]):
    __slots__ = ()

    @final
    def read(self, buf: IBuffer, /) -> NoReturn:
        raise DataClassError(f'Cannot read write-only {self.__class__.__name__} object')


class NullDataClass(SimpleDataclass, DataClass[None]):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> None:
        return None

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        if obj is not None:
            raise ValueError(obj)

    def compile_read(self, c: DataClassCompiler) -> bool:
        c.add_result('None')
        return True


class ConstValue(DataClass[T]):
    __slots__ = ('value',)
    value: T

    def __init__(self, value: T) -> None:
        self.value = value

    def read(self, buf: IBuffer, /) -> T:
        return self.value

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        assert obj == self.value

    def compile_read(self, c: DataClassCompiler) -> bool:
        c.add_result(c.add_const('cv', self.value))
        return True


class ShadowedConst(DataClass[T]):
    __slots__ = ('dcls', 'value')
    dcls: DataClass[T]
    value: T

    def __init__(self, dcls: DataClass[T], value: T) -> None:
        self.dcls = dcls
        self.value = value

    def read(self, buf: IBuffer, /) -> T:
        self.dcls.read(buf)
        return self.value

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        self.dcls.write(buf, self.value)

    # def compile_read(self, c: DataClassCompiler) -> bool:
    #     c.add_result(c.add_const('cv', self.value))
    #     return True


def ShadowedConst_(dcls: DataClass[T], value: T) -> DataClass[T]:
    return Converted(
        dcls,
        decode=lambda obj, /: value,
        encode=lambda obj, /: value,
    )


# class SizedInt(DataClass[int]):
#     __slots__ = ('size', 'byteorder', 'signed')
#     size: int
#     byteorder: Literal['big', 'little']
#     signed: bool

#     def __init__(
#         self,
#         size: int = 4,
#         byteorder: Literal['big', 'little'] = 'little',
#         signed: bool = True,
#     ) -> None:
#         self.size = size
#         self.byteorder = byteorder
#         self.signed = signed

#     def read(self, buf: IBuffer, /) -> int:
#         return int.from_bytes(
#             buf.read(self.size),
#             byteorder=self.byteorder,
#             signed=self.signed,
#         )

#     def write(self, buf: OBuffer, obj: int, /) -> None:
#         buf.write(
#             obj.to_bytes(
#                 self.size,
#                 byteorder=self.byteorder,
#                 signed=self.signed,
#             )
#         )

#     def compile_read(self, c: DataClassCompiler) -> bool:
#         c.add_line(f'int.from_bytes(D[P:(P:=P+{self.size})],byteorder={self.byteorder!r},signed={self.signed})')
#         # c.add_line(f'int.from_bytes(B.read({self.size}),byteorder={self.byteorder!r},signed={self.signed})')
#         return True


class CustomCallable(SimpleDataclass, DataClass[T]):
    __slots__ = ('decode', 'encode')

    def __init__(
        self,
        *,
        decode: Callable[[IBuffer], T],
        encode: Callable[[OBuffer, T], Any],
    ) -> None:
        self.decode = decode
        self.encode = encode

    def read(self, buf: IBuffer, /) -> T:
        return self.decode(buf)

    def write(self, buf: OBuffer, obj: T, /) -> None:
        self.encode(buf, obj)

    def compile_read(self, c: DataClassCompiler) -> bool:
        var_decode = c.add_const('cc_decode', self.decode)
        with c.clean():
            c.add_result(f'{var_decode}(B)')
        return False


class StructFormat(SimpleDataclass, DataClass[T]):
    __slots__ = ('pack', 'unpack', 'size', 's')
    s: struct.Struct
    pack: Callable[[T], bytes]
    unpack: Callable[[bytes], tuple[T]]
    size: int

    def __init__(self, fmt: str) -> None:
        self.s = s = struct.Struct(fmt)
        self.pack = s.pack
        self.unpack = s.unpack  # type: ignore[assignment]
        self.size = s.size

    def read(self, buf: IBuffer, /) -> T:
        return self.unpack(buf.read(self.size))[0]

    def write(self, buf: OBuffer, obj: T, /) -> None:
        buf.write(self.pack(obj))

    def compile_read(self, c: DataClassCompiler) -> bool:
        s = self.s
        match s.format:
            case 'b':
                c.add_result('((_ := D[(P := P + 1) - 1]) - 256 * (_ > 127))')
                return True

            case 'B':
                c.add_result('D[(P := P + 1) - 1]')
                return True

            case '?':
                c.add_result('(D[(P := P + 1) - 1] is not 0)')
                return True

            case '<H' | '<I' | '<Q':
                c.add_global('int_from_bytes = int.from_bytes')
                c.add_result(f'int_from_bytes(D[P : (P := P + {s.size})], "little")')
                return True

            case '<h' | '<i' | '<q':
                c.add_global('int_from_bytes = int.from_bytes')
                c.add_result(f'int_from_bytes(D[P : (P := P + {s.size})], "little", signed=True)')
                return True

        sname = c.add_global_struct(self.s)
        c.add_result(f'{sname}.unpack(D[P : (P := P + {self.size})])[0]')
        return True


class SizedStr(SimpleDataclass, DataClass[str]):
    __slots__ = ('length',)
    length: int | None

    def __init__(self, length: int | None = None, /) -> None:
        self.length = length

    def read(self, buf: IBuffer, /) -> str:
        return buf.read_str(self.length)

    def write(self, buf: OBuffer, obj: str, /) -> None:
        buf.write_str(obj, self.length)

    def compile_read(self, c: DataClassCompiler) -> bool:
        with c.clean():
            c.add_result(f'B.read_str({self.length})')
        return False


class SizedWStr(SimpleDataclass, DataClass[str]):
    __slots__ = ('length',)
    length: int | None

    def __init__(self, length: int | None = None, /) -> None:
        self.length = length

    def read(self, buf: IBuffer, /) -> str:
        return buf.read_wstr(self.length)

    def write(self, buf: OBuffer, obj: str, /) -> None:
        buf.write_wstr(obj, self.length)

    def compile_read(self, c: DataClassCompiler) -> bool:
        if self.length is not None:
            c.add_result(f'D[P : (P := P + {self.length * 2})].decode("utf-16le")')
            return True

        c.add_line(f'_ = P')
        c.add_line(f'while D[P] or D[P + 1]: P += 2')
        c.add_result(f'D[_ : (P := P + 2) - 2].decode("utf-16le")')
        return True


DNone = NullDataClass()

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

Byte = UInt8
Bool = StructFormat[bool]('?')
Bool32 = UInt32  # FIXME

Str = SizedStr()
WStr = SizedWStr()


class Bytes(SimpleDataclass, DataClass[bytes]):
    __slots__ = ('size',)

    def __init__(self, size: int | None = None) -> None:
        self.size = size

    def read(self, buf: IBuffer, /) -> bytes:
        return buf.read(self.size)

    def write(self, buf: OBuffer, obj: bytes, /) -> None:
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

    def read(self, buf: IBuffer, /) -> T | None:
        if not self.base.read(buf):
            return None
        obj = self.dcls.read(buf)
        assert obj is not None
        return obj

    def write(self, buf: OBuffer, obj: T | None, /) -> None:
        if obj is None:
            self.base.write(buf, False)
        else:
            self.base.write(buf, True)
            self.dcls.write(buf, obj)

    def compile_read(self, c: DataClassCompiler) -> bool:
        c.compile_read(self.base)
        with c.block(f'if {c.get_result()}:'):
            c.compile_read(self.dcls)
        with c.block('else:'):
            c.add_result('None')
        return False

    def compile_traverse(self) -> Iterator[DataClass[Any]]:
        yield self
        yield self.dcls
        yield self.base


# compositions of dataclasses:


class AnyOf(DataClass[T]):
    __slots__ = ('dcls', 'values', 'msg')
    dcls: DataClass[T]
    values: Sequence_[T]
    msg: str | None

    def __init__(
        self,
        dcls: DataClass[T],
        values: Iterable[T],
        msg: str | None = None,
    ) -> None:
        self.dcls = dcls
        try:
            self.values = set(values)  # type: ignore[assignment]
        except TypeError:
            self.values = list(values)
        self.msg = msg

    def read(self, buf: IBuffer, /) -> T:
        obj = self.dcls.read(buf)
        if obj not in self.values:
            raise ValueError(
                f'Value {obj!r} should be in this set of values: {self.values!r}'
                + f'\n\t{self.msg}' * (self.msg is not None)
            )
        return obj

    def write(self, buf: OBuffer, obj: T, /) -> None:
        if obj not in self.values:
            raise ValueError(
                f'Value {obj!r} should be in this set of values: {self.values!r}'
                + f'\n\t{self.msg}' * (self.msg is not None)
            )
        self.dcls.write(buf, obj)

    def compile_read(self, c: DataClassCompiler) -> bool:
        c.compile_read(self.dcls)
        assert len(self.values)
        if len(self.values) == 1:
            var_value = c.add_const('anyof_value', next(iter(self.values)))

            with c.block(f'if R != {var_value}:'):
                c.add_line(f'raise ValueError(f"Value {{R}} should be equal to {{{var_value}}}")')
        else:
            var_values = c.add_const('anyof_values', self.values)

            with c.block(f'if R not in {var_values}:'):
                c.add_line(
                    f'raise ValueError(f"Value {{R}} should be in this set of values: {{{var_values}}}")'
                )
        return False


def Const(dcls: DataClass[T], value: T, msg: str | None = None) -> AnyOf[T]:
    return AnyOf(dcls, (value,), msg=msg)


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

    def read(self, buf: IBuffer, /) -> list[T]:
        length = self.sizedcls.read(buf)
        assert length >= 0, length
        result: list[T] = []
        for i in range(length):
            try:
                obj = self.dcls.read(buf)
            except Exception as exc:
                # print(buf.format_str(10, 10))
                print(f'Error in List dataclass. Partially readed data ({i}/{length} items):')
                # pprint(result, sort_dicts=False)
                print()
                raise DataClassError(
                    f'Error in reading {self.dcls.__class__} item at index {i+1}/{length}'
                ) from exc
            result.append(obj)
        return result

    def write(self, buf: OBuffer, obj: Sequence_[T], /) -> None:
        self.sizedcls.write(buf, len(obj))

        for i, item in enumerate(obj):
            try:
                self.dcls.write(buf, item)
            except Exception as exc:
                print(f'Error in List dataclass. Partially readed data ({i}/{len(obj)} items):')
                # pprint(result, sort_dicts=False)
                print()
                raise DataClassError(
                    f'Error in reading {self.dcls.__class__} item at index {i+1}/{len(obj)}'
                ) from exc

    def compile_read(self, c: DataClassCompiler) -> bool:
        with c.locals(1) as (var_res,):
            c.add_line(f'{var_res} = []')
            c.compile_read(self.sizedcls)
            with c.block(f'for _ in range({c.get_result()}):'):
                c.compile_read(self.dcls)
                c.add_line(f'{var_res}.append({c.get_result()})')
            c.add_result(var_res)
        return True


class Sequence(DataClass[tuple[Any, ...]]):
    __slots__ = ('dclss',)

    def __init__(self, *dclss: DataClass[Any]) -> None:
        self.dclss = dclss

    def read(self, buf: IBuffer, /) -> tuple[Any, ...]:
        result: list[Any] = []
        for i, dcls in enumerate(self.dclss):
            try:
                item = dcls.read(buf)
            except Exception as exc:
                raise DataClassError(
                    f'error in item of type {dcls.__class__} at index {i}/{len(self.dclss)}'
                ) from exc
            result.append(item)
        return tuple[Any, ...](result)

    def write(self, buf: OBuffer, obj: Sequence_[Any], /) -> None:
        assert len(self.dclss) == len(obj)
        for item, writer in zip(obj, self.dclss):
            writer.write(buf, item)

    def compile_read(self, c: DataClassCompiler) -> bool:
        if not self.dclss:
            c.add_result('()')
            return True
        with c.locals(1) as (var_res,):
            c.add_line(f'{var_res} = []')
            prev: DataClass[Any] = self.dclss[0]
            cnt = 1
            for dcls in [*self.dclss[1:], DataClass()]:
                if dcls is prev:
                    cnt += 1
                    continue

                if cnt == 1:
                    c.compile_read(prev)
                    c.add_line(f'{var_res}.append({c.get_result()})')
                else:
                    with c.block(f'for _ in {(0,)*cnt}:'):
                        c.compile_read(prev)
                        c.add_line(f'{var_res}.append({c.get_result()})')
                cnt = 1
                prev = dcls

            c.add_result(f'tuple({var_res})')
        return True


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
        base: DataClass[dict[Any, Any]] | None = None,
        /,
        **kwargs: DataClass[Any],
    ) -> None:
        self.base = base
        self.kwargs = kwargs

    def read(self, buf: IBuffer, /) -> dict[str, Any]:
        result: dict[str, Any] = self.base.read(buf) if self.base is not None else {}
        try:
            for name, dcls in self.kwargs.items():
                obj = dcls.read(buf)
                if not name.startswith('__'):
                    result[name] = obj
        except Exception as exc:
            raise DataClassError(f'Error in item {name} of type {dcls.__class__}') from exc
        return result

    def write(self, buf: OBuffer, obj: dict[str, Any], /) -> None:
        if self.base is not None:
            self.base.write(buf, obj)

        try:
            for name, dcls in self.kwargs.items():
                if name not in obj and name.startswith('__'):
                    dcls.write(buf, None)
                else:
                    dcls.write(buf, obj[name])
        except Exception as exc:
            raise DataClassError(f'Error in item {name} of type {dcls.__class__}') from exc

    def compile_read(self, c: DataClassCompiler) -> bool:
        with c.locals(1) as (var_res,):
            if self.base is None:
                c.add_line(f'{var_res} = {{}}')
            else:
                c.compile_read(c.compile(self.base))
                c.add_line(f'{var_res} = {c.get_result()}')

            for name, dcls in self.kwargs.items():
                if not name.startswith('__'):
                    c.compile_read(dcls)
                    c.add_line(f'{var_res}[{name!r}] = {c.get_result()}')
                else:
                    c.compile_read(dcls)
            c.add_result(var_res)
        return True


def Converted_(
    dcls: DataClass[T],
    *,
    decode: Callable[[T], G],
    encode: Callable[[G], T],
) -> CustomCallable[G]:
    return CustomCallable(
        decode=lambda buf, /: decode(dcls.read(buf)),
        encode=lambda buf, obj, /: dcls.write(buf, encode(obj)),
    )


class Converted(DataClass[T], Generic[T, G]):
    __slots__ = ('dcls', 'decode', 'encode')
    dcls: DataClass[G]
    decode: Callable[[G], T]
    encode: Callable[[T], G]

    def __init__(
        self,
        dcls: DataClass[G],
        *,
        decode: Callable[[G], T],
        encode: Callable[[T], G],
    ) -> None:
        self.dcls = dcls
        self.decode = decode
        self.encode = encode

    def read(self, buf: IBuffer, /) -> T:
        return self.decode(self.dcls.read(buf))

    def write(self, buf: OBuffer, obj: T, /) -> None:
        self.dcls.write(buf, self.encode(obj))

    def compile_read(self, c: DataClassCompiler) -> bool:
        c.compile_read(self.dcls)
        var_decode = c.add_const('conv_decode', self.decode)
        c.add_result(f'{var_decode}({c.get_result()})')
        return True


def HexBytes(dcls: DataClass[bytes], *, sep: str = ' ', bytes_per_sep: int = -4) -> DataClass[str]:
    return Converted(
        dcls,
        decode=lambda b, /: b.hex(sep=sep, bytes_per_sep=bytes_per_sep),
        encode=bytes.fromhex,
    )


class Nested(DataClass[T]):
    __slots__ = ('dcls1', 'dcls2')

    def __init__(self, dcls1: DataClass[bytes], dcls2: DataClass[T]) -> None:
        self.dcls1 = dcls1
        self.dcls2 = dcls2

    def read(self, buf: IBuffer, /) -> T:
        data = self.dcls1.read(buf)
        obj = self.dcls2.read(IBuffer(data))
        return obj

    def write(self, buf: OBuffer, obj: T, /) -> None:
        buf2 = OBuffer()
        self.dcls2.write(buf2, obj)
        data = bytes(buf2)
        self.dcls1.write(buf, data)

    def compile_read(self, c: DataClassCompiler) -> bool:
        with c.locals(1) as (var_buf,):
            c.add_ns('IBuffer', IBuffer)
            c.compile_read(self.dcls1)
            c.add_line(f'{var_buf} = B')
            c.add_line('B._pos = P')
            c.add_line(f'B = IBuffer(R)')
            c.add_line('P, D = B._pos, B.data')
            c.compile_read(self.dcls2)
            c.add_line(f'B = {var_buf}')
            c.add_line('P, D = B._pos, B.data')
        return False


class Pack(DataClass[list[T]]):
    __slots__ = ('dcls',)

    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, /) -> list[T]:
        result: list[T] = []
        while buf:
            result.append(self.dcls.read(buf))
        return result

    def write(self, buf: OBuffer, obj: list[T], /) -> None:
        for item in obj:
            self.dcls.write(buf, item)


class Selector(DataClass[tuple[G, T]]):
    __slots__ = ('base', 'dclss')
    max_cnt_to_unwind_options: ClassVar[int] = 6  # dont make it bigger

    def __init__(
        self: Selector[G, T],
        base: DataClass[G],
        dclss: dict[G | EllipsisType, DataClass[Any]],
    ) -> None:
        self.base = base
        self.dclss = dclss

    def read(self: Selector[G, T], buf: IBuffer, /) -> tuple[G, T]:
        n = self.base.read(buf)
        if n not in self.dclss:
            if ... not in self.dclss:
                raise ValueError(f'Selector value not in dict: value={n} keys={self.dclss.keys()}')
            return n, self.dclss[...].read(buf)
        return n, self.dclss[n].read(buf)

    def write(self: Selector[G, T], buf: OBuffer, obj: tuple[G, T] | list[Any], /) -> None:
        n = obj[0]
        self.base.write(buf, n)
        if n not in self.dclss:
            if ... not in self.dclss:
                raise ValueError(f'Selector value not in dict: value={n} keys={self.dclss.keys()}')
            self.dclss[...].write(buf, obj[1])
        else:
            self.dclss[n].write(buf, obj[1])

    def compile_read(self, c: DataClassCompiler) -> bool:
        if len(self.dclss) <= self.max_cnt_to_unwind_options:
            with c.locals(1) as (var_res,):
                c.compile_read(self.base)
                c.add_line(f'{var_res} = {c.get_result()}')
                for i, (key, key_dcls) in enumerate(self.dclss.items()):
                    if key == ...:
                        continue
                    if i == 0:
                        prefix = 'if'
                    else:
                        prefix = 'elif'
                    with c.block(f'{prefix} {var_res} == {c.add_const(f"sel_key_{i}", key)}:'):
                        c.compile_read(key_dcls)
                with c.block('else:'):
                    if ... in self.dclss:
                        c.compile_read(self.dclss[...])
                    else:
                        c.add_line('raise Exception(f"Selector value error", R)')
                c.add_result(f'({var_res}, R)')
                return True

        else:
            keys = self.dclss
            keys = {k: c.compile(v) for k, v in keys.items()}
            var_keys = c.add_const('selector_keys', keys)

            c.compile_read(self.base)
            with c.block(f'if R not in {var_keys}:'):
                if ... not in keys:
                    c.add_line(f'raise ValueError(R, {var_keys})')
                else:
                    with c.locals(1) as (var_temp_R,):
                        c.add_line(f'{var_temp_R} = R')
                        c.compile_read(keys[...])
                        c.add_result(f'{var_temp_R}, {c.get_result()}')
            with c.block('else:'), c.clean():
                c.add_result(f'R, {var_keys}[R].read(B)')
            return False


# class ReadOnlySelector(ReadOnlyDataClass[T], Generic[G, T]):
#     __slots__ = ('base', 'dclss')

#     def __init__(
#         self: ReadOnlySelector[G, T],
#         base: DataClass[G],
#         dclss: dict[G | EllipsisType, DataClass[T]],
#     ) -> None:
#         self.base = base
#         self.dclss = dclss

#     def read(self: ReadOnlySelector[G, T], buf: IBuffer, /) -> T:
#         n = self.base.read(buf)
#         if n not in self.dclss:
#             if ... not in self.dclss:
#                 raise ValueError(f'Selector value not in dict: value={n} keys={self.dclss.keys()}')
#             return self.dclss[...].read(buf)
#         return self.dclss[n].read(buf)


def MemoSelectedDataClass(selector: Callable[[Memo], DataClass[T]]) -> DataClass[T]:
    return CustomCallable(
        decode=lambda buf, /: selector(get_memo()).read(buf),
        encode=lambda buf, obj, /: selector(get_memo()).write(buf, obj),
    )


# SR-specific dataclasses:
class BufEC(DataClass[bytes]):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> bytes:
        size = buf.read_u32()
        data = buf.read(size)
        return data

    def write(self, buf: OBuffer, obj: bytes, /) -> None:
        buf.write_u32(len(obj))
        buf.write(obj)


class CryptedRand31pm(SimpleDataclass, DataClass[bytes]):
    __slots__ = ('key', 'seed', 'prepend_size')

    def __init__(self, key: int, seed: int | None = None, prepend_size: bool = False) -> None:
        self.key = key
        self.seed = random.randint(-0x80000000, 0x7FFFFFFF) if seed is None else seed
        self.prepend_size = prepend_size

    @staticmethod
    def get_rnd_bytes(state: int, size: int, /) -> bytearray:
        res = bytearray()
        for _ in itertools.repeat(None, size):
            state = (state % 0x1F31D) * 0x41A7 - (state // 0x1F31D) * 0xB14
            state += 0x7FFFFFFF * (state < 1)
            res.append((state - 1) % 256)
        return res

    @staticmethod
    def bytes_xor(d1: bytes, d2: bytes) -> bytes:
        n1 = int.from_bytes(d1, byteorder='big')
        n2 = int.from_bytes(d2, byteorder='big')
        return (n1 ^ n2).to_bytes(max(len(d1), len(d2)), byteorder='big')

    def read(self, buf: IBuffer, /) -> bytes:
        content_hash = buf.read_u32()
        seed = buf.read_i32() ^ self.key

        header = b''

        if self.prepend_size:
            size = buf.read_u32()
            b = OBuffer()
            b.write_u32(size)
            header = bytes(b)

        else:
            size = len(buf) - buf.pos

        data1 = buf.read(size)
        data2 = self.get_rnd_bytes(seed, size)

        data = self.bytes_xor(data1, data2)

        if (actual_hash := zlib.crc32(data)) != content_hash:
            raise ValueError(
                f'Content hash 0x{content_hash:x} dont match actual hash 0x{actual_hash:x}'
            )
        return header + data

    def write(self, buf: OBuffer, obj: bytes, /) -> None:
        data = obj
        if self.prepend_size:
            data = data[4:]
        size = len(data)

        buf.write_u32(zlib.crc32(data))
        buf.write_i32(self.seed ^ self.key)

        if self.prepend_size:
            buf.write(obj[:4])

        buf.write(self.bytes_xor(data, self.get_rnd_bytes(self.seed, size)))


class ZL(DataClass[bytes]):
    __slots__ = ('mode', 'length', 'optional')

    def __init__(self, mode: int, length: int | None = None, optional: bool = False) -> None:
        assert mode in {1, 2, 3}
        self.mode = mode
        self.length = length
        self.optional = optional

    def read(self, buf: IBuffer, /) -> bytes:
        if self.mode == 1:
            if self.length is None:
                size = buf.read_u32()
            else:
                size = self.length
                if size == -1:
                    size = len(buf) - buf.pos

            magic = buf.read(4)
            if self.optional and magic == b'\0\0\0\0':
                return b''

            assert magic == b'ZL01', magic
            # print(buf.format_str(20, 20))
            decompressed_size = buf.read_u32()
            compressed_data = buf.read(size - 8)
            data = zlib.decompress(compressed_data)
            assert len(data) == decompressed_size
            return data

        if self.mode == 2:
            raise NotImplementedError

        if self.mode == 3:
            raise NotImplementedError

        raise ValueError(f'Unknown ZL mode: {self.mode}')

    def write(self, buf: OBuffer, obj: bytes, /) -> None:
        if self.mode == 1:
            if self.length is not None:
                if self.length != -1:
                    buf.write_u32(self.length)

            if self.optional and not obj:
                buf.write(b'\0\0\0\0')
                return

            compressed = zlib.compress(obj, level=9)
            if self.length is None:
                buf.write_u32(len(compressed) + 8)

            buf.write(b'ZL01')
            buf.write_u32(len(obj))
            buf.write(compressed)
            return

        if self.mode == 2:
            raise NotImplementedError

        if self.mode == 3:
            raise NotImplementedError

        raise ValueError(f'Unknown ZL mode: {self.mode}')


class CRC(DataClass[bytes]):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> bytes:
        crc = buf.read_u32()
        data = buf.read()
        if crc != zlib.crc32(data):
            raise ValueError('Content hash dont match actual hash')
        return data

    def write(self, buf: OBuffer, obj: bytes, /) -> None:
        buf.write_u32(zlib.crc32(obj))
        buf.write(obj)


# dataclasses for consistency testing
class AssertOnEnd(NullDataClass):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> None:
        if not buf.pos == len(buf):
            raise DataClassError(f'{buf.pos = }, {len(buf) = }')

    def write(self, buf: OBuffer, obj: Any, /) -> None:
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

    def read(self, buf: IBuffer, /) -> None:
        self.cnt -= 1
        if self.cnt == 0:
            raise self.exc

    def write(self, buf: OBuffer, obj: Any, /) -> None:
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

    def read(self, buf: IBuffer, /) -> T:
        obj = self.dcls.read(buf)
        get_memo()[self.name] = obj
        return obj

    def write(self, buf: OBuffer, obj: T, /) -> None:
        get_memo()[self.name] = obj
        self.dcls.write(buf, obj)


class GetFromMemo(DataClass[T]):
    __slots__ = ('name', 'default')
    missing: ClassVar[object] = object()

    def __init__(self, name: Hashable, default: T = missing) -> None:  # type: ignore[assignment]
        self.name = name
        self.default = default

    def read(self, buf: IBuffer, /) -> T:
        if self.default is self.missing:
            return get_memo()[self.name]
        else:
            return get_memo().get(self.name, self.default)

    def write(self, buf: OBuffer, obj: T, /) -> None:
        pass


# dataclasses for debugging:
class _Skip(NullDataClass):
    def __init__(self, n: int) -> None:
        self.n = n

    def read(self, buf: IBuffer, /) -> None:
        buf.pos += self.n

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        assert obj is None
        buf.pos += self.n


class _Log(NullDataClass):
    def __init__(self, msg: str = '<log>', before: int | None = 20, after: int | None = 20) -> None:
        self.msg = msg
        self.before = before
        self.after = after

    def read(self, buf: IBuffer, /) -> None:
        print(self.msg)
        print(buf.format_str(self.before, self.after))
        print()

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        assert obj is None
        print(self.msg)
        print(buf.format_str(self.before, self.after))
        print()


class _DumpTo(NullDataClass):
    def __init__(self, filename: Path, mode: Literal['t', 'b'] = 't') -> None:
        self.filename = filename
        self.mode = mode

    def read(self, buf: IBuffer, /) -> None:
        buf.dump_to_file(self.filename, self.mode)

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        buf.dump_to_file(self.filename, self.mode)


class _PrintMsg(NullDataClass):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def read(self, buf: IBuffer, /) -> None:
        print(self.msg)

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        assert obj is None
        print(self.msg)


class _PrintMemo(NullDataClass):
    def read(self, buf: IBuffer, /) -> None:
        pprint(get_memo(), sort_dicts=False)

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        pprint(get_memo(), sort_dicts=False)


class _Print(DataClass[T]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, /) -> T:
        obj = self.dcls.read(buf)
        pprint(obj, sort_dicts=False)
        return obj

    def write(self, buf: OBuffer, obj: T, /) -> None:
        pprint(obj, sort_dicts=False)
        self.dcls.write(buf, obj)


class _Hide(ReadOnlyDataClass[str]):
    def __init__(self, dcls: DataClass[Any]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, /) -> str:
        res = self.dcls.read(buf)
        if isinstance(res, Sized):
            return f'<hidden {res.__class__.__name__}[{len(res)}]>'
        return f'<hidden {res.__class__.__name__}>'


class _LogOnException(DataClass[T]):
    def __init__(self, dcls: DataClass[T]) -> None:
        self.dcls = dcls

    def read(self, buf: IBuffer, /) -> T:
        try:
            return self.dcls.read(buf)
        except Exception:
            print(f'Exception in dataclass {self.dcls.__class__.__name__} occured. Buffer:')
            print(buf.format_str(50, 50))
            raise

    def write(self, buf: OBuffer, obj: T, /) -> None:
        try:
            self.dcls.write(buf, obj)
        except Exception:
            print(f'Exception in dataclass {self.dcls.__class__.__name__} occured. Buffer:')
            print(buf.format_str(50, 50))
            raise


class _Wait(NullDataClass):
    def __init__(self, msg: str = '') -> None:
        self.msg = msg

    def read(self, buf: IBuffer, /) -> None:
        input(f'Wait: {self.msg}')

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        input(f'Wait: {self.msg}')


class _Breakpoint(NullDataClass):
    def read(self, buf: IBuffer, /) -> None:
        breakpoint()

    def write(self, buf: OBuffer, obj: Any, /) -> None:
        breakpoint()
