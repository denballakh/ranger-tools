from __future__ import annotations
from pathlib import Path

import time

from PIL import Image
from PIL.Image import Image as ImageType

from ..std.mixin import DataMixin
from ..std.buffer import Buffer, IBuffer, OBuffer
from ..common import rgb565le_to_rgb888, rgb24_to_rgb16, rgb888_to_rgb565le

__all__ = ('GI',)


class Point:
    __slots__ = ('x', 'y')
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Layer:
    def __init__(self) -> None:
        self.start_X: int = 0
        self.start_Y: int = 0
        self.finish_X: int = 0
        self.finish_Y: int = 0
        self.data: bytes = b''

    @classmethod
    def from_bytes(cls, data: bytes) -> Layer:
        return cls.from_buffer(Buffer(data))

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_buffer(cls, buf: IBuffer) -> Layer:
        layer = cls()

        seek = buf.read_u32()
        size = buf.read_u32()
        layer.start_X = buf.read_i32()
        layer.start_Y = buf.read_i32()
        layer.finish_X = buf.read_i32()
        layer.finish_Y = buf.read_i32()
        unknown1 = buf.read_u32()
        unknown2 = buf.read_u32()
        assert unknown1 == 0, unknown1
        assert unknown2 == 0, unknown2

        buf.push_pos(seek)
        layer.data = buf.read(size)
        buf.pop_pos()

        return layer

    def to_buffer(self, buf: OBuffer) -> int:
        seek_pos = buf.pos
        buf.write(b'\xFF' * 4)
        buf.write_u32(len(self.data))
        buf.write_i32(self.start_X)
        buf.write_i32(self.start_Y)
        buf.write_i32(self.finish_X)
        buf.write_i32(self.finish_Y)
        buf.write_u32(0)
        buf.write_u32(0)
        return seek_pos

    def data_to_buffer(self, buf: OBuffer, seek_pos: int) -> None:
        pos = buf.pos
        buf.write(self.data)

        buf.push_pos(seek_pos)
        buf.write_u32(pos)
        buf.pop_pos()

    def __repr__(self) -> str:
        s = (
            f'Layer:\n'
            f'  size: {len(self.data)}\n'
            f'  position: {self.start_X},{self.start_Y} - {self.finish_X},{self.finish_Y}\n'
        )
        return s


class Header:
    def __init__(self) -> None:
        self.start_X: int = 0
        self.start_Y: int = 0
        self.finish_X: int = 0
        self.finish_Y: int = 0
        self.r_bitmask: int = 0
        self.g_bitmask: int = 0
        self.b_bitmask: int = 0
        self.a_bitmask: int = 0
        self.frame_type: int = -1
        self.layer_count: int = -1

    @classmethod
    def from_bytes(cls, data: bytes) -> Header:
        return cls.from_buffer(Buffer(data))

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_buffer(cls, buf: IBuffer) -> Header:
        header = cls()

        signature = buf.read(4)
        assert signature == b'gi\x00\x00', signature
        version = buf.read_u32()
        assert version == 1, version
        header.start_X = buf.read_i32()
        header.start_Y = buf.read_i32()
        header.finish_X = buf.read_i32()
        header.finish_Y = buf.read_i32()
        header.r_bitmask = buf.read_u32()
        header.g_bitmask = buf.read_u32()
        header.b_bitmask = buf.read_u32()
        header.a_bitmask = buf.read_u32()
        header.frame_type = buf.read_u32()
        header.layer_count = buf.read_u32()
        unknown1 = buf.read_u32()
        unknown2 = buf.read_u32()
        unknown3 = buf.read_u32()
        unknown4 = buf.read_u32()
        assert unknown1 == 0, unknown1
        assert unknown2 == 0, unknown2
        assert unknown3 == 0, unknown3
        assert unknown4 == 0, unknown4

        return header

    def to_buffer(self, buf: OBuffer) -> None:
        buf.write(b'gi\x00\x00')
        buf.write_u32(1)
        buf.write_i32(self.start_X)
        buf.write_i32(self.start_Y)
        buf.write_i32(self.finish_X)
        buf.write_i32(self.finish_Y)
        buf.write_u32(self.r_bitmask)
        buf.write_u32(self.g_bitmask)
        buf.write_u32(self.b_bitmask)
        buf.write_u32(self.a_bitmask)
        buf.write_u32(self.frame_type)
        buf.write_u32(self.layer_count)
        buf.write_u32(0)
        buf.write_u32(0)
        buf.write_u32(0)
        buf.write_u32(0)

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


