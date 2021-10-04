import os


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]:
        if abs(num) < 1024.0:
            if isinstance(num, int):
                return f"{num} {unit}{suffix}"
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} {unit}{suffix}"


def pretty_size(n, pow=0, b=1024, u='B', pre=[''] + [p + 'i' for p in 'KMGTPEZY']):
    from math import log

    pow, n = min(int(log(max(n * b ** pow, 1), b)), len(pre) - 1), n * b ** pow
    return "%%.%if %%s%%s" % abs(pow % (-pow - 1)) % (n / b ** float(pow), pre[pow], u)


def prettier_size(n, pow=0, b=1024, u='B', pre=[''] + [p + 'i' for p in 'KMGTPEZY']):
    r, f = min(int(log(max(n * b ** pow, 1), b)), len(pre) - 1), '{:,.%if} %s%s'
    return (f % (abs(r % (-r - 1)), pre[r], u)).format(n * b ** pow / b ** float(r))


def check_dir(path):
    path = path.replace('\\', '/').replace('//', '/')
    splitted = path.split('/')[:-1]
    splitted = [name.strip('/') for name in splitted]
    splitted = [name for name in splitted if name != '']
    splitted = [name + '/' for name in splitted]
    res = './'
    for item in splitted:
        res += item
        if not os.path.isdir(res):
            os.mkdir(res)


def clamp(v, lt, gt):
    if v <= lt:
        return lt
    if v >= gt:
        return gt
    return v


def rgb565le_to_rgb888(rgb16: bytes) -> tuple:
    # Unpack from little endian 2 bytes
    r = rgb16[1] & 0b11111000
    g = (rgb16[0] & 0b11100000) >> 5 | (rgb16[1] & 0b00000111) << 3
    b = rgb16[0] & 0b00011111

    g <<= 2
    b <<= 3

    return r, g, b


def rgb24_to_rgb16(rgb24: tuple) -> bytes:
    r, g, b = rgb24

    r = round(r / 0xFF * 0x1F) << 11
    g = round(g / 0xFF * 0x3F) << 5
    b = round(b / 0xFF * 0x1F)

    if r | g | b > 0xFFFF:
        raise ValueError

    a, b = divmod(r | g | b, 0x100)

    return bytes([b, a])


def rgb888_to_rgb565le(r, g, b) -> bytes:
    # Essentially reducing green channel bit depth to 5 after reduction for white balance
    g &= 0b11111011

    r = r >> 3 << 11
    g = g >> 2 << 5
    b = b >> 3

    # Pack into little endian 2 bytes
    return bytes([g & 0b11100000 | b, (r | g) >> 8])
