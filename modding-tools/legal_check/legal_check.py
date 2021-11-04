import zlib
import os

_in = '_input'

if not os.path.isdir(_in):
    os.mkdir(_in)

bad_files: list[str] = []
signed_files: list[str] = []

try:
    exec(zlib.decompress(open('obfuscated_code', 'rb').read()).decode())
except FileNotFoundError as e:
    print(f'No required code')
    raise

for path, _, files in os.walk(_in):
    path2 = path.replace(_in, '', 1).replace('\\', '/').replace('//', '/')

    for filen in files:
        filename: str = '/'.join([path, filen]).replace('\\', '/').replace('//', '/')

        if filename.endswith('.dat'):

            print(f'Checking {filename}... ', end='')

            with open(filename, 'rb') as file:
                data = file.read()

            if is_signed(data):
                print('ok')
                signed_files.append(filename)
            else:
                print('error!')
                bad_files.append(filename)

print()

if not bad_files:
    print('All files are signed!')

else:
    print('This files are not signed:')
    print('\n'.join(bad_files))
    print()
    print('This files are signed:')
    print('\n'.join(signed_files))
    print()

