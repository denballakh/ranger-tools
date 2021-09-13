'''
Перекрашивает .png и .txt в соответствии с правилами
'''
from PIL import Image  # type: ignore[import]
from random import sample
import os
# import sys
import colorsys
# from math import ceil
import time

randomize = False

Image.MAX_IMAGE_PIXELS = 4096 ** 2

min_alpha = 2

rewrite = False
PROFILE = True
modified_file_delta = 3600 # s

_in = '1_converted/'
_out = '2_colored/'
_dats = '_dats/'

dat_file = 'Main.txt'

modified_rules = []
dat_rule_mod = 0

def get_rules():
    rules = {
        'Red':           transform(-4/18, 0, 8/18),
        'Green':         transform(0, 4/18, -4/18, dark=0.9),
        'Blue':          transform(0, 0, 2/18, dark=1.0),

        'Grey':          to_grey(1.00),
        'DarkGrey':      to_grey(0.75),
    }

    return rules

dat_colors = [
    (91,91,91),

    (82,227,255),
    # (165,182,140),
    # (189,109,107),
    (82,227,255),
    # (0,255,0),
    # (255,127,0),
    # (255,0,0),
    (0,40,57),
    (82,146,173),
    (90,125,140),
    (57,117,140),
    (24,65,90),
    (82,150,165),
    (41,101,123),
    # (173,56,57),
    (198,239,255),
    (0,166,198),
    (49,239,255),
    (74,166,255),
    (33,235,239),
    (0,40,66),
    (0,255,255),



    (  0, 135, 192), #
    ( 37, 178, 189), #
    ( 61,  88,  95), #
    # (209, 144,  62), #

    (0,62,77),
    (0,204,117),
    (38,176,195),
    (151,225,238),
    (171,198,207),
    (0,110,176),
    (0,34,54),


    # (  0,   0,   0), # 0x000000
    (  0,   0, 255), # 0x0000ff
    (  0,  24,  41), # 0x001829
    (  0,  26,  49), # 0x001a31
    (  0,  44,  70), # 0x002c46
    # (  0, 204, 117), # 0x00cc75
    # (  0, 255,   0), # 0x00ff00
    (  0, 255, 255), # 0x00ffff
    (  7, 105, 158), # 0x07699e
    ( 27,  68,  98), # 0x1b4462
    # ( 31,  19,   4), # 0x1f1304
    ( 41, 101, 123), # 0x29657b
    ( 45, 105, 124), # 0x2d697c
    ( 50, 240, 252), # 0x32f0fc
    ( 52, 231, 255), # 0x34e7ff
    ( 55, 230, 255), # 0x37e6ff
    ( 57, 103, 103), # 0x396767
    ( 57, 239, 255), # 0x39efff
    ( 58,  92, 100), # 0x3a5c64
    ( 63, 214, 255), # 0x3fd6ff
    ( 78, 141, 161), # 0x4e8da1
    ( 85, 113, 128), # 0x557180
    # ( 86, 214,  14), # 0x56d60e
    ( 88, 229, 255), # 0x58e5ff
    ( 97, 149, 168), # 0x6195a8
    # (101, 171, 137), # 0x65ab89
    (102, 177, 201), # 0x66b1c9
    # (140, 140, 140), # 0x8c8c8c
    (169, 196, 208), # 0xa9c4d0
    # (174, 203,  60), # 0xaecb3c
    # (177,  89,   0), # 0xb15900
    # (191, 185, 128), # 0xbfb980
    (200, 240, 255), # 0xc8f0ff
    # (204, 161, 101), # 0xcca165
    # (212, 212, 212), # 0xd4d4d4
    # (219, 218, 156), # 0xdbda9c
    # (226, 212, 148), # 0xe2d494
    # (247, 148,  29), # 0xf7941d
    # (252, 169,  50), # 0xfca932
    # (254, 255, 255), # 0xfeffff
    # (255,   0,   0), # 0xff0000
    # (255, 166,   0), # 0xffa600
    # (255, 222,   0), # 0xffde00
    # (255, 239, 132), # 0xffef84
    # (255, 240, 100), # 0xfff064
    # (255, 255,   0), # 0xffff00
    # (255, 255, 230), # 0xffffe6
    # (255, 255, 255), # 0xffffff
]

