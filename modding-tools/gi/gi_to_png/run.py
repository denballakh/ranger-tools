from pathlib import Path

from rangers.graphics.gi import GI

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.gi'):
    try:
        out_name = _out / filename.relative_to(_in).with_suffix('.png')

        print(f'{filename} -> {out_name}')

        gi = GI.from_gi(filename)
        img = gi.to_image()

        out_name.parent.mkdir(exist_ok=True, parents=True)
        img.save(out_name)

    except:
        import traceback

        traceback.print_exc()
