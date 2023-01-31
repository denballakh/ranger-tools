"""
Перекрашивает .png и .txt в соответствии с правилами
"""
from __future__ import annotations
from typing import Any, Callable, Protocol
import shutil

from math import cos, sin, radians
import time

from PIL import Image

# from rangers.graphics.dithering import dither_bayer

import config


min_alpha = 2

modified_file_delta = config.modified_file_delta

_in = config._1
_out = config._2
_dats = config._dats

dat_file = config.dat_file

modified_rules = config.modified_rules
dat_rule_mod = config.dat_rule_mod

dither = config.dither

PixelType3 = tuple[float, float, float]
PixelType = tuple[float, float, float, float]


class RuleProto(Protocol):
    def __call__(self, a: PixelType, b: PixelType | Any = ..., /) -> PixelType:
        ...


def get_rules() -> dict[str, RuleProto]:
    # transform(red_angle, green_angle, blue_angle, saturation=1.0, value=1.0, brightness=0.0, bias=1.0, gamma=2.2):
    # fmt: off
    # rules = {
    #     # 'Red':      transform(-100.,   0., 160., saturation=1.2, value=1.0),
    #     # 'Green':    transform(   0., 100., 280., saturation=1.2, value=1.0),
    #     'Green':    transform(   0., 100., 280., saturation=1.0, value=0.8),
    #     # 'DarkGreen':transform(   0., 100., 280., saturation=1.0, value=0.5),
    #     # 'Blue':     transform(   0.,   0.,  40.),
    #     # 'Orange':   transform(   0.,   0., 185., saturation=1.2, value=1.2),
    #     # 'Yellow':   transform(   0.,   0., 210., saturation=1.2, value=1.2),
    #     # 'Cyan':     transform(   0.,   0., 335.),
    #     # 'Magenta':  transform(   0.,   0., 100., saturation=1.2, value=1.2),
    #     # 'Grey':     to_grey(brightness=0.3, bias=1.1),
    #     # 'DarkGrey': to_grey(brightness=1.00, bias=1.5),
    #     # 'Kling':    transform(   0.,   0., -40., saturation=1.0, brightness=0.0),
    #     # 'Neon':     transform(   0.,   0., 345., saturation=2.0, brightness=10000.0, value=1.3),
    # }
    rules = {
        'Red':      transform(-100.,   0., 160., saturation=1.2, value=0.9),
        # 'Pink':     transform(-100.,   0., 160., saturation=6.0, value=0.5, brightness=50000,gamma=0.01),
        'Green':    transform(   0., 100., 280., saturation=1.0, value=0.8),
        'Blue':     transform(   0.,   0.,  40., saturation=0.7, value=1.2),
        'DarkGreen':transform(   0., 100., 280., saturation=1.0, value=0.5),
        'Orange':   transform(   0.,   0., 185., saturation=1.0, value=0.9),
        'Yellow':   transform(   0.,   0., 210., saturation=1.5, value=0.95),
        'Cyan':     transform(   0.,   0., 345., saturation=1.4, value=1.05),
        'Magenta':  transform(   0.,   0., 100., saturation=1.0, value=0.9),
        'Grey':     to_grey(brightness=0.3, bias=1.1),
        'DarkGrey': to_grey(brightness=1.00, bias=1.5),
        'Kling':    transform(   0.,   0., -40., saturation=1.0, brightness=0.0),
        #
        'Peleng':   transform(   0.,   0., 230., saturation=1.0, value=0.9),
        'Fei':      transform(   0.,   0.,  80., saturation=1.0, value=0.8),
        #
        'Neon':     transform(   0.,   0., 345., saturation=2.0, brightness=10000.0, value=1.3),
        ## 'Neon2':    transform(   0.,   0., 200., saturation=2.0, brightness=10000.0, value=1.3),
        ## 'Neon3':    transform(   0.,   0.,  15., saturation=2.0, brightness=10000.0, value=1.3),
    }
    # fmt: on
    return rules

