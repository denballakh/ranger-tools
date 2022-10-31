from collections.abc import Iterable
from typing import Any
import unittest
import math

from rangers.std.buffer import Buffer, IBuffer, OBuffer, BaseBuffer
from rangers.std._buffer import Buffer as _Buffer, IBuffer as _IBuffer, OBuffer as _OBuffer

READ_WRITE_TEST_DATA: list[tuple[str, Any, bytes]] = [
    ('byte', 0, b'\0'),
    ('byte', 1, b'\1'),
    ('byte', 2**8 - 1, b'\xff'),
    #
    ('bool', False, b'\0'),
    ('bool', True, b'\1'),
    #
    ('char', 0, b'\0'),
    ('char', 1, b'\1'),
    ('char', -1, b'\xff'),
    #
    ('uchar', 0, b'\0'),
    ('uchar', 1, b'\1'),
    ('uchar', 2**8 - 1, b'\xff'),
    #
    ('short', 0, b'\0\0'),
    ('short', 1, b'\1\0'),
    ('short', -1, b'\xff\xff'),
    #
    ('ushort', 0, b'\0\0'),
    ('ushort', 1, b'\1\0'),
    ('ushort', 2**16 - 1, b'\xff\xff'),
    #
    ('int', 0, b'\0\0\0\0'),
    ('int', 1, b'\1\0\0\0'),
    ('int', 2, b'\2\0\0\0'),
    ('int', -1, b'\xff\xff\xff\xff'),
    #
    ('uint', 0, b'\0\0\0\0'),
    ('uint', 1, b'\1\0\0\0'),
    ('uint', 2**32 - 1, b'\xff\xff\xff\xff'),
    #
    ('long', 0, b'\0\0\0\0\0\0\0\0'),
    ('long', 1, b'\1\0\0\0\0\0\0\0'),
    ('long', -1, b'\xff\xff\xff\xff\xff\xff\xff\xff'),
    #
    ('ulong', 0, b'\0\0\0\0\0\0\0\0'),
    ('ulong', 1, b'\1\0\0\0\0\0\0\0'),
    ('ulong', 2**64 - 1, b'\xff\xff\xff\xff\xff\xff\xff\xff'),
    #
    ('float', 0.0, b'\0\0\0\0'),
    ('float', 1.0, b'\0\0\x80?'),
    ('float', -1.0, b'\0\0\x80\xbf'),
    ('float', math.pi, b'\xdb\x0fI@'),
    ('float', float('inf'), b'\0\0\x80\x7f'),
    ('float', float('-inf'), b'\0\0\x80\xff'),
    ('float', float('nan'), b'\0\0\xc0\x7f'),
    #
    ('double', 0.0, b'\0\0\0\0\0\0\0\0'),
    ('double', 1.0, b'\0\0\0\0\0\0\xf0?'),
    ('double', -1.0, b'\0\0\0\0\0\0\xf0\xbf'),
    ('double', math.pi, b'\x18-DT\xfb!\t@'),
    ('double', float('inf'), b'\0\0\0\0\0\0\xf0\x7f'),
    ('double', float('-inf'), b'\0\0\0\0\0\0\xf0\xff'),
    ('double', float('nan'), b'\0\0\0\0\0\0\xf8\x7f'),
    #
    ('str', '', b'\0'),
    ('str', 'hello world', b'hello world\0'),
    (
        'str',
        'русский текст',
        b'\xd1\x80\xd1\x83\xd1\x81\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9 \xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82\0',
    ),
    #
    ('wstr', '', b'\0\0'),
    ('wstr', 'hello world', b'h\0e\0l\0l\0o\0 \0w\0o\0r\0l\0d\0\0\0'),
    (
        'wstr',
        'русский текст',
        b'@\x04C\x04A\x04A\x04:\x048\x049\x04 \0B\x045\x04:\x04A\x04B\x04\0\0',
    ),
]

# TODO:
# .pos = ...
# .push_pos, .push_pos
# __iter__, __len__, __bytes__
# __str__, __repr__
# __bool__
# .from_file, .dump_to_file
# .read, .read_format, .read_struct
# .write, .write_format, .write_struct
# .read_str(length=...), .read_wstr(length=...)
# .write_str(length=...), .write_wstr(length=...)

