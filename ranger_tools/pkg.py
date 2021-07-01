import io
import zlib
import os

from .common import bytes_to_uint, uint_to_bytes, str_to_bytes, bytes_to_str, check_dir

__all__ = [
    'PKG',
    'PKGItem',
    'MIN_SIZE_TO_COMPRESS',
    'COMPRESS_PNG',
    'COMPRESS_CHUNK_SIZE',
]

MIN_SIZE_TO_COMPRESS = 32
COMPRESS_PNG = False
COMPRESS_CHUNK_SIZE = 2 ** 16
COMPRESS_CHUNK_MAX_SIZE = 2 ** 16 # 64 KB

ZL01_SIGNATURE = 0x31304c5a
ZL02_SIGNATURE = 0x32304c5a

PKG_DATATYPE_RAW = 1
PKG_DATATYPE_ZLIB = 2
PKG_DATATYPE_DIR = 3




class PKGItem:
    def __init__(self):
        self.data = b''
        self.name = ''
        self.type = -1
        self.childs = []
        self.parent = None

    def __repr__(self) -> str:
        s = f'''
        PKGItem:
        Name: {self.name!r}
        Type: {self.type}
        Size: {len(self.data)} b
        Number of childs: {len(self.childs)}
        Childs names: {[child.name for child in self.childs]!r}
        Parent name: {None if self.parent is None else self.parent.name}
        '''
        return s

    @classmethod
    def _compress(cls, data) -> bytes:
        assert 0 < COMPRESS_CHUNK_SIZE <= COMPRESS_CHUNK_MAX_SIZE, f'Invalid COMPRESS_CHUNK_SIZE: {COMPRESS_CHUNK_SIZE}. Should be in range from 1 to {COMPRESS_CHUNK_MAX_SIZE}'
        chunks = []
        stream = io.BytesIO(data)
        while stream.tell() != len(data):
            buf = stream.read(COMPRESS_CHUNK_SIZE)
            chunks.append(buf)
        result = []
        for chunk in chunks:
            comp = zlib.compress(chunk, level=9)
            x = uint_to_bytes(len(comp) + 8) + b'ZL02' + uint_to_bytes(len(chunk)) + comp
            result.append(x)
        result = b''.join(result)
        return result

    @classmethod
    def _decompress(cls, data) -> bytes:
        result = b''
        index = 0
        while index < len(data):
            bufsize = bytes_to_uint(data[index : index + 4])
            index += 4
            buf = data[index : index + bufsize]
            index += bufsize
            assert bytes_to_uint(buf[0 : 4]) in (ZL01_SIGNATURE, ZL02_SIGNATURE), f'Invalid ZL signature: {buf[0 : 4]}'
            result += zlib.decompress(buf[8 :])
        return result

    def decompressed_length(self):
        if self.type == PKG_DATATYPE_ZLIB:
            data = self.data
            result = 0
            index = 0
            while index < len(data):
                bufsize = bytes_to_uint(data[index + 0 : index + 4])
                result += bytes_to_uint(data[index + 8 : index + 12])
                index += 4 + bufsize
            return result

        if self.type == PKG_DATATYPE_RAW:
            return len(self.data)

        if self.type == PKG_DATATYPE_DIR:
            return 0

        raise TypeError(f'Unknown item type: {self.type}')

    def compress(self):
        if self.type == PKG_DATATYPE_RAW:
            if not COMPRESS_PNG and self.name.endswith('.png'): return
            if len(self.data) < MIN_SIZE_TO_COMPRESS: return
            self.data = self._compress(self.data)
            self.type = PKG_DATATYPE_ZLIB

        elif self.type == PKG_DATATYPE_DIR:
            for child in self.childs:
                child.compress()

    def decompress(self):
        if self.type == PKG_DATATYPE_ZLIB:
            self.data = self._decompress(self.data)
            self.type = PKG_DATATYPE_RAW

        elif self.type == PKG_DATATYPE_DIR:
            for child in self.childs:
                child.decompress()

    def copy(self):
        new = PKGItem()
        new.data = self.data
        new.name = self.name
        new.type = self.type
        new.childs = [child.copy() for child in self.childs]
        new.parent = self.parent
        return new

    def size(self):
        if self.type == PKG_DATATYPE_DIR:
            return sum(child.size() for child in self.childs)
        return len(self.data)

    def count(self):
        if self.type == PKG_DATATYPE_DIR:
            return 1 + sum(child.count() for child in self.childs)
        return 1

    def __getitem__(self, key: str):
        assert self.type == PKG_DATATYPE_DIR, f'Cannot get item of non-dir item: {self}'
        if '/' in key:
            key, *child_key = key.split('/')
            child_key = '/'.join(child_key)
        else:
            child_key = ''

        for child in self.childs:
            if child.name == key:
                if child_key:
                    return child[child_key]
                return child

        raise KeyError(f'Invalid key: {key}')

    def full_path(self) -> str:
        result = self.name
        if self.parent:
            result = self.parent.full_path() + result
        if self.type == PKG_DATATYPE_DIR:
            result += '/'
        return result

    def find_in_childs(self, name: str):
        for i, child in enumerate(self.childs):
            if child.name == name:
                return i
        return -1

    def header(self, offsets: dict[str, int]) -> bytes:
        if self.type == PKG_DATATYPE_DIR:
            size = 0
        else:
            size = len(self.data) + 4

        original_size = self.decompressed_length()

        full_path = self.full_path()
        assert full_path in offsets, f'Unknown error while calculating offsets: {offsets}'
        offset = offsets[full_path]

        result = b''
        result += uint_to_bytes(size)
        result += uint_to_bytes(original_size)
        result += str_to_bytes(self.name.upper(), 63)
        result += str_to_bytes(self.name, 63)
        result += uint_to_bytes(self.type)
        result += uint_to_bytes(self.type)
        result += b'\0\0\0\0'
        result += b'\0\0\0\0'
        result += uint_to_bytes(offset)
        result += b'\0\0\0\0'

        return result

    def get_data(self, offset: int, offsets: dict[str, int]):
        result = b''

        if self.type == PKG_DATATYPE_DIR:

            result += b'\xaa\0\0\0' # zero1
            result += uint_to_bytes(len(self.childs))
            result += b'\x9e\0\0\0' # zero2

            for child in self.childs:
                data = child.header(offsets)
                result += data

            for child in self.childs:
                data = child.get_data(offset + len(result), offsets)
                result += data

        else:
            result += uint_to_bytes(len(self.data))
            result += self.data


        return result


    def check_offsets(self, offset: int, offsets: dict[str, int]):
        size = 0
        if self.type == PKG_DATATYPE_DIR:
            size += 12 + len(self.childs) * 158
            offsets[self.full_path()] = offset
            for child in self.childs:
                size += child.check_offsets(offset + size, offsets)
        else:
            offsets[self.full_path()] = offset + size
            size += 4 + len(self.data)
        return size

    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> list['PKGItem']:
        result = []

        index = offset

        index += 4
        items_count = bytes_to_uint(data[index : index + 4]); index += 4
        index += 4

        for i in range(items_count):
            child = PKGItem()
            result.append(child)

            index = offset + 12 + 158 * i

            index += 4
            index += 4
            index += 63
            child.name = bytes_to_str(data[index : index + 63]); index += 63
            child.type = bytes_to_uint(data[index : index + 4]); index += 4
            assert child.type in (PKG_DATATYPE_DIR, PKG_DATATYPE_RAW, PKG_DATATYPE_ZLIB), f'Invalid item type: {child.type}. Should be in {(PKG_DATATYPE_DIR, PKG_DATATYPE_RAW, PKG_DATATYPE_ZLIB)}'
            index += 4
            index += 4
            index += 4
            child_offset = bytes_to_uint(data[index : index + 4]); index += 4
            index += 4

            if child.type == PKG_DATATYPE_DIR:
                child.childs = cls.from_bytes(data, child_offset)
                for child_child in child.childs:
                    child_child.parent = child

            else:
                index = child_offset
                size = bytes_to_uint(data[index : index + 4]); index += 4
                child.data = data[index : index + size]

        return result

    def items_list(self):
        result = []
        for child in self.childs:
            if child.type == PKG_DATATYPE_DIR and child.childs:
                result += child.items_list()
            else:
                result += [child]
        return result