class GI(DataMixin):
    header: Header
    layers: list[Layer]
    metadata: bytes

    def __init__(self, *, metadata: bytes | None = None) -> None:
        self.header = Header()
        self.layers = []

        if metadata is None:
            self.metadata = b'[timestamp: ' + str(int(time.time())).encode() + b']'
        else:
            self.metadata = bytes(metadata)

    def __repr__(self) -> str:
        return '\n'.join([repr(self.header)] + [repr(layer) for layer in self.layers])

    @classmethod
    def from_buffer(cls, buf: IBuffer, **kwargs: object) -> GI:
        gi = cls()
        gi.header = Header.from_buffer(buf)

        gi.layers = []
        for _ in range(gi.header.layer_count):
            layer = Layer.from_buffer(buf)
            gi.layers.append(layer)

        return gi

    def to_buffer(self, buf: OBuffer, **kwargs: object) -> None:
        self.header.to_buffer(buf)
        data_positions = []
        for l in self.layers:
            data_positions.append(l.to_buffer(buf))
        buf.write(self.metadata)
        for i, l in enumerate(self.layers):
            l.data_to_buffer(buf, data_positions[i])

    @classmethod
    def from_gi(cls, path: Path) -> GI:
        with open(path, 'rb') as file:
            data = file.read()

        return cls.from_bytes(data)

    def to_gi(self, path: Path) -> None:
        with open(path, 'wb') as fp:
            fp.write(self.to_bytes())

    @classmethod
    def from_png(cls, path: Path, fmt: int = 2, opt: int = 16) -> GI:
        return cls.from_image(Image.open(path), fmt=fmt, opt=opt)

    def to_png(self, path: Path) -> None:
        self.to_image().save(path)

    @classmethod
    def from_image(cls, img: ImageType, fmt: int | None = 2, opt: int | None = None) -> GI:
        assert fmt in {0, 1, 2, 3, 4, 5}

        if fmt == 0:
            return from_image_0(img, fmt, opt)

        if fmt == 1:
            return from_image_1(img, fmt, opt)

        if fmt == 2:
            return from_image_2(img, fmt, opt)

        if fmt == 3:
            return from_image_3(img, fmt, opt)

        if fmt == 4:
            return from_image_4(img, fmt, opt)

        if fmt == 5:
            return from_image_5(img, fmt, opt)

        raise ValueError

    def to_image(self) -> ImageType:
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
def from_image_0(img: ImageType, fmt: int, opt: int | None = None) -> GI:
    assert fmt == 0

    img = img.convert('RGBA')
    width: int
    height: int
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

    # RGBA8888
    data: list[tuple[int, int, int, int]] = list(img.getdata())

    r: int
    g: int
    b: int
    a: int
    if opt == 32:
        # ARGB8888
        header.a_bitmask = 0xFF000000
        header.r_bitmask = 0x00FF0000
        header.g_bitmask = 0x0000FF00
        header.b_bitmask = 0x000000FF

        for index in range(width * height):
            r, g, b, a = data[index]
            buf.write(bytes([b, g, r, a]))

    elif opt == 16:
        # RGB565 without alpha
        header.a_bitmask = 0x0000
        header.r_bitmask = 0xF800
        header.g_bitmask = 0x07E0
        header.b_bitmask = 0x001F

        for index in range(width * height):
            r, g, b, a = data[index]
            buf.write(rgb24_to_rgb16((r, g, b)))

    else:
        raise ValueError(f'Invalid option value: {opt}')

    layer.data = bytes(buf.data)

    return gi


def from_image_1(img: ImageType, fmt: int, opt: int | None = None) -> GI:
    assert fmt == 1
    raise NotImplementedError


