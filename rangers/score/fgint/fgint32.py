"""!
@file
"""
from __future__ import annotations

import os
import ctypes
from ctypes import (
    Structure as struct,
    c_bool,
    c_char,
    c_wchar,
    c_byte,
    c_ubyte,
    c_short,
    c_ushort,
    c_int,
    c_uint,
    c_long,
    c_ulong,
    c_longlong,
    c_ulonglong,
    c_size_t,
    c_ssize_t,
    c_float,
    c_double,
    c_longdouble,
    c_char_p,
    c_wchar_p,
    c_void_p,
    pointer,
    POINTER,
    byref,
    cast,
)

from msl.loadlib import Server32  # type: ignore[import]

libname = R'FGIntWrapper.dll'

class PascalString(struct):
    _fields_ = [
        ('len', c_ubyte),
        ('val', c_ubyte * 25),
    ]

class FGInt32(Server32):

    def __init__(self, host, port, **kwargs):
        super().__init__(os.path.join(os.path.dirname(__file__), libname), 'cdll', host, port)

    def add(self, a, b):
        return self.lib.AddIntegers(a, b)

    def ConvertBase64to256(self, data: bytes) -> bytes:
        f = self.lib._ConvertBase64to256
        f.argtypes = [POINTER(PascalString)]
        f.restype = c_int
        ps = PascalString()


        f(pointer(ps))
        ps = cast(ps, c_void_p).contents

        return f'{ps} {ps.len} {bytes(ps.val)}'
        return bytes(ps.val)
