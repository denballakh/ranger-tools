import os

class Point:
    __slots__ = ['x', 'y']
    def __repr__(self) -> str:
        return f'<Point: x={self.x!r} y={self.y!r}>'

    def __init__(self, x, y):
        self.x = x
        self.y = y


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, 'little', signed=True)

def bytes_to_uint(b: bytes) -> int:
    return int.from_bytes(b, 'little', signed=False)

def uint_to_bytes(n: int) -> bytes:
    return n.to_bytes(4, 'little', signed=False)

def int_to_bytes(n: int) -> bytes:
    return n.to_bytes(4, 'little', signed=True)


def bytes_xor(bytes1: bytes, bytes2: bytes) -> bytes:
    assert len(bytes1) == len(bytes2)
    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))


def bytes_to_str(b: bytes) -> str:
    return ''.join([chr(x) for x in b])

def str_to_bytes(s: str, l: int = 63) -> bytes:
    result = bytes(ord(c) for c in s)
    result = result + b'\0' * (l - len(result))
    return result


def check_dir(path):
    path = path.replace('\\', '/').replace('//', '/')
    splitted = path.split('/')[:-1]
    splitted = [name.strip('/') for name in splitted]
    splitted = [name for name in splitted if name != '']
    splitted = [name + '/' for name in splitted]
    res = './'
    for _, item in enumerate(splitted):
        res += item
        if not os.path.isdir(res):
            os.mkdir(res)


def rgb16_to_rgb24(rgb16: bytes) -> tuple:
    b, a = rgb16
    x = a * 0x100 + b
    r = round((x >> 11 & 0b011111) * (0xff / 0x1f))
    g = round((x >> 5  & 0b111111) * (0xff / 0x3f))
    b = round((x       & 0b011111) * (0xff / 0x1f))

    return [r, g, b]

def rgb24_to_rgb16(rgb24: tuple) -> bytes:
    r, g, b = rgb24
    r = round(r / 0xff * 0x1f) << 11
    g = round(g / 0xff * 0x3f) << 5
    b = round(b / 0xff * 0x1f)

    if r | g | b > 0xffff:
        raise ValueError

    a, b = divmod(r | g | b, 0x100)

    return bytes([b, a])
