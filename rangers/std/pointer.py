from __future__ import annotations
import builtins
from typing import Any, ClassVar, Final, Protocol, overload
import struct
import ctypes

__all__ = ('pointer',)

PTR_SIZE: Final[int] = struct.calcsize('@P')


class SupportsInt(Protocol):
    def __int__(self) -> int:
        ...


class pointer:
    __slots__ = ('addr',)
    __match_args__ = ('addr',)

    addr: int
    __arrays: ClassVar[dict[int, type[ctypes.Array[ctypes.c_ubyte]]]] = {}

    @classmethod
    def ptr_size(cls) -> int:
        return PTR_SIZE

    def __init__(self, addr: SupportsInt, /) -> None:
        # if isinstance(addr, pointer):
        #     addr = addr.addr
        addr = int(addr)

        if addr < 0:
            raise ValueError('negative pointer', addr)

        if addr.bit_length() > PTR_SIZE * 8:
            raise ValueError('too big pointer', addr)

        self.addr = addr

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__!s}({self.addr:#0{2*PTR_SIZE+2}x})'

    def __str__(self, /) -> str:
        return f'<pointer to {self.addr:#0{2*PTR_SIZE+2}x}>'

    def __int__(self, /) -> int:
        return self.addr

    # def __index__(self, /) -> int:
    #     return self.addr

    def __bool__(self, /) -> bool:
        return bool(self.addr)

    def __copy__(self, /) -> pointer:
        # return self.__class__(self.addr)
        return self

    def __hash__(self, /) -> int:
        return self.addr

    def __eq__(self, obj: pointer | int | object, /) -> bool:
        if isinstance(obj, int):
            return self.addr == obj
        if isinstance(obj, pointer):
            return self.addr == obj.addr
        return NotImplemented

    def __ne__(self, obj: pointer | int | object, /) -> bool:
        if isinstance(obj, int):
            return self.addr != obj
        if isinstance(obj, pointer):
            return self.addr != obj.addr
        return NotImplemented

    def __gt__(self, obj: pointer | int | object, /) -> bool:
        if isinstance(obj, int):
            return self.addr > obj
        if isinstance(obj, pointer):
            return self.addr > obj.addr
        return NotImplemented

    def __ge__(self, obj: pointer | int | object, /) -> bool:
        if isinstance(obj, int):
            return self.addr >= obj
        if isinstance(obj, pointer):
            return self.addr >= obj.addr
        return NotImplemented

    def __lt__(self, obj: pointer | int | object, /) -> bool:
        if isinstance(obj, int):
            return self.addr < obj
        if isinstance(obj, pointer):
            return self.addr < obj.addr
        return NotImplemented

    def __le__(self, obj: pointer | int | object, /) -> bool:
        if isinstance(obj, int):
            return self.addr <= obj
        if isinstance(obj, pointer):
            return self.addr <= obj.addr
        return NotImplemented

    def __add__(self, value: int | pointer, /) -> pointer:
        return self.__class__(self.addr + int(value))

    def __radd__(self, value: int | pointer, /) -> pointer:
        return self.__class__(self.addr + int(value))

    @overload
    def __sub__(self, value: int, /) -> pointer:
        ...

    @overload
    def __sub__(self, value: pointer, /) -> int:
        ...

    def __sub__(self, value: int | pointer, /) -> int | pointer:
        if isinstance(value, int):
            return self.__class__(self.addr - value)
        else:
            return self.addr - value.addr

    @classmethod
    def __get_array(cls, size: int, /) -> type[ctypes.Array[ctypes.c_ubyte]]:
        if size not in cls.__arrays:
            cls.__arrays[size] = ctypes.c_ubyte * size
        return cls.__arrays[size]

    def read(self, size: int, /) -> bytes:
        return bytes(self.__get_array(size).from_address(self.addr))

    def write(self, data: bytes, /) -> None:
        self.__get_array(len(data)).from_address(self.addr)[:] = data  # type: ignore[call-overload]

    def read_struct(self, s: struct.Struct, /) -> tuple[Any, ...]:
        return s.unpack(self.read(s.size))

    def write_struct(self, s: struct.Struct, *values: Any) -> None:
        return self.write(s.pack(*values))

    def read_format(self, fmt: str, /) -> tuple[Any, ...]:
        return self.read_struct(struct.Struct(fmt))

    def write_format(self, fmt: str, *values: Any) -> None:
        return self.write_struct(struct.Struct(fmt), *values)

    @property
    def byte(self, /) -> int:
        return self.read(1)[0]

    @byte.setter
    def byte(self, value: int, /) -> None:
        return self.write(bytes((value,)))

    @property
    def bool(self, *, __s: struct.Struct = struct.Struct('?')) -> builtins.bool:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @bool.setter
    def bool(self, value: builtins.bool, *, __s: struct.Struct = struct.Struct('?')) -> None:
        self.write_struct(__s, value)

    @property
    def int8(self, *, __s: struct.Struct = struct.Struct('b')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @int8.setter
    def int8(self, value: int, *, __s: struct.Struct = struct.Struct('b')) -> None:
        self.write_struct(__s, value)

    @property
    def uint8(self, *, __s: struct.Struct = struct.Struct('B')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @uint8.setter
    def uint8(self, value: int, *, __s: struct.Struct = struct.Struct('B')) -> None:
        self.write_struct(__s, value)

    @property
    def int16(self, *, __s: struct.Struct = struct.Struct('@h')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @int16.setter
    def int16(self, value: int, *, __s: struct.Struct = struct.Struct('@h')) -> None:
        self.write_struct(__s, value)

    @property
    def uint16(self, *, __s: struct.Struct = struct.Struct('@H')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @uint16.setter
    def uint16(self, value: int, *, __s: struct.Struct = struct.Struct('@H')) -> None:
        self.write_struct(__s, value)

    @property
    def int32(self, *, __s: struct.Struct = struct.Struct('@i')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @int32.setter
    def int32(self, value: int, *, __s: struct.Struct = struct.Struct('@i')) -> None:
        self.write_struct(__s, value)

    @property
    def uint32(self, *, __s: struct.Struct = struct.Struct('@I')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @uint32.setter
    def uint32(self, value: int, *, __s: struct.Struct = struct.Struct('@I')) -> None:
        self.write_struct(__s, value)

    @property
    def int64(self, *, __s: struct.Struct = struct.Struct('@q')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @int64.setter
    def int64(self, value: int, *, __s: struct.Struct = struct.Struct('@q')) -> None:
        self.write_struct(__s, value)

    @property
    def uint64(self, *, __s: struct.Struct = struct.Struct('@Q')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @uint64.setter
    def uint64(self, value: int, *, __s: struct.Struct = struct.Struct('@Q')) -> None:
        self.write_struct(__s, value)

    @property
    def float(self, *, __s: struct.Struct = struct.Struct('@f')) -> builtins.float:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @float.setter
    def float(self, value: builtins.float, *, __s: struct.Struct = struct.Struct('@f')) -> None:
        self.write_struct(__s, value)

    @property
    def double(self, *, __s: struct.Struct = struct.Struct('@d')) -> builtins.float:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @double.setter
    def double(self, value: builtins.float, *, __s: struct.Struct = struct.Struct('@d')) -> None:
        self.write_struct(__s, value)

    @property
    def size_t(self, *, __s: struct.Struct = struct.Struct('@N')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @size_t.setter
    def size_t(self, value: int, *, __s: struct.Struct = struct.Struct('@N')) -> None:
        self.write_struct(__s, value)

    @property
    def ssize_t(self, *, __s: struct.Struct = struct.Struct('@n')) -> int:  # type: ignore[misc]
        return self.read_struct(__s)[0]

    @ssize_t.setter
    def ssize_t(self, value: int, *, __s: struct.Struct = struct.Struct('@n')) -> None:
        self.write_struct(__s, value)

    @property
    def ptr(self, *, __s: struct.Struct = struct.Struct('@P')) -> pointer:  # type: ignore[misc]
        return pointer(self.read_struct(__s)[0])

    @ptr.setter
    def ptr(self, value: pointer, *, __s: struct.Struct = struct.Struct('@P')) -> None:
        self.write_struct(__s, int(value))

    @property
    def cstr(self, /) -> str:
        ptr = self
        res = bytearray()
        while t := ptr.byte:
            res.append(t)
            ptr += 1
        return res.decode('utf-8')

    @cstr.setter
    def cstr(self, value: str, /) -> None:
        raise NotImplementedError

    @property
    def cwstr(self, /) -> str:
        ptr = self
        res = bytearray()
        while t := ptr.uint16:
            res.extend(ptr.read(2))
            ptr += 2
        return res.decode('utf-16le')

    @cwstr.setter
    def cwstr(self, value: str, /) -> None:
        raise NotImplementedError

    @property
    def pstr(self, /) -> str:
        ptr = self
        size = ptr.uint8
        ptr += 1
        data = ptr.read(size)
        return data.decode('utf-8')

    @pstr.setter
    def pstr(self, value: str, /) -> None:
        raise NotImplementedError

    @property
    def pwstr(self, /) -> str:
        ptr = self
        size = ptr.uint16
        ptr += 2
        data = ptr.read(size * 2)
        return data.decode('utf-16le')

    @pwstr.setter
    def pwstr(self, value: str, /) -> None:
        raise NotImplementedError

