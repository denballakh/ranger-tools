# from __future__ import annotations
# from typing import Callable

# import unittest
# import pathlib
# import tempfile
# import filecmp

# import rangers.dat

# test_files = pathlib.Path() / 'test_data' / 'dat'


# class TestDat(unittest.TestCase):
#     def test_conversions(self) -> None:
#         cls = rangers.dat.DAT
#         for folder_name, ext1, ext2 in (
#             ('txt2dat', '.txt', '.dat'),
#             ('txt2json', '.txt', '.json'),
#             ('json2txt', '.json', '.txt'),
#             ('json2dat', '.json', '.dat'),
#             ('dat2txt', '.dat', '.txt'),
#             ('dat2json', '.dat', '.json'),
#         ):
#             folder = test_files / folder_name
#             for file in [
#                 file for file in folder.iterdir() if file.is_file() and file.suffix == ext1
#             ]:
#                 with self.subTest(folder=folder_name, file=file):
#                     result_file = file.parent / (file.stem + '_result' + ext2)
#                     self.assertTrue(
#                         result_file.is_file(), f'no result file {result_file} for file {file}'
#                     )

#                     with tempfile.TemporaryDirectory() as tempdir:
#                         temp_file = pathlib.Path(tempdir) / result_file.name
#                         cls.from_file(file).to_file(temp_file, fmt='HDMain', sign=False)
#                         # self.assertTrue(filecmp.cmp(result_file, temp_file))
#                         self.assertEqual(cls.from_file(result_file), cls.from_file(temp_file))
#                         self.assertEqual(cls.from_file(result_file), cls.from_file(file))


# class TestSign(unittest.TestCase):
#     @unittest.skipUnless(rangers.dat.DAT_SIGN_AVAILABLE, 'dat sign not available')
#     def test_sign_available(self) -> None:
#         sign_data = rangers.dat.sign_data
#         unsign_data = rangers.dat.unsign_data
#         get_sign = rangers.dat.get_sign
#         check_signed = rangers.dat.check_signed

#         data = b'0123'

#         self.assertEqual(len(get_sign(b'')), 8)
#         self.assertEqual(len(sign_data(b'')), 8)
#         self.assertEqual(get_sign(b''), sign_data(b''))

#         self.assertEqual(len(get_sign(data)), 8)
#         self.assertEqual(len(sign_data(data)), 8 + len(data))

#         self.assertEqual(get_sign(data), get_sign(data))

#         self.assertTrue(check_signed(sign_data(data)))
#         self.assertFalse(check_signed(get_sign(data)))

#         self.assertEqual(data, unsign_data(data))
#         self.assertEqual(sign_data(data), sign_data(sign_data(data)))
#         self.assertEqual(data, unsign_data(sign_data(data)))
#         self.assertEqual(data, unsign_data(sign_data(sign_data(b'0123'))))

#     @unittest.skipIf(rangers.dat.DAT_SIGN_AVAILABLE, 'dat sign available')
#     def test_sign_not_available(self) -> None:
#         sign_data = rangers.dat.sign_data
#         unsign_data = rangers.dat.unsign_data
#         get_sign = rangers.dat.get_sign
#         check_signed = rangers.dat.check_signed

#         data = b'0123'
#         self.assertEqual(get_sign(data), b'')
#         self.assertEqual(check_signed(data), b'')


# if __name__ == '__main__':
#     unittest.main()


from itertools import repeat
import gc

from rangers.std.buffer import Buffer, FastBuffer
from rangers.std.time import AdaptiveTimeMeasurer, print_stats


