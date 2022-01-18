"""!
@file
"""

import os
import ctypes

from msl.loadlib import Client64  # type: ignore[import]

__all__ = [
    'FGInt',
    'FGIntWrapper',
]

class FGInt:
    pass

class FGIntLib(Client64):
    def __init__(self):
        super().__init__(module32='fgint32', append_sys_path=os.path.dirname(__file__))

    def add(self, a, b):
        return self.request32('add', a, b)

    def ConvertBase64to256(self, data: bytes) -> bytes:
        return self.request32('ConvertBase64to256', data)

# FGIntWrapper = FGIntLib()

# print(FGIntWrapper.ConvertBase64to256(b'123123123'))
