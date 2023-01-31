'''
Конвертирует .gi-файлы в .png
Запускать его не нужно, использовался только один раз
'''
from pathlib import Path
from rangers.graphics.gi import GI
import shutil

import config

_in = config._0
_out = config._1

def main() -> None:
    for in_file in _in.rglob('**/*'):
        if not in_file.is_file():
            continue

        rel_path = in_file.relative_to(_in)

        if in_file.suffix == '.gi':
            if in_file.stat().st_size == 0:
                continue

            out_file = _out / rel_path.with_suffix('.png')
            if out_file.is_file() and out_file.stat().st_mtime > in_file.stat().st_mtime:
                continue

            gi = GI.from_gi(in_file)

            if gi.header.frame_type not in {0, 2}:
                print(f'Unsupported gi format: {in_file} (frame type: {gi.header.frame_type})')
                continue

            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.touch()
            print(out_file)

            gi.to_image().save(out_file)

            continue

        if in_file.suffix == '.gai':
            if in_file.stat().st_size == 0:
                continue

            print(f'Unsupported extension: {in_file}')

            continue

        if in_file.suffix == '.png':
            if in_file.stat().st_size == 0:
                continue

            out_file = _out / rel_path.with_suffix('.keep_png.png')
            if out_file.is_file() and out_file.stat().st_mtime > in_file.stat().st_mtime:
                continue

            out_file.parent.mkdir(parents=True, exist_ok=True)
            print(out_file)

            shutil.copy(in_file, out_file)

            continue

        print(f'Unsupported extension: {in_file}')


if __name__ == '__main__':
    main()
