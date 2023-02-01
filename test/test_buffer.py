from collections.abc import Iterable
from typing import Any
import unittest
import math

from rangers.std.buffer import Buffer, IBuffer, OBuffer, BaseBuffer

READ_WRITE_TEST_DATA: list[tuple[str, Any, bytes]] = [
    ('byte', 0, b'\0'),
    ('byte', 1, b'\1'),
    ('byte', 2**8 - 1, b'\xff'),
    #
    ('bool', False, b'\0'),
    ('bool', True, b'\1'),
    #
    ('i8', 0, b'\0'),
    ('i8', 1, b'\1'),
    ('i8', -1, b'\xff'),
    #
    ('u8', 0, b'\0'),
    ('u8', 1, b'\1'),
    ('u8', 2**8 - 1, b'\xff'),
    #
    ('i16', 0, b'\0\0'),
    ('i16', 1, b'\1\0'),
    ('i16', -1, b'\xff\xff'),
    #
    ('u16', 0, b'\0\0'),
    ('u16', 1, b'\1\0'),
    ('u16', 2**16 - 1, b'\xff\xff'),
    #
    ('i32', 0, b'\0\0\0\0'),
    ('i32', 1, b'\1\0\0\0'),
    ('i32', 2, b'\2\0\0\0'),
    ('i32', -1, b'\xff\xff\xff\xff'),
    #
    ('u32', 0, b'\0\0\0\0'),
    ('u32', 1, b'\1\0\0\0'),
    ('u32', 2**32 - 1, b'\xff\xff\xff\xff'),
    #
    ('i64', 0, b'\0\0\0\0\0\0\0\0'),
    ('i64', 1, b'\1\0\0\0\0\0\0\0'),
    ('i64', -1, b'\xff\xff\xff\xff\xff\xff\xff\xff'),
    #
    ('u64', 0, b'\0\0\0\0\0\0\0\0'),
    ('u64', 1, b'\1\0\0\0\0\0\0\0'),
    ('u64', 2**64 - 1, b'\xff\xff\xff\xff\xff\xff\xff\xff'),
    #
    ('f32', 0.0, b'\0\0\0\0'),
    ('f32', 1.0, b'\0\0\x80?'),
    ('f32', -1.0, b'\0\0\x80\xbf'),
    ('f32', math.pi, b'\xdb\x0fI@'),
    ('f32', float('inf'), b'\0\0\x80\x7f'),
    ('f32', float('-inf'), b'\0\0\x80\xff'),
    ('f32', float('nan'), b'\0\0\xc0\x7f'),
    #
    ('f64', 0.0, b'\0\0\0\0\0\0\0\0'),
    ('f64', 1.0, b'\0\0\0\0\0\0\xf0?'),
    ('f64', -1.0, b'\0\0\0\0\0\0\xf0\xbf'),
    ('f64', math.pi, b'\x18-DT\xfb!\t@'),
    ('f64', float('inf'), b'\0\0\0\0\0\0\xf0\x7f'),
    ('f64', float('-inf'), b'\0\0\0\0\0\0\xf0\xff'),
    ('f64', float('nan'), b'\0\0\0\0\0\0\xf8\x7f'),
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

                # if method_name not in {'str', 'wstr'}:
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
                    self.assertEqual(buf.pos, len(data))
                    self.assertEqual(bytes(buf), data)

                # with self.subTest(
                #     msg='test_2',
                #     cls=cls,
                #     method_name=method_name,
                #     value=value,
                #     expected_data=data,
                # ):
                #     if method_name not in {'str', 'wstr'}:
                #         n = 10
                #         buf = cls(n*b'\0')
                #         buf.pos = n // 2
                #         meth = getattr(buf, f'write_{method_name}')
                #         actual_value = meth(value)
                #         self.assertEqual(buf.pos, n // 2)
                #         self.assertEqual(bytes(buf), n*b'\0' + data)
                #         # print(type(buf))


def test_speed() -> None:
    import gc
    from rangers.std.time import AdaptiveTimeMeasurer

    gc.enable()
    gc.collect()
    gc.disable()

    with AdaptiveTimeMeasurer(
        target_time=0.1,
        config_file='_buffer_bench.json',
    ) as atm:
        print()
        print()

        T = atm('empty loop', extra=2)
        T.calibrate(0)
        with T as _:
            for _ in _:
                pass
        assert T.time is not None
        T.calibrate(T.time)

        with atm('calibrated empty loop') as _:
            for _ in _:
                pass

        ba = bytearray(b'0123' * 10**8)
        bahw1 = bytearray(b'hello world\0' * 10**8)
        bahw2 = bytearray(b'hello world\0\0' * 10**8)
        bazeros = bytearray(b'\0' * 10**8)
        new_buf = lambda: cls(ba)

        gc.collect()

        cls: type[Buffer]
        for cls in (Buffer,):
            clsname = cls.__name__
            print()

            with atm(f'{clsname}()') as _:
                for _ in _:
                    cls()

            buf = cls()
            with atm(f'{clsname}.write(b"")') as _:
                for _ in _:
                    buf.write(b"")

            buf = cls()
            with atm(f'{clsname}.write([])') as _:
                for _ in _:
                    buf.write([])

            buf = cls()
            with atm(f'{clsname}.write_byte(7)') as _:
                for _ in _:
                    buf.write_byte(7)

            buf = cls()
            with atm(f'{clsname}.write_bool(True)') as _:
                for _ in _:
                    buf.write_bool(True)

            buf = cls()
            with atm(f'{clsname}.write_i8(-123)') as _:
                for _ in _:
                    buf.write_i8(-123)

            buf = cls()
            with atm(f'{clsname}.write_u8(123)') as _:
                for _ in _:
                    buf.write_u8(123)

            buf = cls()
            with atm(f'{clsname}.write_i16(-1234)') as _:
                for _ in _:
                    buf.write_i16(-1234)

            buf = cls()
            with atm(f'{clsname}.write_u16(1234)') as _:
                for _ in _:
                    buf.write_u16(1234)

            buf = cls()
            with atm(f'{clsname}.write_i32(-123456789)') as _:
                for _ in _:
                    buf.write_i32(-123456789)

            buf = cls()
            with atm(f'{clsname}.write_u32(123456789)') as _:
                for _ in _:
                    buf.write_u32(123456789)

            buf = cls()
            with atm(f'{clsname}.write_i64(-123456789)') as _:
                for _ in _:
                    buf.write_i64(-123456789)

            buf = cls()
            with atm(f'{clsname}.write_u64(123456789)') as _:
                for _ in _:
                    buf.write_u64(123456789)

            buf = cls()
            with atm(f'{clsname}.write_f32(1.23)') as _:
                for _ in _:
                    buf.write_f32(1.23)

            buf = cls()
            with atm(f'{clsname}.write_f64(1.23)') as _:
                for _ in _:
                    buf.write_f64(1.23)

            buf = cls()
            with atm(f'{clsname}.write_str("hello world")') as _:
                for _ in _:
                    buf.write_str("hello world")

            buf = cls()
            with atm(f'{clsname}.write_wstr("hello world")') as _:
                for _ in _:
                    buf.write_wstr("hello world")

            buf = cls()
            with atm(f'{clsname}.write_str("")') as _:
                for _ in _:
                    buf.write_str("")

            buf = cls()
            with atm(f'{clsname}.write_wstr("")') as _:
                for _ in _:
                    buf.write_wstr("")

            buf = new_buf()
            with atm(f'{clsname}.read(0)') as _:
                for _ in _:
                    buf.read(0)

            buf = new_buf()
            with atm(f'{clsname}.read(3)') as _:
                for _ in _:
                    buf.read(3)

            buf = new_buf()
            with atm(f'{clsname}.read_byte()') as _:
                for _ in _:
                    buf.read_byte()

            buf = new_buf()
            with atm(f'{clsname}.read_bool()') as _:
                for _ in _:
                    buf.read_bool()

            buf = new_buf()
            with atm(f'{clsname}.read_i8()') as _:
                for _ in _:
                    buf.read_i8()

            buf = new_buf()
            with atm(f'{clsname}.read_u8()') as _:
                for _ in _:
                    buf.read_u8()

            buf = new_buf()
            with atm(f'{clsname}.read_i16()') as _:
                for _ in _:
                    buf.read_i16()

            buf = new_buf()
            with atm(f'{clsname}.read_u16()') as _:
                for _ in _:
                    buf.read_u16()

            buf = new_buf()
            with atm(f'{clsname}.read_i32()') as _:
                for _ in _:
                    buf.read_i32()

            buf = new_buf()
            with atm(f'{clsname}.read_u32()') as _:
                for _ in _:
                    buf.read_u32()

            buf = new_buf()
            with atm(f'{clsname}.read_i64()') as _:
                for _ in _:
                    buf.read_i64()

            buf = new_buf()
            with atm(f'{clsname}.read_u64()') as _:
                for _ in _:
                    buf.read_u64()

            buf = new_buf()
            with atm(f'{clsname}.read_f32()') as _:
                for _ in _:
                    buf.read_f32()

            buf = new_buf()
            with atm(f'{clsname}.read_f64()') as _:
                for _ in _:
                    buf.read_f64()

            buf = cls(bahw1)
            with atm(f'{clsname}.read_str()') as _:
                for _ in _:
                    buf.read_str()

            buf = cls(bahw2)
            with atm(f'{clsname}.read_wstr()') as _:
                for _ in _:
                    buf.read_wstr()

            buf = cls(bazeros)
            with atm(f'{clsname}.read_str() # empty') as _:
                for _ in _:
                    buf.read_str()

            buf = cls(bazeros)
            with atm(f'{clsname}.read_wstr() # empty') as _:
                for _ in _:
                    buf.read_wstr()


if __name__ == '__main__':
    unittest.main()
