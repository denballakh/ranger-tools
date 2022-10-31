from pathlib import Path

from rangers.robotcomplate import RC

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.json'):
    try:
        out_name = _out / filename.relative_to(_in).with_suffix('.dat')

        print(f'{filename} -> {out_name}')

        rc = RC.from_json(filename)
        out_name.parent.mkdir(exist_ok=True, parents=True)
        rc.to_file(out_name)

    except:
        import traceback

        traceback.print_exc()
