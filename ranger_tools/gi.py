from PIL import Image

from .common import bytes_to_uint, uint_to_bytes, rgb24_to_rgb16, rgb16_to_rgb24

__all__ = ['GI']

class Layer:
    _size = 32

    def __init__(self):
        self.seek = None
        self.size = None
        self.start_X = None
        self.start_Y = None
        self.finish_X = None
        self.finish_Y = None
        self.unknown1 = 0
        self.unknown2 = 0

        self.index = None

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Layer':
        layer = cls()

        layer.seek =        bytes_to_uint(data[0 : 4])
        layer.size =        bytes_to_uint(data[4 : 8])
        layer.start_X =     bytes_to_uint(data[8 : 12])
        layer.start_Y =     bytes_to_uint(data[12 : 16])
        layer.finish_X =    bytes_to_uint(data[16 : 20])
        layer.finish_Y =    bytes_to_uint(data[20 : 24])
        layer.unknown1 =    bytes_to_uint(data[24 : 28]) # r0
        layer.unknown2 =    bytes_to_uint(data[28 : 32]) # r1

        return layer

    def to_bytes(self) -> bytes:
        result = b''
        result += uint_to_bytes(self.seek)
        result += uint_to_bytes(self.size)
        result += uint_to_bytes(self.start_X)
        result += uint_to_bytes(self.start_Y)
        result += uint_to_bytes(self.finish_X)
        result += uint_to_bytes(self.finish_Y)
        result += uint_to_bytes(self.unknown1)
        result += uint_to_bytes(self.unknown2)

        return list(result)

    def __repr__(self) -> str:
        s = f'''
        Layer {self.index}:
        seek: {self.seek}
        size: {self.size}
        position: {self.start_X},{self.start_Y} - {self.finish_X},{self.finish_Y}
        unknown1: {self.unknown1}
        unknown2: {self.unknown2}
        '''

        return s


class Header:
    _size = 64

    def __init__(self):
        self.signature = 26983
        self.version = 1
        self.start_X = None
        self.start_Y = None
        self.finish_X = None
        self.finish_Y = None
        self.r_bitmask = None
        self.g_bitmask = None
        self.b_bitmask = None
        self.a_bitmask = None
        self.frame_type = None
        self.layer_count = None
        self.unknown1 = 0
        self.unknown2 = 0
        self.unknown3 = 0
        self.unknown4 = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Header':
        header = cls()
        header.signature =   bytes_to_uint(data[0 : 4])
        header.version =     bytes_to_uint(data[4 : 8])
        header.start_X =     bytes_to_uint(data[8 : 12])
        header.start_Y =     bytes_to_uint(data[12 : 16])
        header.finish_X =    bytes_to_uint(data[16 : 20])
        header.finish_Y =    bytes_to_uint(data[20 : 24])
        header.r_bitmask =   bytes_to_uint(data[24 : 28])
        header.g_bitmask =   bytes_to_uint(data[28 : 32])
        header.b_bitmask =   bytes_to_uint(data[32 : 36])
        header.a_bitmask =   bytes_to_uint(data[36 : 40])
        header.frame_type =  bytes_to_uint(data[40 : 44])
        header.layer_count = bytes_to_uint(data[44 : 48])
        header.unknown1 =    bytes_to_uint(data[48 : 52]) # countUpdateRect
        header.unknown2 =    bytes_to_uint(data[52 : 56]) # smeUpdateRect
        header.unknown3 =    bytes_to_uint(data[56 : 60]) # rz0
        header.unknown4 =    bytes_to_uint(data[60 : 64]) # rz1

        return header

    def to_bytes(self) -> bytes:
        result = b''
        result += uint_to_bytes(self.signature)
        result += uint_to_bytes(self.version)
        result += uint_to_bytes(self.start_X)
        result += uint_to_bytes(self.start_Y)
        result += uint_to_bytes(self.finish_X)
        result += uint_to_bytes(self.finish_Y)
        result += uint_to_bytes(self.r_bitmask)
        result += uint_to_bytes(self.g_bitmask)
        result += uint_to_bytes(self.b_bitmask)
        result += uint_to_bytes(self.a_bitmask)
        result += uint_to_bytes(self.frame_type)
        result += uint_to_bytes(self.layer_count)
        result += uint_to_bytes(self.unknown1)
        result += uint_to_bytes(self.unknown2)
        result += uint_to_bytes(self.unknown3)
        result += uint_to_bytes(self.unknown4)

        return list(result)

    def __repr__(self) -> str:
        s = f'''
        signature: {self.signature}
        version: {self.version}
        position: {self.start_X},{self.start_Y} - {self.finish_X},{self.finish_Y}
        bitmasks: A:{hex(self.a_bitmask):10} R:{hex(self.r_bitmask):10} G:{hex(self.g_bitmask):10} B:{hex(self.b_bitmask):10}
        frame_type: {self.frame_type} ({[
                'One layer, 16 or 32 bit, depends on mask',
                'One layer, 16 bit RGB optimized',
                'Three layers: 16 bit RGB optimized - body, 16 bit RGB optimized - outline, 6 bit Alpha optimized',
                'Two layers: Indexed RGB colors, Indexed Alpha',
                'One layer, indexed RGBA colors',
                'Delta frame of GAI animation',
            ][self.frame_type]})
        layer_count: {self.layer_count}
        unknown1: {self.unknown1}
        unknown2: {self.unknown2}
        unknown3: {self.unknown3}
        unknown4: {self.unknown4}
        '''

        return s