class PKG:
    def __init__(self, root: PKGItem):
        self.root = root

    @classmethod
    def open(cls, filename: str):
        with open(filename, 'rb') as fp:
            data = fp.read()

        root = PKGItem()
        root.type = PKG_DATATYPE_DIR
        root.childs = PKGItem.from_bytes(data, 4)
        for child in root.childs:
            child.parent = root

        return PKG(root)

    def save(self, filename: str):
        root = self.root

        result = b''
        result += uint_to_bytes(4)

        offsets = {}
        root.check_offsets(4, offsets)
        data = root.get_data(4, offsets)
        result += data

        with open(filename, 'wb') as fp:
            fp.write(result)


    @classmethod
    def open_directory(cls, path: str):
        root = PKGItem()
        root.type = PKG_DATATYPE_DIR

        pkg = PKG(root)

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        dirs = [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]

        for file in files:
            filename = os.path.join(path, file)
            with open(filename, 'rb') as fp:
                data = fp.read()

            item = PKGItem()
            item.data = data
            item.name = file
            item.type = PKG_DATATYPE_RAW
            item.childs = []
            item.parent = root
            root.childs.append(item)

        for directory in dirs:
            dirname = os.path.join(path, directory)

            sub_item = cls.open_directory(dirname).root

            item = PKGItem()
            item.data = b''
            item.name = directory
            item.type = PKG_DATATYPE_DIR
            item.childs = sub_item.childs
            for child in item.childs:
                child.parent = item

            item.parent = root
            root.childs.append(item)

        return pkg

    def save_directory(self, path: str):
        self.decompress()
        for item in self.items_list():
            filename = path + '/' + item.full_path()
            check_dir(filename)
            if item.type == PKG_DATATYPE_DIR:
                os.mkdir(filename)
            else:
                with open(filename, 'wb') as fp:
                    fp.write(item.data)


    def size(self): return self.root.size()
    def count(self): return self.root.count()

    def compress(self): self.root.compress()
    def decompress(self): self.root.decompress()
    def copy(self): return self.root.copy()
    def items_list(self): return self.root.items_list()


if __name__ == '__main__':
    # pkg = PKG.open_directory('common/')
    # pkg.save('common.pkg')
    # pkg.compress()
    # pkg.save('common_compressed.pkg')
    # pkg.save_directory('common_extracted/')
    pkg = PKG.open('common.pkg')
    pkg.save('common_compressed.pkg')
    pkg = PKG.open('common_compressed.pkg')
