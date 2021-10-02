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


def clamp(v, lt, gt):
    if(v <= lt):
        return lt
    if(v >= gt):
        return gt
    return v


def rgb565le_to_rgb888(rgb16: bytes) -> tuple:
    # Unpack from little endian 2 bytes
    r =  rgb16[1] & 0b11111000
    g = (rgb16[0] & 0b11100000) >> 5 | (rgb16[1] & 0b00000111) << 3
    b =  rgb16[0] & 0b00011111

    g <<= 2
    b <<= 3

    return (r, g, b)


def rgb24_to_rgb16(rgb24: tuple) -> bytes:
    r, g, b = rgb24

    r = round(r / 0xff * 0x1f) << 11
    g = round(g / 0xff * 0x3f) << 5
    b = round(b / 0xff * 0x1f)

    if r | g | b > 0xffff:
        raise ValueError

    a, b = divmod(r | g | b, 0x100)

    return bytes([b, a])


def rgb888_to_rgb565le(rgba32: tuple) -> bytes:
    r, g, b, a = rgba32

    if a == 0:
        return bytes([0, 0])

    else:
        if a == 255:
            # Essentially reducing green channel bit depth to 5 for white balance
            g &= 0b11111011

        else:
            # Preventing format from "exploding" color channel values when combined with transparency channel
            if r > a:
                r = max(r - (255 - a), a)

            if g > a:
                g = max(g - (255 - a), a)

            if b > a:
                b = max(b - (255 - a), a)

            # Essentially reducing green channel bit depth for white balance
            g -= g & 0b00000111

        r = r >> 3 << 11
        g = g >> 2 << 5
        b = b >> 3

    # Swap to little endian
    return bytes([g & 0b11100000 | b, (r | g) >> 8])