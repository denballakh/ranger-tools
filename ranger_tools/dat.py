# import zlib
# import time

# from .common import bytes_to_uint, bytes_to_int, bytes_xor, int_to_bytes

# class DAT:
#     pass
    # _seed_xor = b'\xF1\x0B\x97\xBE' # 0xBE970BF1 4f5c0 reload

    # _sr1_key =              b'\x00\x00\x00\x00'
    # _reload_main_key =      b'\xfe\x77\x0a\xc9'
    # _reload_cache_key =     b'\x59\xe6\xfd\x72'
    # _hd_main_key =          b'\x89\xc6\xe8\xb1'
    # _hd_cache_key =         b'\x37\x3f\x8f\xea'

    # @staticmethod
    # def _rand31pm(seed: int) -> int:
    #     while True:
    #         hi, lo = divmod(seed, 0x1f31d)
    #         seed = lo * 0x41a7 - hi * 0xb14
    #         if seed < 1:
    #             seed += 0x7fffffff
    #         yield seed - 1

    # def __init__(self, data: bytes):
    #     content_hash = bytes_to_uint(data[0 : 4])
    #     seed = bytes_to_int(bytes_xor(data[4 : 8], self._hd_main_key))

    #     rnd = self._rand31pm(seed)
    #     content = list(data[8:])
    #     for i in range(len(content)):
    #         content[i] = content[i] ^  (next(rnd) & 0xff)

    #     content = bytes(content)

    #     zl01 = content[0 : 4]
    #     size = bytes_to_uint(content[4 : 8])
    #     buf = content[8 :]
    #     # assert len(buf) == size, (zl01, size, len(buf), buf)

    #     print(buf)
    #     buf = zlib.decompress(buf)
    #     print(buf)

from rangers.blockpar import BlockPar
DAT = BlockPar

if __name__ == '__main__':
    # filename = 'test.dat'
    # with open(filename, 'rb') as fp:
    #     data = fp.read()

    # dat = DAT(data)


    keys = [
        # (-1553446306), # reload lang
        # (-922060802),
        # (-359710921),
        # (594037343),
        # (1225422847),
        # (1787772680),

        # (-1574169504), # hd cache
        # (-359710921),
        # (573314145),
        # (1787772744),

        # (-1310144887), # hd lang
        # (-687146006),
        # (837338762),
        # (1460337643),

        # (-1382362255), # reload cache
        # (-218241448),
        # (765121394),
        # (1929242201),

        # (-2147483633), # sr1
        # (0),

    ]
    # for key in keys:
    #     print(key.to_bytes(4, 'little', signed=True), hex(key))

