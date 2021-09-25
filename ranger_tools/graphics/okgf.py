import os
import ctypes

from msl.loadlib import Client64

__all__ = [
    'OKGF',
]

class OKGF(Client64):

    def __init__(self):
        super().__init__(module32='okgf32-server', append_sys_path=os.path.dirname(__file__))

    def send_data(self, *args, **kwargs):
        return self.request32('received_data', *args, **kwargs)

