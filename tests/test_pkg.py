from _utils import *
__all__ = ['TEST']

from ranger_tools.pkg import PKG, PKGItem

class TEST(_common_test):
    def test_init():
        PKG(PKGItem())
