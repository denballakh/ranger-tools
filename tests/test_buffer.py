from _utils import *
__all__ = ['TEST']

from ranger_tools.io import Buffer

class TEST(_common_test):
    def test_init():
        assert Buffer().data == b''

        assert Buffer(b'abc').data == b'abc'
        assert Buffer(b'abc').pos == 0
        assert Buffer(b'abc')._position_stack == []

        assert Buffer(bytearray(b'abc')).data == b'abc'
        assert Buffer([97, 98, 99]).data == b'abc'

    def test_eq():
        assert Buffer() == Buffer()
        assert Buffer([]) == Buffer(b'')

