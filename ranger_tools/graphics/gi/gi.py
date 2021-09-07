from PIL import Image
import time

from ...io import Buffer
from ...common import rgb16_to_rgb24, rgb24_to_rgb16, Point, rgba8888_to_rgb565le

__all__ = [
    'GI',
]

class Layer:
    def __init__(self):
        self.start_X = 0
        self.start_Y = 0
        self.finish_X = 0
        self.finish_Y = 0
        self.data = b''


    @classmethod
    def from_bytes(cls, data: bytes) -> 'Layer':
        return cls.from_buffer(Buffer(data))

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_buffer(cls, buf: Buffer) -> 'Layer':
        layer = cls()

        seek = buf.read_uint()
        size = buf.read_uint()
        layer.start_X = buf.read_int()
        layer.start_Y = buf.read_int()
        layer.finish_X = buf.read_int()
        layer.finish_Y = buf.read_int()
        unknown1 = buf.read_uint()
        unknown2 = buf.read_uint()
        assert unknown1 == 0, unknown1
        assert unknown2 == 0, unknown2

        buf.push_pos(seek)
        layer.data = buf.read(size)
        buf.pop_pos()

        return layer

    def to_buffer(self, buf: Buffer):
        seek_pos = buf.pos
        buf.write(b'\xFF' * 4)
        buf.write_uint(len(self.data))
        buf.write_int(self.start_X)
        buf.write_int(self.start_Y)
        buf.write_int(self.finish_X)
        buf.write_int(self.finish_Y)
        buf.write_uint(0)
        buf.write_uint(0)
        return seek_pos

    def data_to_buffer(self, buf: Buffer, seek_pos: int):
        pos = buf.pos
        buf.write(self.data)

        buf.push_pos(seek_pos)
        buf.write_uint(pos)
        buf.pop_pos()


    def __repr__(self) -> str:
        s = (
        f'Layer:\n'
        f'  size: {len(self.data)}\n'
        f'  position: {self.start_X},{self.start_Y} - {self.finish_X},{self.finish_Y}\n'
        )
        return s


class Header:
    def __init__(self):
        self.start_X = 0
        self.start_Y = 0
        self.finish_X = 0
        self.finish_Y = 0
        self.r_bitmask = 0
        self.g_bitmask = 0
        self.b_bitmask = 0
        self.a_bitmask = 0
        self.frame_type = None
        self.layer_count = None

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Header':
        return cls.from_buffer(Buffer(data))

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_buffer(cls, buf: Buffer) -> 'Header':
        header = cls()

        signature = buf.read(4)
        assert signature == b'gi\x00\x00', signature
        version = buf.read_uint()
        assert version == 1, version
        header.start_X = buf.read_int()
        header.start_Y = buf.read_int()
        header.finish_X = buf.read_int()
        header.finish_Y = buf.read_int()
        header.r_bitmask = buf.read_uint()
        header.g_bitmask = buf.read_uint()
        header.b_bitmask = buf.read_uint()
        header.a_bitmask = buf.read_uint()
        header.frame_type = buf.read_uint()
        header.layer_count = buf.read_uint()
        unknown1 = buf.read_uint()
        unknown2 = buf.read_uint()
        unknown3 = buf.read_uint()
        unknown4 = buf.read_uint()
        assert unknown1 == 0, unknown1
        assert unknown2 == 0, unknown2
        assert unknown3 == 0, unknown3
        assert unknown4 == 0, unknown4

        return header

    def to_buffer(self, buf: Buffer):
        buf.write(b'gi\x00\x00')
        buf.write_uint(1)
        buf.write_int(self.start_X)
        buf.write_int(self.start_Y)
        buf.write_int(self.finish_X)
        buf.write_int(self.finish_Y)
        buf.write_uint(self.r_bitmask)
        buf.write_uint(self.g_bitmask)
        buf.write_uint(self.b_bitmask)
        buf.write_uint(self.a_bitmask)
        buf.write_uint(self.frame_type)
        buf.write_uint(self.layer_count)
        buf.write_uint(0)
        buf.write_uint(0)
        buf.write_uint(0)
        buf.write_uint(0)

    def __repr__(self) -> str:
        s = (
            f'position: {self.start_X},{self.start_Y} - {self.finish_X},{self.finish_Y}\n'
            f'bitmasks: A:{hex(self.a_bitmask):10} R:{hex(self.r_bitmask):10} G:{hex(self.g_bitmask):10} B:{hex(self.b_bitmask):10}\n'
            f'''frame_type: {self.frame_type} ({[
                    'One layer, 16 or 32 bit, depends on mask',
                    'One layer, 16 bit RGB optimized',
                    'Three layers: 16 bit RGB optimized - body, 16 bit RGB optimized - outline, 6 bit Alpha optimized',
                    'Two layers: Indexed RGB colors, Indexed Alpha',
                    'One layer, indexed RGBA colors',
                    'Delta frame of GAI animation',
                ][self.frame_type]})\n'''
            f'layer_count: {self.layer_count}\n'
        )

        return s


