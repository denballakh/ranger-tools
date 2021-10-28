"""!
@file
"""

from PIL import Image

from ..io import Buffer
from .gi import GI
from .gai import GAI

__all__ = ['HAI']

# struct HAIHeader
# {
#     uint32_t signature;  //!< Signature
#     uint32_t width;  //!< Animation width
#     uint32_t height;  //!< Animation height
#     uint32_t rowBytes;  //!< Bytes in one line
#     uint32_t count;  //!< Number of frames in animation
#     uint32_t frameSize;  //!< Size of one frame
#     uint32_t unknown1;
#     uint32_t unknown2;
#     uint32_t unknown3;
#     uint32_t unknown4;
#     uint32_t unknown5;
#     uint32_t unknown6;
#     uint32_t palSize;  //!< Size of pallete
# };

class HAIFrame:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f'<HAIFrame: {vars(self)}>'

    @classmethod
    def from_buffer(cls, buf: Buffer) -> 'HAIFrame':
        raise NotImplementedError

    def to_buffer(self, buf: Buffer):
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: bytes):
        buf = Buffer(data)
        return cls.from_buffer(buf)

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return buf.to_bytes()

class HAI:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f'<HAI: {vars(self)}>'

    @classmethod
    def from_buffer(cls, buf: Buffer) -> 'HAI':
        signature = buf.read(4)
        print(f'{signature = }')
        width = buf.read_uint()
        height = buf.read_uint()
        row_bytes = buf.read_uint()
        franes_count = buf.read_uint()
        unknown1 = buf.read_uint(); print(f'{unknown1 = }')
        unknown2 = buf.read_uint(); print(f'{unknown2 = }')
        unknown3 = buf.read_uint(); print(f'{unknown3 = }')
        unknown4 = buf.read_uint(); print(f'{unknown4 = }')
        unknown5 = buf.read_uint(); print(f'{unknown5 = }')
        unknown6 = buf.read_uint(); print(f'{unknown6 = }')
        pallete_size = buf.read_uint()

        raise NotImplementedError

    def to_buffer(self, buf: Buffer):
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: bytes):
        buf = Buffer(data)
        return cls.from_buffer(buf)

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return buf.to_bytes()

    @classmethod
    def from_hai(cls, path: str):
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_hai(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())
