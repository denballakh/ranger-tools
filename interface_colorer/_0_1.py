'''
Конвертирует .gi-файлы в .png
Запускать его не нужно, использовался только один раз
'''
from PIL import Image
from random import sample
import os

from ranger_tools.graphics.gi import GI

randomize = False

Image.MAX_IMAGE_PIXELS = 4096 ** 2

rewrite = False
PROFILE = False

_in = '0_orig/'
_out = '1_converted/'


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

        for file in sample(files, k=len(files)) if randomize else files:
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            if filename.endswith('.gi'):
                if os.stat(filename).st_size == 0: continue

                out_name = _out + f'{path2}/{file.replace(".gi", ".png")}'
                if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime(filename): continue

                gi = GI.from_gi(filename)

                # if gi.header.frame_type == 1:
                #     gi.header.frame_type = 0

                if gi.header.frame_type not in (0, 2):
                    print(f'Unsupported gi format: {filename} (frame type: {gi.header.frame_type})')

                    continue

                check_dir(out_name)
                open(out_name, 'wb').close()
                print(out_name)

                img = gi.to_image()
                img.save(out_name)

                continue

            if filename.endswith('.gai'):
                if os.stat(filename).st_size == 0: continue
                print(f'Unsupported extension: {filename}')

                continue

            if filename.endswith('.png'):
                if os.stat(filename).st_size == 0: continue

                out_name = _out + f'{path2}/{file.replace(".png", ".keep_png.png")}'
                if not rewrite and os.path.isfile(out_name) and os.path.getmtime(out_name) > os.path.getmtime(filename): continue

                check_dir(out_name)
                open(out_name, 'wb').close()
                print(out_name)

                with open(out_name, 'wb') as fout:
                    with open(filename, 'rb') as fin:
                        fout.write(fin.read())

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
        with open('logs/time_profiling_0_1.log', 'wt') as file:
            file.write(s.getvalue())