class GI:
    def __init__(self, data: bytes = None):
        self.header = Header.from_bytes(data[:Header._size])

        self.layers = []
        for i in range(self.header.layer_count):
            layer = Layer.from_bytes(data[Header._size + Layer._size * i: Header._size + Layer._size * (i + 1)])
            layer.index = i
            self.layers.append(layer)

        self.data = data

    def __repr__(self) -> str:
        return '\n'.join([repr(self.header)] + [repr(layer) for layer in self.layers])

    @classmethod
    def open(cls, filename: str) -> 'GI':
        with open(filename, 'rb') as file:
            data = list(file.read())

        return GI(data)

    def save(self, filename: str):
        assert filename.endswith('.gi')
        with open(filename, 'wb') as fp:
            fp.write(bytes(self.data))

    @classmethod
    def from_image(cls, img: Image, format=0, bit=None) -> 'GI':
        assert bit in (16, 32, None)
        assert format in (0, 1, 2, 3, 4, 5)

        savers = [
            save_frame_type_0,
            save_frame_type_1,
            save_frame_type_2,
            save_frame_type_3,
            save_frame_type_4,
            save_frame_type_5,
        ]
        saver = savers[format]
        if bit is None:
            return saver(img)
        else:
            return saver(img, bit)

    def to_image(self) -> Image:
        loaders = [
            load_frame_type_0,
            load_frame_type_1,
            load_frame_type_2,
            load_frame_type_3,
            load_frame_type_4,
            load_frame_type_5,
        ]
        loader = loaders[self.header.frame_type]
        return loader(self)


# One layer, 16 or 32 bit, depends on mask
def save_frame_type_0(img: Image, bit=16) -> GI:
    img = img.convert('RGBA')
    width, height = img.size

    header = Header()
    header.start_X = 0
    header.start_Y = 0
    header.finish_X = width
    header.finish_Y = height
    header.frame_type = 0
    header.layer_count = 1

    layer = Layer()
    layer.start_X = 0
    layer.start_Y = 0
    layer.finish_X = width
    layer.finish_Y = height


    data = []

    if bit == 32:
        # RGBA
        # 8888
        header.r_bitmask = 0x00FF0000
        header.g_bitmask = 0x0000FF00
        header.b_bitmask = 0x000000FF
        header.a_bitmask = 0xFF000000
        for y in range(layer.start_Y, layer.finish_Y):
            for x in range(layer.start_X, layer.finish_X):
                r, g, b, a = img.getpixel((x, y))
                data += [b, g, r, a]
    else:
        # RGB16
        # 5650
        header.r_bitmask = 0xF800
        header.g_bitmask = 0x07E0
        header.b_bitmask = 0x001F
        header.a_bitmask = 0x0000
        for y in range(layer.start_Y, layer.finish_Y):
            for x in range(layer.start_X, layer.finish_X):
                r, g, b, a = img.getpixel((x, y))
                data += rgb24_to_rgb16((r, g, b))
                # data += [round(63 - a / 4)]


    layer.size = len(data)
    layer.seek = header._size + layer._size
    data = header.to_bytes() + layer.to_bytes() + data


    gi = GI(data)

    return gi

def save_frame_type_1(img: Image, bit=16) -> GI:
    raise NotImplementedError

