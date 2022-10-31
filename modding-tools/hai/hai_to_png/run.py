from pathlib import Path

from rangers.graphics.hai import HAI

_in = Path('_input')
_out = Path('_output')

_in.mkdir(exist_ok=True)
_out.mkdir(exist_ok=True)

for filename in _in.rglob('*.hai'):
    try:
        folder_png = _out / filename.relative_to(_in).with_suffix('')
        folder_png.mkdir(exist_ok=True, parents=True)
        print(f'{filename} -> {folder_png}')
        hai = HAI.from_file(filename)
        hai.to_image_folder(folder_png)

    except:
        import traceback

        traceback.print_exc()