class TestBuffer(unittest.TestCase):
    def test_construction(self) -> None:
        for cls in (Buffer, IBuffer, OBuffer):
            self.assertRaises(TypeError, cls, None)
            self.assertRaises(TypeError, cls, 0)
            self.assertRaises(TypeError, cls, [])
            self.assertRaises(TypeError, cls, '')

            for data in [b'', b'123', bytes(100), bytearray(), bytearray(b'123')]:
                with self.subTest(data=data):
                    buf = Buffer(data)
                    self.assertEqual(buf.data, data)
                    self.assertEqual(bytes(buf), data)
                    self.assertEqual(bytearray(buf), data)

    def test_iter(self) -> None:
        self.assertEqual(list(Buffer()), [])
        self.assertEqual(list(Buffer(b'abc')), list(b'abc'))

    def test_bool(self) -> None:
        self.assertFalse(Buffer())
        buf = Buffer(b'abc')
        self.assertTrue(buf)
        buf.pos = 3
        self.assertFalse(buf)

    def test_len(self) -> None:
        self.assertEqual(len(Buffer()), 0)
        self.assertEqual(len(Buffer(b'abc')), 3)
        b = Buffer(b'abc')
        b.pos = 3
        self.assertEqual(len(b), 3)

    def test_to_bytes(self) -> None:
        data = b'abc'
        b = Buffer(data)
        self.assertEqual(bytes(b), data)
        self.assertEqual(b.data, data)

        self.assertEqual(bytes(Buffer()), b'')

    def _assertEqualEx(self, obj1: object, obj2: object) -> None:
        if isinstance(obj1, float):
            self.assertIsInstance(obj2, float)
            assert isinstance(obj2, float)
            if math.isnan(obj1):
                self.assertTrue(math.isnan(obj2), f'{obj2} is not nan')
            elif math.isinf(obj1):
                self.assertEqual(obj2, obj1)
            else:
                self.assertTrue(abs(obj2 - obj1) < 1e-7, f'{obj2} != {obj1}')
        else:
            self.assertEqual(obj2, obj1)
        self.assertIs(type(obj2), type(obj1), (obj1, obj2))

    def test_read(self) -> None:
        clss: Iterable[type[IBuffer]] = [
            IBuffer,
            Buffer,
            # FastBuffer,  # type: ignore[list-item]
            _IBuffer,
            _Buffer,
        ]
        for cls in clss:
            for method_name, value, data in READ_WRITE_TEST_DATA:
                print(cls, method_name)
                with self.subTest(
                    msg='test_1',
                    cls=cls,
                    method_name=method_name,
                    expected_value=value,
                    data=data,
                ):
                    buf = cls(data)
                    meth = getattr(buf, f'read_{method_name}')
                    actual_value = meth()
                    self._assertEqualEx(value, actual_value)
                    self.assertEqual(buf.pos, len(data))

                with self.subTest(
                    msg='test_2',
                    cls=cls,
                    method_name=method_name,
                    expected_value=value,
                    data=data,
                ):
                    n = 10
                    buf = cls(b'\0' * n + data + b'\0' * n)
                    buf.read(n)
                    meth = getattr(buf, f'read_{method_name}')
                    actual_value = meth()
                    buf.read(n)
                    self._assertEqualEx(value, actual_value)
                    self.assertEqual(buf.pos, len(data) + 2 * n)

                # if method_name not in {'str', 'wstr'} and cls not in {FastBuffer}:  # type: ignore[comparison-overlap]
                #     with self.subTest(
                #         msg='test_3',
                #         cls=cls,
                #         method_name=method_name,
                #         expected_value=value,
                #         data=data,
                #     ):
                #         n = 10
                #         buf = cls(b'\0' * n + data + b'\0' * n)
                #         meth = getattr(buf, f'read_{method_name}')
                #         actual_value = meth(n)
                #         self._assertEqualEx(value, actual_value)
                #         self.assertEqual(buf.pos, 0)


    def test_write(self) -> None:
        clss: Iterable[type[OBuffer]] = [
            OBuffer,
            Buffer,
            # FastBuffer,  # type: ignore[list-item]
            _OBuffer,
            _Buffer,
        ]
        for cls in clss:
            for method_name, value, data in READ_WRITE_TEST_DATA:
                with self.subTest(
                    msg='test_1',
                    cls=cls,
                    method_name=method_name,
                    value=value,
                    expected_data=data,
                ):
                    buf = cls()
                    meth = getattr(buf, f'write_{method_name}')
                    actual_value = meth(value)
                    if cls not in {'FastBuffer'}:  # type: ignore[comparison-overlap]
                        self.assertEqual(buf.pos, len(data))
                    self.assertEqual(bytes(buf), data)

                # with self.subTest(
                #     msg='test_2',
                #     cls=cls,
                #     method_name=method_name,
                #     value=value,
                #     expected_data=data,
                # ):
                #     if method_name not in {'str', 'wstr'} and cls not in {FastBuffer}:  # type: ignore[comparison-overlap]
                #         n = 10
                #         buf = cls(n*b'\0')
                #         buf.pos = n // 2
                #         meth = getattr(buf, f'write_{method_name}')
                #         actual_value = meth(value)
                #         self.assertEqual(buf.pos, n // 2)
                #         self.assertEqual(bytes(buf), n*b'\0' + data)
                #         # print(type(buf))


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as exc:
        if exc.code == 0:
            import os
            # input()
            os._exit(0)