class GI:
    header: Header
    layers: list[Layer]
    metadata: bytes

    def __init__(self, *, metadata=None):
        self.header = Header()
        self.layers = []

        if metadata is None:
            self.metadata = b'[timestamp: ' + str(int(time.time())).encode() + b']'
        else:
            self.metadata = bytes(metadata)

    def __repr__(self) -> str:
        return '\n'.join([repr(self.header)] + [repr(layer) for layer in self.layers])

    @classmethod
    def from_bytes(cls, data: bytes) -> 'GI':
        return cls.from_buffer(Buffer(data))

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_buffer(cls, buf: Buffer) -> 'GI':
        gi = cls()
        gi.header = Header.from_buffer(buf)

        gi.layers = []
        for _ in range(gi.header.layer_count):
            layer = Layer.from_buffer(buf)
            gi.layers.append(layer)

        return gi

    def to_buffer(self, buf: Buffer):
        self.header.to_buffer(buf)
        data_positions = []
        for l in self.layers:
            data_positions.append(l.to_buffer(buf))
        buf.write(self.metadata)
        for i, l in enumerate(self.layers):
            l.data_to_buffer(buf, data_positions[i])


    @classmethod
    def from_gi(cls, path: str) -> 'GI':
        with open(path, 'rb') as file:
            data = file.read()

        return GI.from_bytes(data)

    def to_gi(self, path: str):
        with open(path, 'wb') as fp:
            fp.write(self.to_bytes())

    @classmethod
    def from_image(cls, img: Image, fmt=2, opt=None) -> 'GI':
        assert fmt in (0, 1, 2, 3, 4, 5)

        converters = {
            0: from_image_0,
            1: from_image_1,
            2: from_image_2,
            3: from_image_3,
            4: from_image_4,
            5: from_image_5,
        }
        converter = converters[fmt]
        return converter(img, fmt, opt)

    def to_image(self) -> Image:
        converters = {
            0: to_image_0,
            1: to_image_1,
            2: to_image_2,
            3: to_image_3,
            4: to_image_4,
            5: to_image_5,
        }
        converter = converters[self.header.frame_type]
        return converter(self)


# One layer, 16 or 32 bit, depends on mask
def from_image_0(img: Image, fmt, opt=None) -> GI:
    assert fmt == 0

    img = img.convert('RGBA')
    width, height = img.size

    gi = GI()
    header = gi.header
    header.start_X = 0
    header.start_Y = 0
    header.finish_X = width
    header.finish_Y = height
    header.frame_type = 0
    header.layer_count = 1

    layer = Layer()
    gi.layers.append(layer)
    layer.start_X = 0
    layer.start_Y = 0
    layer.finish_X = width
    layer.finish_Y = height


    buf = Buffer()

    if opt == 32:
        # RGBA
        # 8888gg
        header.r_bitmask = 0x00FF0000
        header.g_bitmask = 0x0000FF00
        header.b_bitmask = 0x000000FF
        header.a_bitmask = 0xFF000000

        for y in range(layer.start_Y, layer.finish_Y):
            for x in range(layer.start_X, layer.finish_X):
                r, g, b, a = img.getpixel((x, y))
                if a == 0:
                    r, g, b = 0, 255, 0
                buf.write_byte(b)
                buf.write_byte(g)
                buf.write_byte(r)
                buf.write_byte(a)

    elif opt == 16:
        # RGB16
        # 5650
        header.r_bitmask = 0xF800
        header.g_bitmask = 0x07E0
        header.b_bitmask = 0x001F
        header.a_bitmask = 0x0000

        for y in range(layer.start_Y, layer.finish_Y):
            for x in range(layer.start_X, layer.finish_X):
                r, g, b, a = img.getpixel((x, y))
                buf.write(rgb24_to_rgb16((r, g, b)))

    else:
        raise ValueError(f'Invalid option value: {opt}')

    layer.data = bytes(buf)

    return gi

def from_image_1(img: Image, fmt, opt=None) -> GI:
    assert fmt == 1
    raise NotImplementedError

