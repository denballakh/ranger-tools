import zlib
import os

from ranger_tools.pkg import PKG

_in = '_input'
_out = '_output'

if not os.path.isdir(_in):
    os.mkdir(_in)

if not os.path.isdir(_out):
    os.mkdir(_out)


def convert_ini_to_dict(content: str) -> dict:
    result = {}
    for s in content.split('\n'):
        if not s: continue
        if '=' not in s: continue

        key, val = s.split('=', 1)
        if key in result:
            result[key] += '\n' + val
        else:
            result[key] = val
    return result


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



for file in os.listdir(_in):
    filename = os.path.join(_in, file)
    try:
        if os.path.isfile(filename): continue
        output_name = f'{_out}/{file}.pkg'
        print(f'{filename!r} -> {output_name!r}')

        pkg = PKG.from_dir(filename)
        pkg.compress()
        check_dir(output_name)
        pkg.to_pkg(output_name)

    except Exception as e:
        print(f'Error with file {filename}: {e}')
