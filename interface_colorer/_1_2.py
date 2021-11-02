"""
Перекрашивает .png и .txt в соответствии с правилами
"""
from math import cos, sin, radians, sqrt
from random import sample
import os
import time

from PIL import Image

from rangers.common import check_dir, identity, _clamp, darken, average, my_mul, nonlinear_brightness, recolor

import config

Image.MAX_IMAGE_PIXELS = 4096 ** 2

min_alpha = 2

# Controlled by main.py
rewrite = config.rewrite
randomize = config.randomize
PROFILE = config.PROFILE

modified_file_delta = config.modified_file_delta

_in = config._1
_out = config._2
_dats = config._dats

dat_file = config.dat_file

modified_rules = config.modified_rules
dat_rule_mod = config.dat_rule_mod


def get_rules():
    # transform(red_angle, green_angle, blue_angle, saturation=1.0, value=1.0, brightness=0.0, bias=1.0, gamma=2.2):

    rules = {
        'Red':      transform(-90, 0, 160, saturation=1.08, value=0.98),
        # 'Green':    transform(0, 90, 280),
        # 'Blue':     transform(0, 0, 40),

        # 'Yellow':   transform(0, 0, 220),
        # 'Cyan':     transform(0, 0, 340),
        # 'Magenta':  transform(0, 0, 100),

        # 'Grey':     to_grey(brightness=0.42),
        # 'DarkGrey': to_grey(brightness=6.00, bias=1.03)
    }
    return rules