def from_image_2(img: Image, fmt, opt=None) -> GI:
    assert fmt == 2
    assert opt is None or opt == 16

    img = img.convert('RGBA')
    width, height = img.size

    gi = GI()
    header = gi.header
    header.start_X = 0
    header.start_Y = 0
    header.finish_X = width
    header.finish_Y = height
    header.r_bitmask = 0xF800
    header.g_bitmask = 0x07e0
    header.b_bitmask = 0x001F
    header.a_bitmask = 0x0000

    header.frame_type = 2
    header.layer_count = 3

    gi.layers = [Layer(), Layer(), Layer()]

    layer0 = gi.layers[0]
    layer0.start_X = 0
    layer0.start_Y = 0
    layer0.finish_X = width
    layer0.finish_Y = height

    layer1 = gi.layers[1]
    layer1.start_X = 0
    layer1.start_Y = 0
    layer1.finish_X = width
    layer1.finish_Y = height

    layer2 = gi.layers[2]
    layer2.start_X = 0
    layer2.start_Y = 0
    layer2.finish_X = width
    layer2.finish_Y = height

    buf0 = Buffer()
    buf1 = Buffer()
    buf2 = Buffer()

    cnt = 0
    pixels = b''

    # RGBA8888
    data = list(img.getdata())
    index = 0

    for y in range(height):
        for x in range(width):
            if data[index][3] == 255:
                if cnt and not pixels:
                    buf0.write_byte(cnt) # skip cnt pixels
                    cnt = 0
                    pixels = b''
                cnt += 1

                pixels += rgba8888_to_rgb565le(data[index])

                if cnt >= 127:
                    buf0.write_byte(0x80 + cnt) # read cnt pixels + pixels
                    buf0.write(pixels)
                    cnt = 0
                    pixels = b''
            else:
                if pixels:
                    buf0.write_byte(0x80 + cnt) # read cnt pixels + pixels
                    buf0.write(pixels)
                    cnt = 0
                    pixels = b''
                cnt += 1

                if cnt >= 127:
                    buf0.write_byte(cnt) # skip cnt pixels
                    cnt = 0
                    pixels = b''

            index += 1

        if pixels:
            buf0.write_byte(0x80 + cnt) # read cnt pixels + pixels
            buf0.write(pixels)
            pixels = b''
        elif cnt:
            if cnt == width:
                buf0.write_byte(0x80)
                cnt = 0
                continue
            else:
                buf0.write_byte(cnt) # skip cnt pixels

        cnt = 0

        buf0.write_byte(0x00) # go to next line

    cnt = 0
    pixels1 = b''
    pixels2 = b''

    index = 0

    for y in range(height):
        for x in range(width):
            if data[index][3] not in (0, 255):
                if cnt and not pixels1:
                    buf1.write_byte(cnt)  # skip cnt pixels
                    buf2.write_byte(cnt)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''
                cnt += 1

                pixels1 += rgba8888_to_rgb565le(data[index])
                pixels2 += bytes([(255 - data[index][3]) >> 2])

                if cnt >= 127:
                    buf1.write_byte(0x80 + cnt)
                    buf1.write(pixels1)
                    buf2.write_byte(0x80 + cnt)
                    buf2.write(pixels2)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''
            else:
                if pixels1:
                    buf1.write_byte(0x80 + cnt)
                    buf1.write(pixels1)
                    buf2.write_byte(0x80 + cnt)
                    buf2.write(pixels2)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''
                cnt += 1

                if cnt >= 127:
                    buf1.write_byte(cnt) # read cnt pixels + pixels
                    buf2.write_byte(cnt)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''

            index += 1

        if pixels1:
            buf1.write_byte(0x80 + cnt)
            buf1.write(pixels1)
            buf2.write_byte(0x80 + cnt)
            buf2.write(pixels2)
            pixels1 = b''
            pixels2 = b''
        elif cnt:
            if cnt == width:
                buf1.write_byte(0x80) # go to next line
                buf2.write_byte(0x80)
                cnt = 0
                continue
            else:
                buf1.write_byte(cnt)
                buf2.write_byte(cnt)

        cnt = 0
        buf1.write_byte(0x00) # go to next line
        buf2.write_byte(0x00)


    buf0_ = Buffer()
    buf0_.write_uint(len(buf0))
    buf0_.write_uint(width)
    buf0_.write_uint(height)
    buf0_.write_uint(0)
    buf0_.write(buf0)

    buf1_ = Buffer()
    buf1_.write_uint(len(buf1))
    buf1_.write_uint(width)
    buf1_.write_uint(height)
    buf1_.write_uint(0)
    buf1_.write(buf1)

    buf2_ = Buffer()
    buf2_.write_uint(len(buf2))
    buf2_.write_uint(width)
    buf2_.write_uint(height)
    buf2_.write_uint(0)
    buf2_.write(buf2)

    layer0.data = bytes(buf0_)
    layer1.data = bytes(buf1_)
    layer2.data = bytes(buf2_)


    return gi


