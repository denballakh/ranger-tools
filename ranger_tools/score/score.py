import zlib

from ..io import Buffer

__all__ = [
    'SCORE',
]

class SCORE:
    pass


def _rand31pm(seed: int) -> int:
    while True:
        hi, lo = divmod(seed, 0x1f31d)
        seed = lo * 0x41a7 - hi * 0xb14
        if seed < 1:
            seed += 0x7fffffff
        yield seed - 1

def decipher(data: bytes, key: int) -> bytes:
    din = Buffer(data)
    rnd = _rand31pm(key)
    dout = Buffer()
    while not din.end():
        dout.write_byte(din.read_byte() ^  (next(rnd) & 0xff))
    result = dout.to_bytes()
    return result

def magic(content):
    data = b''
    content = content.split('*************** Protect database ****************')[-1]
    content = ''.join([c for c in content if c in '0123456789ABCDEF'])
    while content:
        b, content = content[:2], content[2:]
        data += eval(f'b"\\x{b}"')
    buf = Buffer(data)
    _three = buf.read_int()
    assert _three == 3, _three
    key_xored = buf.read_int()
    unknown1 = buf.read_uint()
    unknown2 = buf.read_uint()
    print(f'unknown1 = {hex(unknown1)}')
    print(f'unknown2 = {hex(unknown2)}')
    key = key_xored ^ 0x140F3F9B
    assert key in range(0, 2000000000), key
    data = decipher(buf.read(), key)
    buf = Buffer(data)
    zl01 = buf.read(4)
    assert zl01 ==b'ZL01', zl01
    decompressed_size = buf.read_uint()
    data = buf.read()
    data = zlib.decompress(data)
    assert decompressed_size == len(data), (decompressed_size, len(data))
    return data

def load_score(score_name: str) -> SCORE:
    with open(score_name, 'rt') as file:
        buf = Buffer(magic(file.read()))

    # 1175 - длительность партии

    version = buf.read_uint()
    print('version =', version, {0xcc: '(reload)', 0xcd: '(hd)'}[version])
    byte_00 = buf.read_byte()
    print(f'{byte_00 = }')

    difflevels = []
    for i in range(8):
        diff = buf.read_byte()
        difflevels.append(diff)
    print(f'{difflevels = }')
    assert buf.pos == 13, buf.pos
    name = buf.read_wstr(); print(f'{name = }')
    byte_0 = buf.read_byte(); print(f'{byte_0 = }')
    byte_1 = buf.read_byte(); print(f'{byte_1 = }')
    dword_0 = buf.read_uint(); print(f'{dword_0 = }')
    byte_2 = buf.read_byte(); print(f'{byte_2 = }')

    pirates_killed = buf.read_word(); print(f'{pirates_killed = }')
    transports_killed = buf.read_word(); print(f'{transports_killed = }')
    dominators_killed = buf.read_word(); print(f'{dominators_killed = }')
    system_captured = buf.read_word(); print(f'{system_captured = }')
    word_4 = buf.read_word(); print(f'{word_4 = }')

    dword_1 = buf.read_uint(); print(f'{dword_1 = }')
    dword_2 = buf.read_uint(); print(f'{dword_2 = }')

    values_1 = []
    for i in range(dword_2):
        val = buf.read_byte()
        values_1.append(val)
        # print(f'value_{i} = {val}')
    print(f'{values_1 = }')
    free_points = buf.read_uint(); print(f'{free_points = }')

    assert buf.pos == 69, buf.pos
    skills = []
    for i in range(6):
        sk = buf.read_byte()
        skills.append(sk)
        # print(f'skill_{i} = {sk}')
    print(f'{skills = }')

    byte_3 = buf.read_byte(); print(f'{byte_3 = }')
    # byte_3 = buf.read_byte(); print(f'{byte_3 = }')

    dword_4 = buf.read_uint(); print(f'{dword_4 = }')
    data_0 = buf.read(dword_4); print('data_0 =', data_0[:100], ',', len(data_0))

    galaxy_id = buf.read_uint(); print(f'{galaxy_id = } (not sure)') # galaxy_id

    # byte_4 = buf.read_byte(); print(f'{byte_4 = }')

    dword_6 = buf.read_word(); print(f'{dword_6 = }')
    data_1 = buf.read(dword_6); print('data_1 =', data_1[:100], ',', len(data_1))

    dword_7 = buf.read_uint(); print(f'{dword_7 = }')


    dword_8 = buf.read_word(); print(f'{dword_8 = }')
    data_2 = buf.read(dword_8 * 3); print('data_2 =', data_2[:100], ',', len(data_2))

    dword_9 = buf.read_uint(); print(f'{dword_9 = }')

    byte_4 = buf.read_byte(); print(f'{byte_4 = }')
    byte_5 = buf.read_byte(); print(f'{byte_5 = }')
    byte_6 = buf.read_byte(); print(f'{byte_6 = }')


    dword_10 = buf.read_word(); print(f'{dword_10 = }')
    data_3 = buf.read(); print('data_3 =', data_3[:100], ',', len(data_3))




    _='''
    \xcd - version
    \0 - v4byte - ?

    \0
    \0
    \1
    \0
    \1
    \2
    \3
    \0

    \0 \0
    \0 \x13
    \4 @
    \4 5
    \4 D
    \4 \0
    \0 \0

    \4
    \x0e
    \2\0\0\0
    \0
    \0\0
    \0\0
    \0\0
    \0\0
    \0\0

    \0\0\0\0
    \0\0\0\0
    \0\0\0\0
    \0\0\1\0\0\0,

    \0\0\0\0 - dword3

    \0 - skills
    \0
    \1
    \1
    \0
    \0
    '''
