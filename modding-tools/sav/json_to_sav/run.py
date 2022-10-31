from pathlib import Path

try:
    from rangers.sav import SAV
except ImportError:
    raise NotImplementedError('no required code') from None

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.json'):
    try:
        out_name = _out / filename.relative_to(_in).with_suffix('.sav')

        print(f'{filename} -> {out_name}')

        sav = SAV.from_json(filename)

        out_name.parent.mkdir(exist_ok=True, parents=True)
        sav.to_file(out_name)
    except:
        import traceback

        traceback.print_exc()