# fmt: off
dat_colors: tuple[PixelType3, ...] = (
    ( 91,  91,  91),
    ( 82, 227, 255),
    # (165, 182, 140),
    # (189, 109, 107),
    ( 82, 227, 255),
    # (  0, 255,   0),
    # (255, 127,   0),
    # (255,   0,   0),
    (  0,  40,  57),
    ( 82, 146, 173),
    ( 90, 125, 140),
    ( 57, 117, 140),
    ( 24,  65,  90),
    ( 82, 150, 165),
    ( 41, 101, 123),
    # (173,  56,  57),
    (198, 239, 255),
    (  0, 166, 198),
    ( 49, 239, 255),
    ( 74, 166, 255),
    ( 33, 235, 239),
    (  0,  40,  66),
    (  0, 255, 255),
    (  0, 135, 192),
    ( 37, 178, 189),
    ( 61,  88,  95),
    # (209, 144,  62)
    (  0,  62,  77),
    (  0, 204, 117),
    ( 38, 176, 195),
    (151, 225, 238),
    (171, 198, 207),
    (  0, 110, 176),
    (  0,  34,  54),
    # (  0,   0,   0), # 0x000000
    (  0,   0, 255),  # 0x0000ff
    (  0,  24,  41),  # 0x001829
    (  0,  26,  49),  # 0x001a31
    (  0,  44,  70),  # 0x002c46
    # (  0, 204, 117), # 0x00cc75
    # (  0, 255,   0), # 0x00ff00
    (  0, 255, 255),  # 0x00ffff
    (  7, 105, 158),  # 0x07699e
    ( 27,  68,  98),  # 0x1b4462
    # ( 31,  19,   4), # 0x1f1304
    ( 41, 101, 123),  # 0x29657b
    ( 45, 105, 124),  # 0x2d697c
    ( 50, 240, 252),  # 0x32f0fc
    ( 52, 231, 255),  # 0x34e7ff
    ( 55, 230, 255),  # 0x37e6ff
    ( 57, 103, 103),  # 0x396767
    ( 57, 239, 255),  # 0x39efff
    ( 58,  92, 100),  # 0x3a5c64
    ( 63, 214, 255),  # 0x3fd6ff
    ( 78, 141, 161),  # 0x4e8da1
    ( 85, 113, 128),  # 0x557180
    # ( 86, 214,  14), # 0x56d60e
    ( 88, 229, 255),  # 0x58e5ff
    ( 97, 149, 168),  # 0x6195a8
    # (101, 171, 137), # 0x65ab89
    (102, 177, 201),  # 0x66b1c9
    # (140, 140, 140), # 0x8c8c8c
    (169, 196, 208),  # 0xa9c4d0
    # (174, 203,  60), # 0xaecb3c
    # (177,  89,   0), # 0xb15900
    # (191, 185, 128), # 0xbfb980
    (200, 240, 255),  # 0xc8f0ff
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
)
# fmt: on
dat_colors = tuple(tuple(map(float, x)) for x in dat_colors)  # type: ignore[misc]

dat_prefixes = (
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
)


def recolor_dat() -> None:
    # for color in dat_colors:
    #     r, g, b = color
    #     print(f'({r:>3}, {g:>3}, {b:>3}), # 0x{hex(r)[2:]:0>2}{hex(g)[2:]:0>2}{hex(b)[2:]:0>2}')
    # 1/0

    in_file = _dats / dat_file
    dat_content = in_file.read_text()

    for rulename, rule in rules.items():
        out_file = _out / rulename / dat_file

        if (
            out_file.is_file()
            and out_file.stat().st_mtime > in_file.stat().st_mtime
            and 'test' not in rulename
            and rulename not in modified_rules
            and not dat_rule_mod
        ):
            continue

        print(out_file)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.touch()

        s = dat_content
        for color in dat_colors:
            new_color = rule((*color, 255))[:3]
            _1 = ','.join([str(round(x)) for x in color])
            _2 = ','.join([str(round(x)) for x in new_color])
            for prefix in dat_prefixes:
                if not prefix.endswith('='):
                    prefix = prefix + '='

                s = s.replace(prefix + _1, prefix + _2)

        out_file.write_text(s)


# (1 - k / 2) * k == 1 - (1 - (1 - k / 2)) / k
def darken(k: float, /) -> Callable[[float], float]:
    assert 0 < k < 2, f'Value for k should be between 0 and 2: k = {k}'

    k /= 2  # For balance to be at 1 instead of 0.5
    _k = 1 - k
    kd = k / _k

    def f(x: float) -> float:
        if x > _k:
            return 1 - (1 - x) / kd
        return x * kd

    return f


def average(
    c1: PixelType3,
    c2: PixelType3,
    ratio: float = 0.5,
    /,
) -> PixelType3:
    return tuple(y * ratio + x * (1 - ratio) for x, y in zip(c1, c2))  # type: ignore[return-value]


