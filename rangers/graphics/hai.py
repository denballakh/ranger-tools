from __future__ import annotations
import os
import itertools
from pathlib import Path
from types import ModuleType

from PIL import Image


# cv2: ModuleType | None
# np: ModuleType | None
# try:
#     import numpy as np  # type: ignore[no-redef]
#     import cv2  # type: ignore[no-redef]
# except ImportError:
#     cv2 = None
#     np = None


from ..std.mixin import DataMixin
from ..std.buffer import Buffer, IBuffer, OBuffer

# from ..std.decorator import profile

__all__ = ('HAI',)

HAI_MAGIC = 0x4210420


class HAI(DataMixin):
    width: int
    height: int
    pal_size: int
    frames: list[tuple[bytes, bytes]]

    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.pal_size = 0
        self.frames = []

    @classmethod
    def from_buffer(cls, buf: IBuffer, **kwargs: object) -> HAI:
        self = cls()
        magic = buf.read_u32()
        if magic != HAI_MAGIC:
            raise ValueError('Invalid magic:', magic)

        self.width = buf.read_u32()
        self.height = buf.read_u32()
        row_bytes = buf.read_u32()
        assert row_bytes == self.width == self.height
        frame_count = buf.read_u32()
        frame_size = buf.read_u32()
        _unk1 = buf.read_u32()
        _unk2 = buf.read_u32()
        _unk3 = buf.read_u32()
        _unk4 = buf.read_u32()
        _unk5 = buf.read_u32()
        _unk6 = buf.read_u32()
        # assert (_unk1, _unk2, _unk2, _unk2, _unk2, _unk2) == (1, 8, 0, 0, 0, 0) # ???
        self.pal_size = buf.read_u32() // 4

        assert frame_size == self.width * self.height + self.pal_size * 4

        for _ in range(frame_count):
            data = buf.read(self.width * self.height)
            palette = buf.read(4 * self.pal_size)
            self.frames.append((data, palette))

        return self

    def to_buffer(self, buf: OBuffer, **kwargs: object) -> None:
        buf.write_u32(HAI_MAGIC)
        buf.write_u32(self.width)
        buf.write_u32(self.height)
        buf.write_u32(self.width)
        buf.write_u32(len(self.frames))
        buf.write_u32(self.width * self.height + self.pal_size * 4)
        buf.write_u32(1)
        buf.write_u32(8)
        buf.write_u32(0)
        buf.write_u32(0)
        buf.write_u32(0)
        buf.write_u32(0)
        buf.write_u32(self.pal_size * 4)

        for data, palette in self.frames:
            assert len(data) == self.width * self.height
            assert len(palette) == 4 * self.pal_size
            buf.write(data)
            buf.write(palette)

    @classmethod
    def from_images(cls, images: list[Image.Image]) -> HAI:
        self = cls()

        self.width = max(img.size[0] for img in images)
        self.height = max(img.size[1] for img in images)
        assert self.width > 0
        assert self.height > 0

        self.pal_size = 256

        for img in images:
            img = img.convert('RGBA')
            img = img.resize((self.width, self.height))
            img = img.quantize(self.pal_size)

            pal = img.getpalette()
            assert pal is not None
            palbuf = Buffer(bytearray(pal))
            assert len(palbuf.data) == self.pal_size * 3, len(palbuf.data)

            data = bytes(img.getdata())
            palette = bytearray()

            while palbuf:
                rgb = palbuf.read(3)
                palette.extend(rgb)
                palette.append(255 * any(x > 1 for x in rgb))

            assert len(palette) == self.pal_size * 4, len(palette)
            self.frames.append((data, bytes(palette)))

        return self

    def to_images(self) -> list[Image.Image]:
        result: list[Image.Image] = []
        size = self.width, self.height

        for data, palette in self.frames:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            result.append(img)
            palbuf = Buffer(palette)
            pal: list[tuple[int, int, int, int]] = []
            while palbuf:
                pal.append(
                    (
                        palbuf.read_byte(),
                        palbuf.read_byte(),
                        palbuf.read_byte(),
                        palbuf.read_byte(),
                    ),
                )

            for (j, i), index in zip(
                itertools.product(
                    range(self.width),
                    range(self.height),
                ),
                data,
            ):
                img.putpixel((i, j), pal[index])

        return result

    @classmethod
    def from_image_folder(cls, path: Path) -> HAI:
        images: list[Image.Image] = []
        for filename in sorted(os.listdir(path)):
            images.append(Image.open(os.path.join(path, filename)))
        return cls.from_images(images)

    def to_image_folder(self, path: Path) -> None:

        images = self.to_images()
        for i, img in enumerate(images):
            filename = path / f'{i:03}.png'
            img.save(filename)


# def get_pallete(
#     img: list[tuple[int, int, int, int]],
#     pal_size: int = 256,
# ) -> tuple[list[int], list[tuple[int, int, int, int]]]:
#     # bad pallete
#     # palette: list[tuple[int, int, int, int]] = [
#     #     (r * 255 // 3, g * 255 // 3, b * 255 // 3, a * 255 // 3)
#     #     for r, g, b, a in itertools.product(range(4), range(4), range(4), range(4))
#     # ]
#     # S = 63
#     # R = lambda x: clamp(round(x), 0, 3)
#     # data: list[int] = [
#     #     (R(r / S) + R(g / S) * 4 + R(b / S) * 16 + R(a / S) * 64) % 256
#     #     for y, x in itertools.product(range(height), range(width))
#     #     for r, g, b, a in [img.getpixel((x, y))]
#     # ]
#     ...