def from_image_2(img: ImageType, fmt: int, opt: int | None = None) -> GI:
    assert fmt == 2
    assert opt is None or opt == 16

    img = img.convert('RGBA')
    width: int
    height: int
    width, height = img.size

    gi = GI()
    header: Header = gi.header
    header.start_X = 0
    header.start_Y = 0
    header.finish_X = width
    header.finish_Y = height
    header.r_bitmask = 0xF800
    header.g_bitmask = 0x07E0
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

    cnt: int = 0
    pixels: bytes = b''

    # RGBA8888
    data: list[tuple[int, int, int, int]] = list(img.getdata())
    index: int = 0

    for y in range(height):
        for x in range(width):
            if data[index][3] == 255:
                if cnt and not pixels:
                    buf0.write_byte(cnt)  # skip cnt pixels
                    cnt = 0
                    pixels = b''
                cnt += 1

                pixels += rgb888_to_rgb565le(data[index][0], data[index][1], data[index][2])

                if cnt >= 127:
                    buf0.write_byte(0x80 + cnt)  # read cnt pixels + pixels
                    buf0.write(pixels)
                    cnt = 0
                    pixels = b''
            else:
                if len(pixels):
                    buf0.write_byte(0x80 + cnt)  # read cnt pixels + pixels
                    buf0.write(pixels)
                    cnt = 0
                    pixels = b''
                cnt += 1

                if cnt >= 127:
                    buf0.write_byte(cnt)  # skip cnt pixels
                    cnt = 0
                    pixels = b''

            index += 1

        if len(pixels):
            buf0.write_byte(0x80 + cnt)  # read cnt pixels + pixels
            buf0.write(pixels)
            pixels = b''

        elif cnt:
            if cnt == width:
                buf0.write_byte(0x80)
                cnt = 0
                continue
            else:
                buf0.write_byte(cnt)  # skip cnt pixels

        cnt = 0

        buf0.write_byte(0x00)  # go to next line

    cnt = 0
    pixels1: bytes = b''
    pixels2: bytes = b''

    index = 0

    for y in range(height):
        for x in range(width):
            if data[index][3] not in {0, 255}:
                if cnt and not pixels1:
                    buf1.write_byte(cnt)  # skip cnt pixels
                    buf2.write_byte(cnt)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''
                cnt += 1

                # Premultiplying pixel by alpha for second layer (destructive operation)
                r = (data[index][0] * data[index][3]) >> 8
                g = (data[index][1] * data[index][3]) >> 8
                b = (data[index][2] * data[index][3]) >> 8

                pixels1 += rgb888_to_rgb565le(r, g, b)
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
                if len(pixels1):
                    buf1.write_byte(0x80 + cnt)
                    buf1.write(pixels1)
                    buf2.write_byte(0x80 + cnt)
                    buf2.write(pixels2)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''
                cnt += 1

                if cnt >= 127:
                    buf1.write_byte(cnt)  # read cnt pixels + pixels
                    buf2.write_byte(cnt)
                    cnt = 0
                    pixels1 = b''
                    pixels2 = b''

            index += 1

        if len(pixels1):
            buf1.write_byte(0x80 + cnt)
            buf1.write(pixels1)
            buf2.write_byte(0x80 + cnt)
            buf2.write(pixels2)
            pixels1 = b''
            pixels2 = b''

        elif cnt:
            if cnt == width:
                buf1.write_byte(0x80)  # go to next line
                buf2.write_byte(0x80)
                cnt = 0
                continue
            else:
                buf1.write_byte(cnt)
                buf2.write_byte(cnt)

        cnt = 0
        buf1.write_byte(0x00)  # go to next line
        buf2.write_byte(0x00)

    buf0_ = Buffer()
    buf0_.write_u32(len(buf0))
    buf0_.write_u32(width)
    buf0_.write_u32(height)
    buf0_.write_u32(0)
    buf0_.write(buf0.data)

    buf1_ = Buffer()
    buf1_.write_u32(len(buf1))
    buf1_.write_u32(width)
    buf1_.write_u32(height)
    buf1_.write_u32(0)
    buf1_.write(buf1.data)

    buf2_ = Buffer()
    buf2_.write_u32(len(buf2))
    buf2_.write_u32(width)
    buf2_.write_u32(height)
    buf2_.write_u32(0)
    buf2_.write(buf2.data)

    layer0.data = bytes(buf0_.data)
    layer1.data = bytes(buf1_.data)
    layer2.data = bytes(buf2_.data)

    return gi