##
# Clamping to 0, 255
def _clamp(v: float, /) -> int:
    if v < 0.0:
        return 0
    if v > 255.0:
        return 255
    return round(v)


# FIXME move back to interface colorer
def recolor(
    color: PixelType | list[int],
    mask: PixelType | list[int] | None,
    red_angle: float,
    green_angle: float,
    blue_angle: float,
    brightness: float,
    lightness: Callable[[float], float],
    gamma: float,
    p_matrix: tuple[list[list[float]], list[list[float]], list[list[float]]],
) -> PixelType:
    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    mask = mask or (255, 255, 255, 255)

    r, g, b, a = color
    mr, mg, mb, ma = mask

    # mask = mr, mg, mb

    if mr in _255 and mg in _0 and mb in _0:
        angle = red_angle
        matrix = p_matrix[0]
    elif mr in _0 and mg in _255 and mb in _0:
        angle = green_angle
        matrix = p_matrix[1]
    else:
        angle = blue_angle
        matrix = p_matrix[2]

    # elif mr in _0  and mg in _0 and mb in _255:
    #     pass
    # elif mr in _255  and mg in _255 and mb in _255:
    #     pass
    # else:
    #     pass

    # RGB hue rotation
    result: PixelType3 = (
        _clamp(color[0] * matrix[0][0] + color[1] * matrix[0][1] + color[2] * matrix[0][2]),
        _clamp(color[0] * matrix[1][0] + color[1] * matrix[1][1] + color[2] * matrix[1][2]),
        _clamp(color[0] * matrix[2][0] + color[1] * matrix[2][1] + color[2] * matrix[2][2]),
    )

    if angle == blue_angle:
        ratio = ma / 255.0

        if brightness != 0.0 or ratio != 1.0:
            # Linearize RGB from gamma
            result = tuple((channel / 255.0) ** gamma for channel in result)  # type: ignore[assignment]
            # Apply non-linearity
            result = tuple(lightness(channel) for channel in result)  # type: ignore[assignment]

            if ratio != 1.0:
                original: tuple[float, float, float] = tuple((channel / 255.0) ** gamma for channel in (r, g, b))  # type: ignore[assignment]
                result = average(original, result, ratio)

            # De-linearize to gamma
            result = tuple(channel ** (1 / gamma) * 255.0 for channel in result)  # type: ignore[assignment]

    return *result, a


##
# Degree of non-linearity expressed in values `(-∞, +∞)\{0}`. Non-linearity increases when approaching `0`
# Bias is neutral at `1.0`.
# Lowering value shifts bias of the non-linearity towards `0` on the x scale, raising shifts bias towards max
def nonlinear_brightness(dn: float, bias: float = 1.0, /) -> Callable[[float], float]:
    assert bias > 0, f'Value for bias should be higher than 0: bias = {bias}'
    assert dn != 0, 'Value for dn cannot be equal to 0'

    # To reflect behavior of positive dn values
    if dn < 0:
        dn -= 1

    def f(x: float, /) -> float:
        return ((1 + dn) * (x**bias)) / (dn + (x**bias))

    return f


def to_grey(brightness: float, bias: float = 1.0, gamma: float = 2.2) -> RuleProto:
    gamma_inv = 1 / gamma

    size = 5
    _255 = range(256 - size, 256)
    _0 = range(0, 0 + size)

    if brightness != 0:
        lightness = nonlinear_brightness(brightness, bias)
    else:
        lightness = lambda x, /: x

    def f(color: PixelType, mask: PixelType | None = None, /) -> PixelType:
        r, g, b, a = color

        if mask is not None:
            mr, mg, mb, ma = mask

            if mr in _255 and mg in _0 and mb in _0:
                return r, g, b, a
            if mr in _0 and mg in _255 and mb in _0:
                return r, g, b, a

        else:
            ma = 255.0

        # Linearize RGB from gamma
        original: PixelType3 = (
            (r / 255.0) ** gamma,
            (g / 255.0) ** gamma,
            (b / 255.0) ** gamma,
        )
        # Rec. 709 luma grayscale coefficients
        v = original[0] * 0.2126 + original[1] * 0.7152 + original[2] * 0.0722
        # Apply non-linearity
        v = lightness(v)

        ratio = ma / 255.0
        if ratio != 1.0:
            result = average(original, (v, v, v), ratio)
            # De-linearize to gamma
            result = (
                result[0] ** gamma_inv * 255.0,
                result[1] ** gamma_inv * 255.0,
                result[2] ** gamma_inv * 255.0,
            )
        else:
            v = v**gamma_inv * 255.0
            result = v, v, v

        return *result, a

    return f


