"""!
@file
"""
from __future__ import annotations

import zlib

from PIL import Image


from ..std.mixin import DataMixin
from ..std.dataclass import ZL
from ..buffer import Buffer
from .gi import GI

__all__ = ('GAI',)

# //! Header of animation in *.gai file
# struct GAIHeader
# {
#     uint32_t signature;  //!< File signature
#     uint32_t version;  //!< Format version
#     uint32_t startX;  //!< Left corner
#     uint32_t startY;  //!< Top corner
#     uint32_t finishX;  //!< Right corner
#     uint32_t finishY;  //!< Bottom corner
#     uint32_t frameCount; //!< Number of frames in animation
#     uint32_t haveBackground; //!< Animation a background in separate file
#     uint32_t waitSeek;  //!< Wait seek?
#     uint32_t waitSize;  //!< Wait size?
#     uint32_t unknown1;
#     uint32_t unknown2;
# };


# struct Animation
# {
#     QVector<QImage> images;
#     QVector<int> times;
# };


class GAIFrame:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'<GAIFrame: {vars(self)}>'

    @classmethod
    def from_buffer(cls, buf: Buffer) -> GAIFrame:
        buf.push_pos()
        signature = buf.read(4)
        buf.pop_pos()
        if signature in {b'ZL01', b'ZL02'}:
            buf = Buffer(buf.read_dcls(ZL(mode=1)))

        gi = GI.from_buffer(buf)

        raise NotImplementedError

    def to_buffer(self, buf: Buffer) -> None:
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: bytes) -> GAIFrame:
        buf = Buffer(data)
        return cls.from_buffer(buf)

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return buf.to_bytes()


class GAI(DataMixin):
    start_X: int
    start_Y: int
    finish_X: int
    finish_Y: int
    have_background: bool
    frames: list[GAIFrame]
    delays: list[int]

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'<GAI: {vars(self)}>'

    @classmethod
    def from_buffer(cls, buf: Buffer) -> GAI:
        self = cls()

        signature = buf.read(4)
        print(f'{signature = }')
        format_version = buf.read_uint()
        print(f'{format_version = }')
        self.start_X = buf.read_int()
        self.start_Y = buf.read_int()
        self.finish_X = buf.read_int()
        self.finish_Y = buf.read_int()
        frame_count = buf.read_uint()
        self.have_background = bool(buf.read_uint())
        wait_seek = buf.read_uint()
        wait_size = buf.read_uint()

        self.frames = []

        gi_seek_size = []
        for _ in range(frame_count):
            seek = buf.read_uint()
            size = buf.read_uint()
            gi_seek_size.append([seek, size])

        self.delays = self.loadGAITimes(buf)

        for i in range(frame_count):
            buf.push_pos(gi_seek_size[i][0])
            data = buf.read(gi_seek_size[i][1])
            frame = GAIFrame.from_buffer(Buffer(data))
            buf.pop_pos()

            self.frames.append(frame)

        return self

    def loadGAITimes(self, buf: Buffer) -> list[int]:
        buf.push_pos()

        result: list[int] = []
        pass

        buf.pop_pos()
        return result

    def to_buffer(self, buf: Buffer):
        raise NotImplementedError

    @classmethod
    def from_gai(cls, path: str) -> GAI:
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_gai(self, path: str) -> None:
        with open(path, 'wb') as file:
            file.write(self.to_bytes())
