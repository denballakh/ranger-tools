"""!
@file
"""

import os
import ctypes

from msl.loadlib import Server32  # type: ignore[import]


class OKGF32(Server32):

    def __init__(self, host, port, **kwargs):
        super().__init__(os.path.join(os.path.dirname(__file__), 'okgf'),
                                     'cdll', host, port)

    def received_data(self, *args, **kwargs):
        return str(self.lib) + ' ' + str(dir(self.lib))
