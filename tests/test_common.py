from __future__ import annotations
from typing import TYPE_CHECKING

from itertools import repeat

import rangers.common as common

def test_doc():
    """!

    """


if __name__ == '__main__':
    import doctest
    import os

    doctest.testmod(common)
    doctest.testmod()

    input('Press enter to exit...')
    os._exit(0)

vars.__self__