def from_image_3(img: ImageType, fmt: int, opt: int | None = None) -> GI:
    assert fmt == 3
    raise NotImplementedError


def from_image_4(img: ImageType, fmt: int, opt: int | None = None) -> GI:
    assert fmt == 4
    raise NotImplementedError


def from_image_5(img: ImageType, fmt: int, opt: int | None = None) -> GI:
    assert fmt == 5
    raise NotImplementedError


# One layer, 16 or 32 bit, depends on mask
def to_image_0(gi: GI) -> ImageType:
    assert gi.header.frame_type == 0
    assert len(gi.layers) == 1

    header = gi.header
    layer = gi.layers[0]

    width = header.finish_X - header.start_X
    height = header.finish_Y - header.start_Y

    if (header.a_bitmask, header.r_bitmask, header.g_bitmask, header.b_bitmask) == (
        0xFF000000,
        0x00FF0000,
        0x0000FF00,
        0x000000FF,
    ):
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
                img.putpixel((x - header.start_X, y - header.start_Y), rgb565le_to_rgb888(rgb16))

    else:
        raise ValueError(
            f'Invalid bitmask: {(header.r_bitmask, header.g_bitmask, header.b_bitmask)}'
        )

    return img


# One layer, 16 bit RGB optimized
def to_image_1(gi: GI) -> ImageType:
    assert gi.header.frame_type == 1
    assert gi.header.layer_count == 1
    raise NotImplementedError


# Three layers: 16 bit RGB optimized - body, 16 bit RGB optimized - outline, 6 bit Alpha optimized
def to_image_2(gi: GI) -> ImageType:
    assert gi.header.frame_type == 2
    assert len(gi.layers) == 3

    header = gi.header

    width = header.finish_X - header.start_X
    height = header.finish_Y - header.start_Y

    out_data = [0] * ((width * height) * 4)

    for li in range(3):
        layer = gi.layers[li]
        buf = Buffer(layer.data)

        if not buf:
            continue
        size = buf.read_u32()
        assert size == len(layer.data) - 16

        layer_width = buf.read_u32()
        layer_height = buf.read_u32()
        assert layer_width == layer.finish_X - layer.start_X
        assert layer_height == layer.finish_Y - layer.start_Y

        _0 = buf.read_u32()
        assert _0 == 0, _0

        start_X = layer.start_X - header.start_X
        start_Y = layer.start_Y - header.start_Y

        pos = Point(0, 0)

        while buf:
            byte = buf.read_byte()

            if byte in {0, 0x80}:
                # goto new scanline
                pos.x = 0
                pos.y += 1

            elif byte > 0x80:
                # pixels found
                cnt = byte & 0x7F
                size -= cnt * (1 if li == 2 else 2)

                pos_add = (pos.y + start_Y) * width + start_X

                while cnt:
                    index = (pos.x + pos_add) * 4

                    if li in {0, 1}:
                        r, g, b = rgb565le_to_rgb888(buf.read(2))
                        a = 255
                    else:
                        a = (63 - buf.read_byte()) << 2

                        r = out_data[index]
                        g = out_data[index + 1]
                        b = out_data[index + 2]

                        if a not in {0, 255}:
                            # Retrieveing second layer pixel value from premultiplied alpha (destructive operation)
                            r = round((r / a) * 63) << 2
                            g = round((g / a) * 63) << 2
                            b = round((b / a) * 63) << 2

                    out_data[index] = r
                    out_data[index + 1] = g
                    out_data[index + 2] = b
                    out_data[index + 3] = a

                    pos.x += 1
                    cnt -= 1

            elif byte < 0x80:
                # shift to right
                pos.x += byte

    return Image.frombytes('RGBA', (width, height), bytes(out_data))


# Two layers: Indexed RGB colors, Indexed Alpha
def to_image_3(gi: GI) -> ImageType:
    assert gi.header.frame_type == 3
    assert gi.header.layer_count == 2
    raise NotImplementedError


# One layer, indexed RGBA colors
def to_image_4(gi: GI) -> ImageType:
    assert gi.header.frame_type == 4
    assert gi.header.layer_count == 1
    raise NotImplementedError


# Delta frame of GAI animation
def to_image_5(gi: GI) -> ImageType:
    assert gi.header.frame_type == 5
    raise NotImplementedError
