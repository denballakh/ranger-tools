from types import EllipsisType
from typing import cast

import unittest

from rangers.buffer import Buffer


class TestBuffer(unittest.TestCase):
    def test_construction(self) -> None:
        b1 = Buffer(b'abc')
        b2 = Buffer(b'abc')
        b2.pos = 1

        for arg, values in cast(
            list[
                tuple[
                    bytes | tuple[int] | list[int] | Buffer | int | EllipsisType,
                    tuple[bytes, int, list],
                ]
            ],
            [
                (..., (b'', 0, [])),
                (b'', (b'', 0, [])),
                ([], (b'', 0, [])),
                ((), (b'', 0, [])),
                (b'abc', (b'abc', 0, [])),
                (bytearray(b'abc'), (b'abc', 0, [])),
                ([97, 98, 99], (b'abc', 0, [])),
                ((97, 98, 99), (b'abc', 0, [])),
                (b1, (b'abc', 0, [])),
                (b2, (b'abc', 0, [])),
                (0, (b'', 0, [])),
                (10, (b'\0' * 10, 0, [])),
            ],
        ):
            with self.subTest(arg=arg, values=values):
                _position_stack: list
                data, pos, _position_stack = values
                if arg is ...:
                    buf = Buffer()
                else:
                    assert not isinstance(arg, EllipsisType)
                    buf = Buffer(arg)
                # buf = Buffer(arg) if arg is not ... else Buffer()
                if data is not ...:
                    self.assertEqual(buf.data, data)
                if data is not ...:
                    self.assertEqual(buf.pos, pos)
                if data is not ...:
                    self.assertEqual(buf._position_stack, _position_stack)

        self.assertRaises(TypeError, Buffer, None)
        self.assertRaises(ValueError, Buffer, -1)
        self.assertRaises(TypeError, Buffer, Buffer)

    def test_iter(self):
        self.assertEqual(list(Buffer()), [])
        self.assertEqual(list(Buffer(b'abc')), [97, 98, 99])

    def test_repr(self):
        for data, pos in (
            (b'', 0),
            (b'abc', 0),
            (b'abc', 1),
        ):
            self.assertEqual(eval(repr(Buffer(data, pos=pos))), Buffer(data, pos=pos))

    def test_equality(self):
        self.assertEqual(Buffer(), Buffer())
        self.assertEqual(Buffer(), Buffer([]))
        self.assertEqual(Buffer(b''), Buffer([]))

        self.assertEqual(Buffer(b'a'), Buffer(b'a'))
        self.assertEqual(Buffer(b'abc'), Buffer(b'abc'))
        self.assertEqual(Buffer(b'abc'), Buffer([97, 98, 99]))
        self.assertEqual(Buffer(b'\0'), Buffer(1))

        self.assertNotEqual(Buffer(b'a'), Buffer(b'b'))
        self.assertNotEqual(Buffer(b''), Buffer(b'b'))
        self.assertNotEqual(Buffer(b'\0'), Buffer(b''))

    def test_bool(self):
        self.assertFalse(Buffer())
        self.assertTrue(Buffer(b'a'))

    def test_len(self):
        self.assertEqual(len(Buffer()), 0)
        self.assertEqual(len(Buffer(b'a')), 1)
        self.assertEqual(len(Buffer(10)), 10)

    def test_getitem(self):
        self.assertRaises(IndexError, Buffer().__getitem__, 0)
        self.assertEqual(Buffer(b'\0')[0], 0)
        self.assertEqual(Buffer(b'\x99')[0], 0x99)
        self.assertEqual(Buffer(b'abc')[1], 98)

    def test_to_bytes(self):
        b = Buffer(b'abc')
        self.assertEqual(bytes(b), b.to_bytes())
        self.assertEqual(b'abc', b.to_bytes())

        self.assertEqual(Buffer().to_bytes(), b'')


if __name__ == '__main__':
    unittest.main()