def save_frame_type_2(img: Image, bit=16) -> GI:
    img = img.convert('RGBA')
    width, height = img.size

    header = Header()
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

    layer0 = Layer()
    layer0.start_X = 0
    layer0.start_Y = 0
    layer0.finish_X = width
    layer0.finish_Y = height

    layer1 = Layer()
    layer1.start_X = 0
    layer1.start_Y = 0
    layer1.finish_X = width
    layer1.finish_Y = height

    layer2 = Layer()
    layer2.start_X = 0
    layer2.start_Y = 0
    layer2.finish_X = width
    layer2.finish_Y = height

    data0 = []
    data1 = []
    data2 = []

    # for y in range(height):
    #     for x in range(width):
    #         r, g, b, a = img.getpixel((x, y))
    #         if a == 0:
    #             data0 += [0x01]
    #             data1 += [0x01]
    #             data2 += [0x01]
    #         elif a == 255:
    #             data0 += [0x81] + rgb24_to_rgb16((r, g, b))
    #             data1 += [0x01]
    #             data2 += [0x01]
    #         else:
    #             data0 += [0x01]
    #             data1 += [0x81] + rgb24_to_rgb16((r, g, b))
    #             data2 += [0x81] + [round(63 - a / 4)]

    #     data0 += [0x80]
    #     data1 += [0x80]
    #     data2 += [0x80]



    cnt = 0
    pixels = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            if a == 255:
                if cnt and not pixels:
                    data0 += [cnt] # skip cnt pixels
                    cnt = 0
                    pixels = []
                cnt += 1
                pixels += rgb24_to_rgb16((r, g, b))

                if cnt >= 127:
                    data0 += [0x80 + cnt] + pixels # read cnt pixels + pixels
                    cnt = 0
                    pixels = []
            else:
                if pixels:
                    data0 += [0x80 + cnt] + pixels # read cnt pixels + pixels
                    cnt = 0
                    pixels = []
                cnt += 1

                if cnt >= 127:
                    data0 += [cnt] # skip cnt pixels
                    cnt = 0
                    pixels = []
        if pixels:
            data0 += [0x80 + cnt] + pixels # read cnt pixels + pixels
            pixels = []
        elif cnt:
            if cnt == width:
                data0 += [0x80]
                cnt = 0
                continue
            else:
                data0 += [cnt] # skip cnt pixels
        cnt = 0

        # if y != height - 1:
        data0 += [0x00] # go to next line

    cnt = 0
    pixels1 = []
    pixels2 = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            if a not in (0, 255):
                if cnt and not pixels1:
                    data1 += [cnt] # skip cnt pixels
                    data2 += [cnt]
                    cnt = 0
                    pixels1 = []
                    pixels2 = []
                cnt += 1
                pixels1 += rgb24_to_rgb16((r, g, b))
                pixels2 += [round(63 - a / 4)]

                if cnt >= 127:
                    data1 += [0x80 + cnt] + pixels1 # read cnt pixels + pixels
                    data2 += [0x80 + cnt] + pixels2
                    cnt = 0
                    pixels1 = []
                    pixels2 = []
            else:
                if pixels1:
                    data1 += [0x80 + cnt] + pixels1 # read cnt pixels + pixels
                    data2 += [0x80 + cnt] + pixels2
                    cnt = 0
                    pixels1 = []
                    pixels2 = []
                cnt += 1

                if cnt >= 127:
                    data1 += [cnt] # read cnt pixels + pixels
                    data2 += [cnt]
                    cnt = 0
                    pixels1 = []
                    pixels2 = []
        if pixels1:
            data1 += [0x80 + cnt] + pixels1 # read cnt pixels + pixels
            data2 += [0x80 + cnt] + pixels2
            pixels1 = []
            pixels2 = []
        elif cnt:
            if cnt == width:
                data1 += [0x80] # go to next line
                data2 += [0x80]
                cnt = 0
                continue
            else:
                data1 += [cnt]
                data2 += [cnt]

        cnt = 0
        # if y != height - 1:
        data1 += [0x00] # go to next line
        data2 += [0x00]




    # 0, 0x80 - end of line
    # > 0x80 - read (x - 0x80) pixels
    # 0 < x < 0x80 - skip x pixels
    data0 = list(sum([list(int.to_bytes(x, 4, 'little')) for x in (len(data0), width, height, 0x00)], start=[])) + data0
    data1 = list(sum([list(int.to_bytes(x, 4, 'little')) for x in (len(data1), width, height, 0x00)], start=[])) + data1
    data2 = list(sum([list(int.to_bytes(x, 4, 'little')) for x in (len(data2), width, height, 0x00)], start=[])) + data2


    # data0 = list(int.to_bytes(len(data0), 4, 'little')) + [0] * 12 + data0
    # data1 = list(int.to_bytes(len(data1), 4, 'little')) + [0] * 12 + data1
    # data2 = list(int.to_bytes(len(data2), 4, 'little')) + [0] * 12 + data2

    layer0.size = len(data0)
    layer1.size = len(data1)
    layer2.size = len(data2)

    layer0.seek = header._size + layer0._size + layer1._size + layer2._size
    layer1.seek = layer0.seek + layer0.size
    layer2.seek = layer1.seek + layer1.size

    data = header.to_bytes() + layer0.to_bytes() + layer1.to_bytes() + layer2.to_bytes() + data0 + data1 + data2


    gi = GI(data)

    return gi


