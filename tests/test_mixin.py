from __future__ import annotations
from typing import TYPE_CHECKING

from itertools import repeat

from rangers.std.mixin import PrintFormat, PrintableMixin
from rangers.common import is_compiled

COMPILED = PrintFormat.format.__class__.__name__ != 'function'


def test_doc():
    """!
    >>> obj = type('cls', (), {})()
    >>> obj.x = 0
    >>> obj.y = 1
    >>> obj._p = 2
    >>> obj.__d = 3
    >>> obj.__a__ = 4
    >>> print(PrintFormat().format(obj))
    <cls: x=0 y=1>
    >>> print(PrintFormat(use_private_attrs=True).format(obj))
    <cls: x=0 y=1 _p=2 __d=3 __a__=4>
    >>> print(PrintFormat(attrs=('x', '_p')).format(obj))
    <cls: x=0 _p=2>
    >>> print(PrintFormat(attrs=('x', '_p'), pos_only_attrs=('x', '_p')).format(obj))
    <cls: 0 2>
    >>> print(PrintFormat(attrs=('y', 'x', '_p', '__d'), pos_only_attrs=('_p', 'x')).format(obj))
    <cls: 2 0 y=1 __d=3>

    >>> print(PrintFormat(attrs=('y', 'x', '_p'), pos_only_attrs=('x', '_p'), use_private_attrs=True).format(obj))
    <cls: 0 2 y=1>
    >>> print(PrintFormat(attrs=('y', 'x', '_p'), pos_only_attrs=('x', '_p')).format(obj))
    <cls: 0 2 y=1>
    >>> print(PrintFormat(attrs=('',), fmt_empty='<{class_name}>').format(obj))
    <cls>

    """


if __name__ == '__main__':
    import doctest
    import os

    res = doctest.testmod()

    input('Press enter to exit...')
    os._exit(res.failed)
