'''
Конвертирует .png-файлы в .gi
Конвертирует .keep_png.png в .png
Копирует датники
TODO:
Конвертирует _gai папки в .gai
'''
import time
import shutil

from PIL import Image

from rangers.graphics.gi import GI


import config

Image.MAX_IMAGE_PIXELS = 4096**2


# Default GI conversion
gi_type = config.gi_type
gi_bit = config.gi_bit
dither = config.dither

_in = config._2
_out = config._3


def main() -> None:
    for in_dir in _in.rglob('**/*'):
        if not in_dir.is_dir():
            continue
        rel_path = in_dir.relative_to(_in)

        if in_dir.stem.endswith('_gai'):
            out_file = _out / rel_path.with_stem(rel_path.stem.replace('_gai', '.gai'))
            # print(f'{_in + path} -> {out_name}')
            continue
            # if (
            #     out_name.is_file()
            #     and out_name.stat().st_mtime > os.path.getmtime('/'.join([path, files[0]]))
            # ):
            #     continue

            # check_dir(out_name)
            # open(out_name, 'wb').close()
            # print(out_name)

            # frames = []
            # for file in files:
            #     filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            #     if not filename.endswith('.png'):
            #         continue
            #     img = Image.open(filename)
            #     frames.append(img)

            # gai = GAI.from_images(frames)
            # gai.save(out_name)

            # continue


    for in_file in _in.rglob('**/*'):
        rel_path = in_file.relative_to(_in)
        if not in_file.is_file():
            continue

        if in_file.parent.stem.endswith('_gai'):
            continue

        if in_file.stat().st_size == 0:
            continue

        if in_file.name.endswith('.keep_png.png'):
            out_file = _out / rel_path.with_name(rel_path.name.replace('.keep_png.png', '.png'))
            if (
                out_file.is_file()
                and out_file.stat().st_mtime > in_file.stat().st_mtime
            ):
                continue

            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.touch()
            print(out_file)

            shutil.copy(in_file, out_file)

            continue

        if in_file.suffix == '.png':
            out_file = _out / rel_path.with_name(rel_path.name.replace('.32bit.','.')).with_suffix('.gi')
            #f'{path2}/{file.replace(".png", ".gi").replace(".32bit.",".")}'

            if (
                out_file.is_file()
                and out_file.stat().st_mtime > in_file.stat().st_mtime
            ):
                continue

            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.touch()
            print(out_file)

            img = Image.open(in_file)
            if in_file.stem.endswith('.32bit'):
                # gi = GI.from_image(img, 0, 32)
                # gi = GI.from_image(img, 0, 32)
                print(f'Warning! 32-bit image: {in_file}')
                gi = GI.from_image(img, gi_type, gi_bit)
            else:
                gi = GI.from_image(img, gi_type, gi_bit)
            gi.metadata = (
                f'[[[GI image for mod DenUIRecolor. Author: denball. ({time.ctime()})]]]'.encode()
            )
            gi.to_gi(out_file)

            continue

        if in_file.suffix ==  '.txt':
            out_file = _out / rel_path.parent.parent / f'{rel_path.parent.name}_{rel_path.name}'
            # f'{}_{file.replace(".txt", ".txt")}'
            if (
                out_file.is_file()
                and out_file.stat().st_mtime > in_file.stat().st_mtime
            ):
                continue

            out_file.parent.mkdir(parents=True, exist_ok=True)
            print(out_file)

            shutil.copy(in_file, out_file)

            # out_name = _out + f'{path2}_{file.replace(".txt", ".dat")}'
            # if os.path.isfile(out_name) and out_name.stat().st_mtime > filename.stat().st_mtime: continue

            # check_dir(out_name)
            # print(out_name)

            # dat = DAT.from_txt(filename)
            # dat.save_txt(out_name)

            continue

        print(f'Unsupported extension: {in_file}')

    shutil.copytree(config._override / config._3, config._3, dirs_exist_ok=True)


if __name__ == '__main__':
    main()
