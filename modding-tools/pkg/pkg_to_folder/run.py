from pathlib import Path

from rangers.pkg import PKG

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.pkg'):
    try:
        folder = _out / filename.relative_to(_in).with_suffix('')

        print(f'{filename} -> {folder}')
        try:
            pkg = PKG.from_file(filename)
        except Exception:
            pkg = PKG.from_file(filename, sr1=True)

        folder.mkdir(exist_ok=True, parents=True)
        pkg.to_folder(folder)

    except:
        import traceback

        traceback.print_exc()
