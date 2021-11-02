'''
Конвертирует .png-файлы в .gi
Конвертирует .keep_png.png в .png
TODO:
Конвертирует _gai папки в .gai
Конвертирует .txt файлы в .dat
'''
from random import sample
import os
import time

from PIL import Image

from rangers.graphics.gi import GI
from rangers.graphics.gai import GAI
# from rangers.pkg import PKG
# from rangers.dat import DAT

import config

Image.MAX_IMAGE_PIXELS = 4096 ** 2

rewrite = config.rewrite
randomize = config.randomize
PROFILE = config.PROFILE


# Default GI conversion
gi_type = config.gi_type
gi_bit = config.gi_bit

_in = config._2
_out = config._3


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


def process():
    walk = os.walk(_in)
    if randomize:
        walk = list(walk)
        walk = sample(walk, k=len(walk))
    for path, _, files in walk:
        path2 = path.replace(_in, '', 1)

        if path.endswith('_gai'):
            out_name = _out + path2.replace('_gai', '.gai')
            # print(f'{_in + path} -> {out_name}')
            continue
            if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime('/'.join([path, files[0]])): continue

            check_dir(out_name)
            open(out_name, 'wb').close()
            print(out_name)

            frames = []
            for file in files:
                filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
                if not filename.endswith('.png'): continue
                img = Image.open(filename)
                frames.append(img)

            gai = GAI.from_images(frames)
            gai.save(out_name)

            continue

        for file in sample(files, k=len(files)) if randomize else files:
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            if os.stat(filename).st_size == 0: continue

            if filename.endswith('.keep_png.png'):
                out_name = _out + path2 + '/' + file.replace('.keep_png.png', '.png')
                if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime(filename): continue

                check_dir(out_name)
                open(out_name, 'wb').close()
                print(out_name)

                with open(out_name, 'wb') as fout:
                    with open(filename, 'rb') as fin:
                        fout.write(fin.read())

                continue

            if filename.endswith('.png'):
                out_name = _out + f'{path2}/{file.replace(".png", ".gi")}'
                if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime(filename): continue

                check_dir(out_name)
                open(out_name, 'wb').close()
                print(out_name)

                img = Image.open(filename)
                gi = GI.from_image(img, gi_type, gi_bit)
                gi.metadata = f'[[[GI image for mod UIRecolor. Author: denball. ({time.ctime()})]]]'.encode()
                gi.to_gi(out_name)

                continue

            if filename.endswith('.txt'):
                out_name = _out + f'{path2}_{file.replace(".txt", ".txt")}'
                if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime(filename): continue

                check_dir(out_name)
                print(out_name)

                with open(out_name, 'wb') as fout:
                    with open(filename, 'rb') as fin:
                        fout.write(fin.read())

                # out_name = _out + f'{path2}_{file.replace(".txt", ".dat")}'
                # if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime(filename): continue

                # check_dir(out_name)
                # print(out_name)

                # dat = DAT.from_txt(filename)
                # dat.save_txt(out_name)

                continue

            print(f'Unsupported extension: {filename}')


if __name__ == '__main__':
    if PROFILE:
        import cProfile
        import pstats
        import io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

    process()

    if PROFILE:
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.TIME  # CALLS CUMULATIVE FILENAME LINE NAME NFL PCALLS STDNAME TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()

        if not os.path.isdir('logs'):
            try:
                os.mkdir('logs')
            except FileExistsError:
                pass
        with open('logs/time_profiling_2_3.log', 'wt') as file:
            file.write(s.getvalue())