dat_prefixes = [
    'TextColor',
    'TextShadowColor',
    'CaptionColorDown',
    'CaptionColorDownA',
    'CaptionColorNormal',
    'CaptionColorNormalA',
    'CaptionShadowColorDown',
    'CaptionShadowColorDownA',
    'CaptionShadowColorNormal',
    'CaptionShadowColorNormalA',
    'CaptionColorDisable',
    'CaptionColorDisableA',
    'CaptionShadowColorDisable',
    'CaptionShadowColorDisableA',
    # 'TransColor',


    'MapsNameColor',
    'QuestsNameColor',
    'MapsNameColor',
    'ColorNormal',
    'ColorSelected',
    'ColorActive',
    'ColorProblems',
    'ColorCriticalProblems',
    'NewSaveNormal',
    'NewSaveSelected',
    'SlotNormal',
    'SlotSelected',
    'BlinkColorA',
    'BlinkColorB',
    'ExpPointsToSpendOnSelf',
    'ExpPointsToSpendOnOther',
    'ModeColorNormal',
    'ModeColorHighlighted',
    'TextColor',
    'DateTransitionColor',
    'GoodsColorOutOfStock',
    'InfoNameColor',
    'InfoHullSeriesColor',
    'StarInfoObjectType',
]


def recolor_dat():
    # for color in dat_colors:
    #     r, g, b = color
    #     print(f'({r:>3}, {g:>3}, {b:>3}), # 0x{hex(r)[2:]:0>2}{hex(g)[2:]:0>2}{hex(b)[2:]:0>2}')
    # 1/0

    filename = _dats + dat_file
    with open(filename, 'rt') as fp:
        dat_str = str(fp.read())

    for rulename, rule in rules.items():
        out_name = _out + rulename + '/' + dat_file

        if not rewrite \
            and os.path.isfile(out_name) \
            and os.path.getmtime(out_name) > os.path.getmtime(filename) \
            and 'test' not in rulename \
            and rulename not in modified_rules \
            and not dat_rule_mod:
            continue

        print(out_name)
        check_dir(out_name)
        open(out_name, 'wb').close()

        s = str(dat_str)
        for color in dat_colors:
            new_color = rule([*color, 255])[:3]
            _1 = ','.join([str(round(x)) for x in color])
            _2 = ','.join([str(round(x)) for x in new_color])
            for prefix in dat_prefixes:
                if not prefix.endswith('='):
                    prefix = prefix + '='

                s = s.replace(prefix + _1, prefix + _2)

        with open(out_name, 'wt') as fp:
            fp.write(s)


def darken(k):
    assert 0 < k < 2, f'Invalid k value: k = {k}'
    k = k / 2
    _k = 1 - k
    kk = k / _k
    def f(x):
        if x > _k:
            return 1 - (1 - x) / kk
        else:
            return x * kk
    return f

def my_mul(x, mn, mx, mul):
    assert mul >= 0
    if mul < 1:
        result = mn + (x - mn) * mul
    elif mul > 1:
        result = mx - (mx - x) / mul
    else:
        result = x
    return min(max(result, mn), mx)

def rotate(color, angle):
    if len(color) == 4:
        r, g, b, a = color
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + angle) % 1
        R, G, B = colorsys.hsv_to_rgb(h, s, v)
        A = a
        return R, G, B, A
    else:
        r, g, b = color
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + angle) % 1
        R, G, B = colorsys.hsv_to_rgb(h, s, v)
        return R, G, B

def average(c1, c2, ratio=0.5):
    return tuple(y * ratio + x * (1 - ratio) for x, y in zip(c1, c2))

def to_grey(k):
    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    darker = darken(k)

    def f(color, mask=None):
        mask = mask or (255, 255, 255, 255)

        r, g, b, a = color
        mr, mg, mb, ma = mask

        color = r, g, b
        mask = mr, mg, mb

        if mr in _255  and mg in _0 and mb in _0:
            return *color, a
        if mr in _0  and mg in _255 and mb in _0:
            return *color, a

        v = max(color)
        # result = colorsys.hls_to_rgb(0, 0, v)
        result = v, v, v
        # result = tuple(255 * x for x in result)
        # result = (r,g,b)

        ratio = ma / 255
        result = tuple(darker(c / 255) * 255 for c in result)
        result = average(color, result, ratio)

        return *result, a

    return f


