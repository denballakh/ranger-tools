from pathlib import Path

from rangers.qm import QM, VER_QMM

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.json'):
    try:
        qm = QM.from_json(filename)
        ext = '.qmm' if qm.data['version'] in VER_QMM else '.qm'
        out_name = _out / filename.relative_to(_in).with_suffix('.json')
        print(f'{filename} -> {out_name}')
        out_name.parent.mkdir(exist_ok=True, parents=True)
        qm.to_file(out_name)

    except:
        import traceback

        traceback.print_exc()
