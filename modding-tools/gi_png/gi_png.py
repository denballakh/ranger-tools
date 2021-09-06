import zlib
import os
from PIL import Image

from ranger_tools.graphics.gi import GI

_in = '_input'
_out = '_output'

if not os.path.isdir(_in):
    os.mkdir(_in)

if not os.path.isdir(_out):
    os.mkdir(_out)

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
    path2 = path.replace(_in, '', 1).replace('//', '/').replace('\\', '/')

    for file in files:
        filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
        try:
            if filename.endswith('.gi'):
                out_name = f'{_out}{path2}/{file.replace(".gi", ".png")}'

                print(f'{filename} -> {out_name}')

                # img = Image.open(filename)

                # gi = GI.from_image(img, 0, 32)
                # check_dir(out_name)
                # gi.to_gi(out_name)


                gi = GI.from_gi(filename)
                img = gi.to_image()

                check_dir(out_name)
                img.save(out_name)



        except Exception as e:
            print(f'Error with file {filename}: {e}')