def transform(
    red_angle: float,
    green_angle: float,
    blue_angle: float,
    saturation: float = 1.0,
    value: float = 1.0,
    brightness: float = 0.0,
    bias: float = 1.0,
    gamma: float = 2.2,
) -> RuleProto:
    # Precompute RGB hue rotation matrices for "red", "green" and "blue" mask angles at start
    p_matrix = (
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    )

    sqrt3 = 3.0**0.5
    for matrix, angle in zip(p_matrix, (red_angle, green_angle, blue_angle)):
        vsu = value * saturation * cos(radians(angle))
        vsu_1_3 = (1.0 - vsu) / 3.0
        vsv = value * saturation * sin(radians(angle))
        vsv_sqrt3 = vsv / sqrt3

        matrix[0][0] = matrix[1][1] = matrix[2][2] = value * vsu + vsu_1_3
        matrix[0][1] = matrix[1][2] = matrix[2][0] = value * vsu_1_3 - vsv_sqrt3
        matrix[0][2] = matrix[1][0] = matrix[2][1] = value * vsu_1_3 + vsv_sqrt3

    if brightness != 0:
        lightness = nonlinear_brightness(brightness, bias)
    else:
        lightness = lambda x, /: x

    return lambda color, mask=None, /: recolor(
        color, mask, red_angle, green_angle, blue_angle, brightness, lightness, gamma, p_matrix
    )


def recolor_two_colors(rule1: RuleProto, rule2: RuleProto) -> RuleProto:
    def f(color: PixelType, mask: PixelType | None = None, /) -> PixelType:
        if mask:
            return rule1(color, mask)
        else:
            return rule2(color, mask)

    return f


rules = get_rules()


def main() -> None:
    recolor_dat()

    for in_file in _in.rglob('**/*'):
        if not in_file.is_file():
            continue

        if in_file.suffix != '.png':
            continue
        if in_file.stem.endswith('_mask'):
            continue
        if in_file.stat().st_size == 0:
            continue

        rel_path = in_file.relative_to(_in)
        img: Image.Image = None  # type: ignore[assignment]
        mask_name = in_file.with_stem(in_file.stem + '_mask')
        universal_mask_name = in_file.with_stem('universal_mask')
        if not mask_name.is_file() and universal_mask_name.is_file():
            mask_name = universal_mask_name

        images: dict[str, Image.Image] = {}

        for rulename in rules:
            out_file = _out / rulename / rel_path
            if (
                out_file.is_file()
                and out_file.stat().st_mtime > in_file.stat().st_mtime
                and (
                    mask_name.is_file()
                    and out_file.stat().st_mtime > mask_name.stat().st_mtime
                    or not mask_name.is_file()
                )
                and 'test' not in rulename
                and rulename not in modified_rules
                or rulename in modified_rules
                and out_file.is_file()
                and out_file.stat().st_mtime > in_file.stat().st_mtime
                and (
                    out_file.stat().st_size == 0
                    or time.time() - out_file.stat().st_mtime < modified_file_delta
                )
            ):
                continue

            print(out_file)

            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.touch()
            print(f'Writing image: {out_file}')

            if img is None:
                img = Image.open(in_file).convert('RGBA')  # type: ignore[unreachable]
            images[rulename] = None  # type: ignore[assignment]  # Just for init

        if not images:
            continue

        mask = None
        if mask_name.is_file():
            mask = Image.open(mask_name).convert('RGBA')
            print(f'Applying mask: {mask_name}')
            assert mask.size == img.size

        images_items = images.items()

        data = list(img.getdata())

        if mask is not None:
            mask_data = list(mask.getdata())

        out_data = []

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
                r, g, b, a = rule(px, mask_px)
                color = (_clamp(round(r)), _clamp(round(g)), _clamp(round(b)), a)
                out_data += color

            out_file = _out / rulename / rel_path
            images[rulename] = Image.frombytes('RGBA', img.size, bytes(out_data))
            # if dither:
            #     images[rulename] = dither_bayer(
            #         images[rulename],
            #         bit_trunc=2,
            #         matrix_n=3,
            #     )
            out_data = []
            images[rulename].save(out_file)

    shutil.copytree(config._override / config._2, config._2, dirs_exist_ok=True)


if __name__ == '__main__':
    main()