def transform(red_angle, green_angle, blue_angle, dark=1.0):

    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    darker = darken(dark)

    def f(color, mask=None):
        mask = mask or (255, 255, 255, 255)

        r, g, b, a = color
        mr, mg, mb, ma = mask

        color = r, g, b
        mask = mr, mg, mb


        ratio = ma / 255
        angle = blue_angle

        if mr in _255  and mg in _0 and mb in _0:
            return *rotate(color, red_angle), a
        if mr in _0  and mg in _255 and mb in _0:
            return *rotate(color, green_angle), a
        # elif mr in _0  and mg in _0 and mb in _255:
        #     pass
        # elif mr in _255  and mg in _255 and mb in _255:
        #     pass
        # else:
        #     pass

        result = rotate(color, angle)
        result = tuple(darker(c / 255) * 255 for c in result)
        result = average(color, result, ratio)

        return *result, a

    return f



def recolor_two_colors(rule1, rule2):
    def f(color, mask=None):
        if (mask):
            return rule1(color, mask)
        else:
            return rule2(color, mask)
    return f




rules = get_rules()

def process():
    recolor_dat()

    walk = os.walk(_in)
    if randomize:
        walk = list(walk)
        walk = sample(walk, k=len(walk))
    for path, _, files in walk:
        for file in sample(files, k=len(files)) if randomize else files:
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            if not filename.endswith('.png'): continue
            if filename.endswith('_mask.png'): continue
            if os.stat(filename).st_size == 0: continue
            path2 = path.replace(_in, '', 1)

            img = None
            mask_name = filename.replace('.png', '_mask.png')
            universal_mask_name = path + '/' + 'universal_mask.png'
            if not os.path.isfile(mask_name) and os.path.isfile(universal_mask_name):
                mask_name = universal_mask_name
                # print(mask_name)

            images = {}

            for rulename in rules:
                out_name = _out + f'{rulename}/{path2}/{file}'
                out_name = out_name.replace('\\', '/').replace('//', '/')
                if not rewrite \
                    and os.path.isfile(out_name) \
                    and os.path.getmtime(out_name) > os.path.getmtime(filename) \
                    and (os.path.isfile(mask_name) and os.path.getmtime(out_name) > os.path.getmtime(mask_name) or not os.path.isfile(mask_name)) \
                    and 'test' not in rulename \
                    and rulename not in modified_rules \
                    or \
                    rulename in modified_rules and \
                    os.path.isfile(out_name) \
                    and os.path.getmtime(out_name) > os.path.getmtime(filename) \
                    and (os.stat(out_name).st_size == 0 or time.time() - os.path.getmtime(out_name) < modified_file_delta):
                    continue

                check_dir(out_name)
                open(out_name, 'wb').close()
                print(out_name)

                if img is None:
                    img = Image.open(filename).convert('RGBA')
                images[rulename] = Image.new('RGBA', img.size)

            if not images: continue

            width, _ = img.size
            data = list(img.getdata())

            mask = None
            if os.path.isfile(mask_name):
                mask = Image.open(mask_name).convert('RGBA')
                assert mask.size == img.size

            res = {rulename: [] for rulename in images}
            images_items = images.items()
            for i, px in enumerate(data):
                # if i % 10000 == 0: print(f'{round(i / len(data) * 100, 1): >5} %')
                y, x = divmod(i, width)


                for rulename, image in images_items:
                    image.putpixel((x, y), px)

                if px[-1] < min_alpha:
                    continue

                mask_px = None
                if mask is not None:
                    mask_px = mask.getpixel((x, y))

                for rulename, image in images_items:
                    rule = rules[rulename]
                    color = rule(px, mask_px)# if mask_px is not None else rule(px)
                    color = tuple(max(min(255, round(x)), 0) for x in color)
                    image.putpixel((x, y), color)

            for rulename, data in res.items():
                for i, px in enumerate(data):
                    y, x = divmod(i, width)
                    images[rulename].putpixel((x, y), px)

                out_name = _out + f'{rulename}/{path2}/{file}'
                images[rulename].save(out_name)


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
            try:
                os.mkdir(res)
            except FileExistsError:
                pass

if __name__ == '__main__':
    if PROFILE:
        import cProfile
        import pstats
        import io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

    process()

    if PROFILE:
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.TIME  # CALLS CUMULATIVE FILENAME LINE NAME NFL PCALLS STDNAME TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        with open('logs/time_profiling_1_2.log', 'wt') as file:
            file.write(s.getvalue())



