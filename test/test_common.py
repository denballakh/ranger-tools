from __future__ import annotations
from typing import Any, NoReturn

import unittest
import doctest

import rangers.common


def load_tests(
    loader: unittest.TestLoader, tests: unittest.TestSuite, ignore: object
) -> unittest.TestSuite:
    tests.addTests(doctest.DocTestSuite(rangers.common))
    return tests


class TestTypedEqual(unittest.TestCase):
    def setUp(self) -> None:
        self.cls = rangers.common.TypedEqual

    def test_slots(self) -> None:
        data = 'some data'
        x = self.cls(data)
        self.assertTrue(hasattr(x, 'obj'))
        self.assertEqual(x.obj, data)
        x.obj
        x.obj = x

        with self.assertRaises(AttributeError):
            x.a = x  # type: ignore[attr-defined]

        with self.assertRaises(AttributeError):
            x.a  # type: ignore[attr-defined]

    def test_hash(self) -> None:
        data: object
        for data in (0, 1, -1, 0.5, '', (), 1.2j):
            self.assertEqual(hash(self.cls(data)), hash(data))

        self.assertRaises(TypeError, hash, self.cls([]))
        self.assertRaises(TypeError, hash, self.cls({}))

    def test_eq(self) -> None:
        self.assertFalse(self.cls(1) == 0)
        self.assertTrue(self.cls(1) == 1)
        self.assertFalse(self.cls('a') == 'b')
        self.assertFalse(self.cls('a') == {})
        self.assertTrue(self.cls('') == '')
        self.assertTrue(self.cls({}) == {})

    def test_ne(self) -> None:
        self.assertFalse(self.cls(1) != 1)
        self.assertTrue(self.cls(1) != 2)
        self.assertTrue(self.cls(1) != 1.0)
        self.assertTrue(self.cls(1) != True)
        self.assertTrue(self.cls(1) != False)
        self.assertTrue(self.cls(()) != (1,))
        self.assertFalse(self.cls(()) != ())
        self.assertFalse(self.cls([]) != [])


class TestIdentityEqual(unittest.TestCase):
    def setUp(self) -> None:
        self.cls = rangers.common.IdentityEqual

    def test_slots(self) -> None:
        data = 'some data'
        x = self.cls(data)
        self.assertTrue(hasattr(x, 'obj'))
        self.assertEqual(x.obj, data)
        x.obj
        x.obj = x

        with self.assertRaises(AttributeError):
            x.a = x  # type: ignore[attr-defined]

        with self.assertRaises(AttributeError):
            x.a  # type: ignore[attr-defined]

    def test_hash(self) -> None:
        data: object
        for data in (0, 1, -1, 0.5, '', (), 1.2j):
            with self.subTest(data=data):
                self.assertEqual(hash(self.cls(data)), hash(data))

        self.assertRaises(TypeError, hash, self.cls([]))
        self.assertRaises(TypeError, hash, self.cls({}))

    def test_eq(self) -> None:
        x_ = 'a'
        y_ = 2
        self.assertIsNot(x_, y_)
        x = self.cls(x_)
        y = self.cls(y_)

        self.assertTrue(x == x_)
        self.assertFalse(x != x_)
        self.assertTrue(y == y_)
        self.assertFalse(y != y_)
        self.assertTrue(x != y_)
        self.assertFalse(x == y_)
        self.assertTrue(x != x)
        self.assertTrue(x != y)
        self.assertTrue(self.cls(0) == 0)
        self.assertFalse(self.cls(0) != 0)


class TestFunctions(unittest.TestCase):
    def test_mapping_proxy_hack(self) -> None:
        from types import MappingProxyType
        from collections import Counter, defaultdict

        func = rangers.common._get_mappingproxy_dict

        mapping: Any
        for mapping in ({1: 2}, Counter('abcddd'), defaultdict(int)):
            with self.subTest(mapping=mapping):
                self.assertIs(mapping, func(MappingProxyType(mapping)))

    def test_assert(self) -> None:
        func = rangers.common.assert_
        func(1)
        self.assertRaises(AssertionError, func, 0)

    def test_raise(self) -> None:
        func = rangers.common.raise_
        self.assertRaises(RuntimeError, func, RuntimeError)
        self.assertRaises(ImportError, func, ImportError)

    def test_hashable(self) -> None:
        func = rangers.common.hashable
        self.assertTrue(func(0))
        self.assertTrue(func(()))
        self.assertTrue(func(func))
        self.assertTrue(func('abc'))
        self.assertTrue(func(frozenset()))
        self.assertTrue(func(int))

        self.assertFalse(func([]))
        self.assertFalse(func({}))
        self.assertFalse(func(bytearray()))

        class X1:
            def __hash__(self) -> NoReturn:
                raise IndexError

        class X2:
            def __hash__(self) -> NoReturn:
                raise TypeError

        class X3:
            def __hash__(self) -> None:  # type: ignore[override]
                return None

        self.assertRaises(IndexError, func, X1())
        self.assertFalse(func(X2()))
        self.assertFalse(func(X3()))


if __name__ == '__main__':
    unittest.main()
