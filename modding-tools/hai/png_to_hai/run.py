from pathlib import Path

from rangers.graphics.hai import HAI

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for folder in _in.rglob('*/'):
    try:
        filename = _out / folder.relative_to(_in).with_suffix('.hai')
        print(f'{folder} -> {filename}')

        hai = HAI.from_image_folder(folder)
        filename.parent.mkdir(exist_ok=True, parents=True)
        hai.to_file(filename)

    except:
        import traceback

        traceback.print_exc()