def test_speed() -> None:
    gc.enable()
    gc.collect()
    gc.disable()

    with AdaptiveTimeMeasurer(
        target_time=0.1,
        config_file='_buffer_bench.json',
        adapt_ratio=10,
    ) as atm:
        print()
        print()

        T = atm('empty loop', extra=2)
        T.calibrate(0)
        with T as cnt:
            for _ in repeat(None, cnt):
                pass
        assert T.time is not None
        T.calibrate(T.time)

        with atm('calibrated empty loop') as cnt:
            for _ in repeat(None, cnt):
                pass

        ba = bytearray(b'0123' * 10**8)
        bahw1 = bytearray(b'hello world\0' * 10**8)
        bahw2 = bytearray(b'hello world\0\0' * 10**8)
        bazeros = bytearray(b'\0' * 10**8)
        new_buf = lambda: cls(ba)

        gc.collect()

        cls: type[Buffer]
        for cls in (Buffer, FastBuffer):  # type: ignore[assignment]
            clsname = cls.__name__
            print()

            with atm(f'{clsname}()') as cnt:
                for _ in repeat(None, cnt):
                    cls()

            buf = cls()
            with atm(f'{clsname}.write(b"")') as cnt:
                for _ in repeat(None, cnt):
                    buf.write(b"")

            buf = cls()
            with atm(f'{clsname}.write([])') as cnt:
                for _ in repeat(None, cnt):
                    buf.write([])

            buf = cls()
            with atm(f'{clsname}.write_byte(7)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_byte(7)

            buf = cls()
            with atm(f'{clsname}.write_bool(True)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_bool(True)

            buf = cls()
            with atm(f'{clsname}.write_char(-123)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_char(-123)

            buf = cls()
            with atm(f'{clsname}.write_uchar(123)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_uchar(123)

            buf = cls()
            with atm(f'{clsname}.write_short(-1234)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_short(-1234)

            buf = cls()
            with atm(f'{clsname}.write_ushort(1234)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_ushort(1234)

            buf = cls()
            with atm(f'{clsname}.write_int(-123456789)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_int(-123456789)

            buf = cls()
            with atm(f'{clsname}.write_uint(123456789)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_uint(123456789)

            buf = cls()
            with atm(f'{clsname}.write_long(-123456789)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_long(-123456789)

            buf = cls()
            with atm(f'{clsname}.write_ulong(123456789)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_ulong(123456789)

            buf = cls()
            with atm(f'{clsname}.write_float(1.23)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_float(1.23)

            buf = cls()
            with atm(f'{clsname}.write_double(1.23)') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_double(1.23)

            buf = cls()
            with atm(f'{clsname}.write_str("hello world")') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_str("hello world")

            buf = cls()
            with atm(f'{clsname}.write_wstr("hello world")') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_wstr("hello world")

            buf = cls()
            with atm(f'{clsname}.write_str("")') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_str("")

            buf = cls()
            with atm(f'{clsname}.write_wstr("")') as cnt:
                for _ in repeat(None, cnt):
                    buf.write_wstr("")

            buf = new_buf()
            with atm(f'{clsname}.read(0)') as cnt:
                for _ in repeat(None, cnt):
                    buf.read(0)

            buf = new_buf()
            with atm(f'{clsname}.read(3)') as cnt:
                for _ in repeat(None, cnt):
                    buf.read(3)

            buf = new_buf()
            with atm(f'{clsname}.read_byte()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_byte()

            buf = new_buf()
            with atm(f'{clsname}.read_bool()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_bool()

            buf = new_buf()
            with atm(f'{clsname}.read_char()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_char()

            buf = new_buf()
            with atm(f'{clsname}.read_uchar()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_uchar()

            buf = new_buf()
            with atm(f'{clsname}.read_short()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_short()

            buf = new_buf()
            with atm(f'{clsname}.read_ushort()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_ushort()

            buf = new_buf()
            with atm(f'{clsname}.read_int()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_int()

            buf = new_buf()
            with atm(f'{clsname}.read_uint()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_uint()

            buf = new_buf()
            with atm(f'{clsname}.read_long()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_long()

            buf = new_buf()
            with atm(f'{clsname}.read_ulong()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_ulong()

            buf = new_buf()
            with atm(f'{clsname}.read_float()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_float()

            buf = new_buf()
            with atm(f'{clsname}.read_double()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_double()

            buf = cls(bahw1)
            with atm(f'{clsname}.read_str()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_str()

            buf = cls(bahw2)
            with atm(f'{clsname}.read_wstr()') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_wstr()

            buf = cls(bazeros)
            with atm(f'{clsname}.read_str() # empty') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_str()

            buf = cls(bazeros)
            with atm(f'{clsname}.read_wstr() # empty') as cnt:
                for _ in repeat(None, cnt):
                    buf.read_wstr()


# FastBuffer(b'h\0e\0l\0l\0o\0 \0\0\0').read_wstr()

# print(repr(FastBuffer(b'h\0e\0l\0l\0o\0 \0\0\0').read_wstr()))
# print(repr(FastBuffer(b'hello \0').read_str()))
# 1/0

# print_stats('_buffer_bench.json')
# input()
while 1:
    test_speed()



# Buffer()                            715 ns ±  37 ns [ 11 s  /  15395385]
# FastBuffer()                        286 ns ±  10 ns [ 11 s  /  36077201]

# Buffer.write(b"")                   450 ns ±  26 ns [ 11 s  /  24823359]
# FastBuffer.write(b"")               129 ns ± 7.3 ns [ 11 s  /  76168184]

# Buffer.write([])                    518 ns ±  41 ns [ 11 s  /  21238649]
# FastBuffer.write([])                203 ns ±  13 ns [ 11 s  /  53820102]

# Buffer.write_byte(7)                809 ns ±  63 ns [ 12 s  /  14228176]
# FastBuffer.write_byte(7)            110 ns ± 9.7 ns [ 10 s  /  86114053]

# Buffer.write_bool(True)             953 ns ±  73 ns [ 11 s  /  11735535]
# FastBuffer.write_bool(True)         205 ns ±  11 ns [ 11 s  /  50177194]

# Buffer.write_char(-123)             881 ns ±  35 ns [ 10 s  /  11638660]
# FastBuffer.write_char(-123)         179 ns ± 5.3 ns [9.4 s  /  50185981]

# Buffer.write_uchar(123)             1.0 μs ±  97 ns [ 11 s  /  11153612]
# FastBuffer.write_uchar(123)         204 ns ± 7.7 ns [ 11 s  /  50143048]

# Buffer.write_short(-1234)           1.0 μs ±  99 ns [ 12 s  /  11286774]
# FastBuffer.write_short(-1234)       225 ns ±  10 ns [ 11 s  /  45239593]

# Buffer.write_ushort(1234)           1.0 μs ±  88 ns [ 11 s  /  11405513]
# FastBuffer.write_ushort(1234)       213 ns ±  18 ns [9.0 s  /  40412644]

# Buffer.write_int(-123456789)        1.0 μs ±  85 ns [ 12 s  /  11639850]
# FastBuffer.write_int(-123456789)    223 ns ±  19 ns [ 10 s  /  44821129]

# Buffer.write_uint(123456789)        882 ns ±  70 ns [ 11 s  /  11992540]
# FastBuffer.write_uint(123456789)    230 ns ±  13 ns [ 11 s  /  44535605]

# Buffer.write_long(-123456789)       823 ns ±  21 ns [ 10 s  /  12060420]
# FastBuffer.write_long(-123456789)   243 ns ±  13 ns [ 11 s  /  43152958]

# Buffer.write_ulong(123456789)       877 ns ±  11 ns [ 10 s  /  11531390]
# FastBuffer.write_ulong(123456789)   241 ns ±  13 ns [ 11 s  /  43906395]

# Buffer.write_float(1.23)            956 ns ±  47 ns [ 11 s  /  11267576]
# FastBuffer.write_float(1.23)        235 ns ±  14 ns [ 11 s  /  46321523]

# Buffer.write_double(1.23)           904 ns ±  53 ns [ 11 s  /  11976005]
# FastBuffer.write_double(1.23)       226 ns ± 5.6 ns [ 10 s  /  44199261]

# Buffer.write_str("hello world")     710 ns ±  10 ns [ 10 s  /  14287677]
# FastBuffer.write_str("hello world") 438 ns ±  14 ns [9.6 s  /  21450954]

# Buffer.write_wstr("hello world")    972 ns ±  16 ns [ 10 s  /  10557721]
# FastBuffer.write_wstr("hello world")844 ns ±  76 ns [ 12 s  /  13915922]

# Buffer.read(0)                      341 ns ± 4.9 ns [ 10 s  /  29559279]
# FastBuffer.read(0)                  221 ns ±  15 ns [ 11 s  /  48999915]

# Buffer.read(3)                      376 ns ± 8.0 ns [ 10 s  /  27011376]
# FastBuffer.read(3)                  291 ns ±  31 ns [ 12 s  /  41339568]

# Buffer.read_byte()                  505 ns ±  12 ns [ 10 s  /  19438052]
# FastBuffer.read_byte()              192 ns ±  13 ns [ 11 s  /  55792394]

# Buffer.read_bool()                  749 ns ±  24 ns [ 11 s  /  14224945]
# FastBuffer.read_bool()              210 ns ±  16 ns [ 11 s  /  50396593]

# Buffer.read_char()                  717 ns ±  13 ns [ 10 s  /  14330302]
# FastBuffer.read_char()              487 ns ±  35 ns [ 12 s  /  23233082]

# Buffer.read_uchar()                 731 ns ±  15 ns [ 10 s  /  14095149]
# FastBuffer.read_uchar()             461 ns ±  29 ns [ 11 s  /  24077347]

# Buffer.read_short()                 709 ns ± 5.1 ns [ 10 s  /  14035916]
# FastBuffer.read_short()             570 ns ±  77 ns [ 14 s  /  23532931]

# Buffer.read_ushort()                789 ns ±  40 ns [ 11 s  /  14043041]
# FastBuffer.read_ushort()            472 ns ±  28 ns [ 11 s  /  23356404]

# Buffer.read_int()                   770 ns ±  40 ns [ 11 s  /  14069991]
# FastBuffer.read_int()               485 ns ±  29 ns [ 11 s  /  22950519]

# Buffer.read_uint()                  758 ns ±  36 ns [ 11 s  /  13942726]
# FastBuffer.read_uint()              481 ns ±  28 ns [ 11 s  /  22548956]

# Buffer.read_long()                  835 ns ±  54 ns [ 12 s  /  13687542]
# FastBuffer.read_long()              555 ns ±  67 ns [ 13 s  /  23259272]

# Buffer.read_ulong()                 732 ns ±  35 ns [ 10 s  /  13909597]
# FastBuffer.read_ulong()             552 ns ±  65 ns [ 13 s  /  23598458]

# Buffer.read_float()                 722 ns ±  14 ns [ 10 s  /  14198728]
# FastBuffer.read_float()             493 ns ±  38 ns [ 12 s  /  23564143]

# Buffer.read_double()                743 ns ±  20 ns [ 11 s  /  14101804]
# FastBuffer.read_double()            471 ns ±  28 ns [ 11 s  /  23074513]

# Buffer.read_str()                   6.8 μs ± 204 ns [ 11 s  /   1570795]
# FastBuffer.read_str()               1.3 μs ± 114 ns [ 10 s  /   7460148]

# Buffer.read_wstr()                  8.3 μs ± 417 ns [ 11 s  /   1352803]
# FastBuffer.read_wstr()              2.3 μs ± 214 ns [ 12 s  /   5177602]

# Buffer.read_str() # empty           1.9 μs ±  52 ns [ 11 s  /   5423331]
# FastBuffer.read_str() # empty       581 ns ±  70 ns [ 13 s  /  21928734]

# Buffer.read_wstr() # empty          1.9 μs ±  56 ns [ 11 s  /   5427784]
# FastBuffer.read_wstr() # empty      595 ns ±  40 ns [ 11 s  /  17482355]