def save_frame_type_3(img: Image, bit=16) -> GI:
    raise NotImplementedError

def save_frame_type_4(img: Image, bit=32) -> GI:
    raise NotImplementedError

def save_frame_type_5(img: Image, bit=16) -> GI:
    raise NotImplementedError


# One layer, 16 or 32 bit, depends on mask
def load_frame_type_0(gi: GI) -> Image:
    assert gi.header.frame_type == 0
    assert gi.header.layer_count == 1

    header = gi.header
    layer = gi.layers[0]

    assert layer.size

    width = header.finish_X - header.start_X
    height = header.finish_Y - header.start_Y

    # index = layer.seek
    data = gi.data


    if (header.a_bitmask, header.r_bitmask, header.g_bitmask, header.b_bitmask) == (0xFF000000, 0xFF0000, 0xFF00, 0xFF):
        result = Image.new('RGBA', (width, height), (0,0,0,0))

        colors = []
        assert len(data) % 4 == 0

        for i in range(layer.seek, layer.seek + layer.size, 4):
            b, g, r, a = data[i:i+4]

            colors.append((r, g, b, a))

        assert len(colors) == width * height

        for x in range(width):
            for y in range(height):
                result.putpixel((x, y), tuple(colors[y * width + x]))


    elif (header.r_bitmask, header.g_bitmask, header.b_bitmask) == (0xF800, 0x7E0, 0x1F):
        result = Image.new('RGB', (width, height), (0,0,0))

        colors = []
        assert len(data) % 2 == 0

        for i in range(layer.seek, layer.seek + layer.size, 2):
            colors.append(rgb16_to_rgb24(data[i : i + 2]))

        assert len(colors) == width * height

        for x in range(width):
            for y in range(height):
                result.putpixel((x, y), tuple(colors[y * width + x]))

    return result

# One layer, 16 bit RGB optimized
def load_frame_type_1(gi: GI) -> Image:
    assert gi.header.frame_type == 1
    assert gi.header.layer_count == 1
    raise NotImplementedError

# Three layers: 16 bit RGB optimized - body, 16 bit RGB optimized - outline, 6 bit Alpha optimized
def load_frame_type_2(gi: GI) -> Image:
    assert gi.header.frame_type == 2
    assert gi.header.layer_count == 3

    header = gi.header

    width = header.finish_X - header.start_X
    height = header.finish_Y - header.start_Y

    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    data = gi.data


    for li in range(3):
        layer = gi.layers[li]
        if not layer.size: continue
        index = layer.seek
        cnt = 0
        size = bytes_to_uint(data[index : index + 4])
        assert size == layer.size - 16
        index += 16
        pos = [0, 0]


        while size > 0:
            byte = data[index]; index += 1
            size -= 1

            if byte in (0, 0x80):
                # goto new scanline
                pos[0] = 0
                pos[1] += 1

            elif byte > 0x80:
                # pixels found
                cnt = byte & 0x7f
                size -= cnt * (1 if li == 2 else 2)

                while cnt:
                    if li in (0, 1):
                        r, g, b = rgb16_to_rgb24(data[index:index+2])
                        res = (r, g, b, 255)
                        index += 2
                    else:
                        r, g, b, _ = result.getpixel((pos[0] + layer.start_X - header.start_X, pos[1] + layer.start_Y - header.start_Y))
                        alpha = data[index]
                        alpha = 4 * (63 - alpha)
                        res = (r, g, b, alpha)
                        index += 1

                    result.putpixel((pos[0] + layer.start_X - header.start_X, pos[1] + layer.start_Y - header.start_Y), res)


                    pos[0] += 1
                    cnt -= 1

            elif byte < 0x80:
                # shift to right
                pos[0] += byte


    return result

# Two layers: Indexed RGB colors, Indexed Alpha
def load_frame_type_3(gi: GI) -> Image:
    assert gi.header.frame_type == 3
    assert gi.header.layer_count == 2
    raise NotImplementedError

# One layer, indexed RGBA colors
def load_frame_type_4(gi: GI) -> Image:
    assert gi.header.frame_type == 4
    assert gi.header.layer_count == 1
    raise NotImplementedError

# Delta frame of GAI animation
def load_frame_type_5(gi: GI) -> Image:
    assert gi.header.frame_type == 5
    raise NotImplementedError

