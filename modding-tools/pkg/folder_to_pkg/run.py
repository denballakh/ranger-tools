from pathlib import Path

from rangers.pkg import PKG

# 0 - без сжатия
# 9 - максимальное сжатие
COMPRESSION = 9

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for folder in _in.rglob('*/'):
    try:
        filename = _out / folder.relative_to(_in).with_suffix('.pkg')

        print(f'{folder} -> {filename}')

        pkg = PKG.from_folder(folder)
        pkg.compress(COMPRESSION)
        filename.parent.mkdir(exist_ok=True, parents=True)
        pkg.to_file(filename)

    except:
        import traceback

        traceback.print_exc()