def from_image_3(img: Image, fmt, opt=None) -> GI:
    assert fmt == 3
    raise NotImplementedError

def from_image_4(img: Image, fmt, opt=None) -> GI:
    assert fmt == 4
    raise NotImplementedError

def from_image_5(img: Image, fmt, opt=None) -> GI:
    assert fmt == 5
    raise NotImplementedError


# One layer, 16 or 32 bit, depends on mask
def to_image_0(gi: GI) -> Image:
    assert gi.header.frame_type == 0
    assert len(gi.layers) == 1

    header = gi.header
    layer = gi.layers[0]

    width = header.finish_X - header.start_X
    height = header.finish_Y - header.start_Y


    if (header.a_bitmask, header.r_bitmask, header.g_bitmask, header.b_bitmask) == (0xFF000000, 0xFF0000, 0xFF00, 0xFF):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

        buf = Buffer(layer.data)
        for y in range(layer.start_Y, layer.finish_Y):
            for x in range(layer.start_X, layer.finish_X):
                b, g, r, a = buf.read(4)
                img.putpixel((x - header.start_X, y - header.start_Y), (r, g, b, a))



    elif (header.r_bitmask, header.g_bitmask, header.b_bitmask) == (0xF800, 0x7E0, 0x1F):
        img = Image.new('RGB', (width, height), (0, 0, 0))

        buf = Buffer(layer.data)
        for y in range(layer.start_Y, layer.finish_Y):
            for x in range(layer.start_X, layer.finish_X):
                rgb16 = buf.read(2)
                img.putpixel((x - header.start_X, y - header.start_Y), rgb16_to_rgb24(rgb16))


    else:
        raise ValueError(f'Invalid bitmask: {(header.r_bitmask, header.g_bitmask, header.b_bitmask)}')

    return img

# One layer, 16 bit RGB optimized
def to_image_1(gi: GI) -> Image:
    assert gi.header.frame_type == 1
    assert gi.header.layer_count == 1
    raise NotImplementedError

# Three layers: 16 bit RGB optimized - body, 16 bit RGB optimized - outline, 6 bit Alpha optimized
def to_image_2(gi: GI) -> Image:
    assert gi.header.frame_type == 2
    assert len(gi.layers) == 3

    header = gi.header

    width = header.finish_X - header.start_X
    height = header.finish_Y - header.start_Y

    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))


    for li in range(3):
        layer = gi.layers[li]
        buf = Buffer(layer.data)

        size = buf.read_uint()
        assert size == len(layer.data) - 16
        width = buf.read_uint()
        height = buf.read_uint()
        assert width == layer.finish_X - layer.start_X
        assert height == layer.finish_Y - layer.start_Y
        _0 = buf.read_uint()
        assert _0 == 0, _0

        pos = Point(0, 0)

        while buf:
            byte = buf.read_byte()

            if byte in (0, 0x80):
                # goto new scanline
                pos.x = 0
                pos.y += 1

            elif byte > 0x80:
                # pixels found
                cnt = byte & 0x7f
                size -= cnt * (1 if li == 2 else 2)

                while cnt:
                    if li in (0, 1):
                        r, g, b = rgb16_to_rgb24(buf.read(2))
                        res = (r, g, b, 255)
                    else:
                        r, g, b, _ = result.getpixel((pos.x + layer.start_X - header.start_X, pos.y + layer.start_Y - header.start_Y))
                        alpha = buf.read_byte()
                        alpha = 4 * (63 - alpha)
                        res = (r, g, b, alpha)

                    result.putpixel((pos.x + layer.start_X - header.start_X, pos.y + layer.start_Y - header.start_Y), res)


                    pos.x += 1
                    cnt -= 1

            elif byte < 0x80:
                # shift to right
                pos.x += byte


    return result

# Two layers: Indexed RGB colors, Indexed Alpha
def to_image_3(gi: GI) -> Image:
    assert gi.header.frame_type == 3
    assert gi.header.layer_count == 2
    raise NotImplementedError

# One layer, indexed RGBA colors
def to_image_4(gi: GI) -> Image:
    assert gi.header.frame_type == 4
    assert gi.header.layer_count == 1
    raise NotImplementedError

# Delta frame of GAI animation
def to_image_5(gi: GI) -> Image:
    assert gi.header.frame_type == 5
    raise NotImplementedError