dat_colors = [
    ( 91,  91,  91),

    ( 82, 227, 255),
    # (165,182,140),
    # (189,109,107),
    ( 82, 227, 255),
    # (0,255,0),
    # (255,127,0),
    # (255,0,0),
    (  0,  40,  57),
    ( 82, 146, 173),
    ( 90, 125, 140),
    ( 57, 117, 140),
    ( 24,  65,  90),
    ( 82, 150, 165),
    ( 41, 101, 123),
    # (173,56,57),
    (198, 239, 255),
    (  0, 166, 198),
    ( 49, 239, 255),
    ( 74, 166, 255),
    ( 33, 235, 239),
    (  0,  40,  66),
    (  0, 255, 255),

    (  0, 135, 192),  #
    ( 37, 178, 189),  #
    ( 61,  88,  95),  #
    # (209, 144,  62), #

    (  0,  62,  77),
    (  0, 204, 117),
    ( 38, 176, 195),
    (151, 225, 238),
    (171, 198, 207),
    (  0, 110, 176),
    (  0,  34,  54),

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



def to_grey(brightness, bias=1.0, gamma=2.2):
    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    if brightness != 0:
        lightness = nonlinear_brightness(brightness, bias)
    else:
        lightness = identity

    def f(color, mask=None):
        mask = mask or (255, 255, 255, 255)

        r, g, b, a = color
        mr, mg, mb, ma = mask

        #mask = mr, mg, mb

        if mr in _255 and mg in _0 and mb in _0:
            return r, g, b, a
        if mr in _0 and mg in _255 and mb in _0:
            return r, g, b, a

        # Linearize RGB from gamma
        original = tuple((channel / 255) ** gamma for channel in (r, g, b))
        # Rec. 709 luma grayscale coefficients
        v = original[0] * .2126 + original[1] * .7152 + original[2] * .0722
        # Apply non-linearity
        v = lightness(v)

        ratio = ma / 255
        if ratio != 1.0:
            result = v, v, v
            result = average(original, result, ratio)
        # De-linearize to gamma
            result = tuple(channel ** (1 / gamma) * 255 for channel in result)
        else:
            v = v ** (1 / gamma) * 255
            result = v, v, v

        return *result, a

    return f


def transform(red_angle, green_angle, blue_angle, saturation=1.0, value=1.0, brightness=0.0, bias=1.0, gamma=2.2):
    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    # Precompute RGB hue rotation matrices for "red", "green" and "blue" mask angles at start
    p_matrix = ([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],
                [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],
                [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    angles = (red_angle, green_angle, blue_angle)

    for matrix, angle in zip(p_matrix, angles):
        vsu = value * saturation * cos(radians(angle))
        vsv = value * saturation * sin(radians(angle))

        matrix[0][0] = value *       vsu       + (1 - vsu) /      3
        matrix[0][1] = value * ((1 - vsu) / 3) -      vsv  / sqrt(3)
        matrix[0][2] = value * ((1 - vsu) / 3) +      vsv  / sqrt(3)
        matrix[1][0] = value * ((1 - vsu) / 3) +      vsv  / sqrt(3)
        matrix[1][1] = value *       vsu       + (1 - vsu) /      3
        matrix[1][2] = value * ((1 - vsu) / 3) -      vsv  / sqrt(3)
        matrix[2][0] = value * ((1 - vsu) / 3) -      vsv  / sqrt(3)
        matrix[2][1] = value * ((1 - vsu) / 3) +      vsv  / sqrt(3)
        matrix[2][2] = value *       vsu       + (1 - vsu) /      3

    if brightness != 0:
        lightness = nonlinear_brightness(brightness, bias)
    else:
        lightness = identity

    return lambda color, mask=None: recolor(
        color, mask,
        red_angle, green_angle, blue_angle,
        brightness, lightness, gamma,
        p_matrix
    )


def recolor_two_colors(rule1, rule2):
    def f(color, mask=None):
        if mask:
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

            images = {}

            for rulename in rules:
                out_name = _out + f'{rulename}/{path2}/{file}'
                out_name = out_name.replace('\\', '/').replace('//', '/')
                if not rewrite \
                   and os.path.isfile(out_name) \
                   and os.path.getmtime(out_name) > os.path.getmtime(filename) \
                   and (os.path.isfile(mask_name) and os.path.getmtime(out_name) > os.path.getmtime(mask_name)
                        or not os.path.isfile(mask_name)) \
                   and 'test' not in rulename \
                   and rulename not in modified_rules \
                        or rulename in modified_rules \
                       and os.path.isfile(out_name) \
                       and os.path.getmtime(out_name) > os.path.getmtime(filename) \
                       and (os.stat(out_name).st_size == 0
                            or time.time() - os.path.getmtime(out_name) < modified_file_delta): continue

                check_dir(out_name)
                open(out_name, 'wb').close()
                print('Writing image: ' + out_name)

                if img is None:
                    img = Image.open(filename).convert('RGBA')
                images[rulename] = None  # Just for init

            if not images: continue

            mask = None
            if os.path.isfile(mask_name):
                mask = Image.open(mask_name).convert('RGBA')
                print('Applying mask: ' + mask_name.replace('\\', '/').replace('//', '/'))
                assert mask.size == img.size

            images_items = images.items()

            data = list(img.getdata())

            if mask is not None:
                mask_data = list(mask.getdata())

            out_data = []

            # start_time = time.perf_counter_ns()

            for rulename, image in images_items:
                for i, px in enumerate(data):
                    if px[-1] < min_alpha:
                        # out_data += (0, 0, 0, 0)
                        out_data += px
                        continue

                    mask_px = None
                    if mask is not None:
                        mask_px = mask_data[i]

                    rule = rules[rulename]
                    r, g, b, a = rule(px, mask_px)  # if mask_px is not None else rule(px)
                    color = (_clamp(round(r)), _clamp(round(g)), _clamp(round(b)), a)
                    out_data += color

                out_name = _out + f'{rulename}/{path2}/{file}'
                images[rulename] = Image.frombytes('RGBA', img.size, bytes(out_data))
                out_data = []
                images[rulename].save(out_name)

            # print('Saving  image: {:<32}'.format(rulename + '/' + file) + ' -   ' + '{:>16}'.format(time.perf_counter_ns() - start_time) + ' ns')


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

        if not os.path.isdir('logs'):
            try:
                os.mkdir('logs')
            except FileExistsError:
                pass
        with open('logs/time_profiling_1_2.log', 'wt') as file:
            file.write(s.getvalue())
