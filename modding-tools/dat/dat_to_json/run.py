from pathlib import Path

from rangers.dat import DAT

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.dat'):
    try:
        out_name = _out / filename.relative_to(_in).with_suffix('.json')

        print(f'{filename} -> {out_name}')

        dat = DAT.from_dat(filename)
        out_name.parent.mkdir(exist_ok=True, parents=True)
        dat.to_json(out_name)

    except:
        import traceback

        traceback.print_exc()
