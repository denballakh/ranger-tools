import zlib
import os

_in = '_input'
_out = '_output'

if not os.path.isdir(_in):
    os.mkdir(_in)

if not os.path.isdir(_out):
    os.mkdir(_out)
try:
    exec(zlib.decompress(open('obfuscated_code', 'rb').read()).decode())
except FileNotFoundError as e:
    print(f'No required code')
    raise


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

for path, _, files in os.walk(_in):
    path2 = path.replace(_in, '', 1).replace('\\', '/').replace('//', '/')

    for file in files:
        filename: str = '/'.join([path, file]).replace('\\', '/').replace('//', '/')
        try:
            if filename.endswith('.dat'):
                out_name = f'{_out}{path2}/{file}'

                print(f'{filename} -> {out_name}')

                with open(filename, 'rb') as file:
                    data = file.read()

                if is_signed(data):
                    print(f'Warning: file {filename!r} is already signed!')
                    signed_data = data
                else:
                    signed_data = sign(data) + data

                check_dir(out_name)

                with open(out_name, 'wb') as file:
                    file.write(signed_data)



        except Exception as e:
            print(f'Error with file {filename}: {e}')


