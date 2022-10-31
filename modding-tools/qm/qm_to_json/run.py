import itertools
from pathlib import Path

from rangers.qm import QM, VER_QMM

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in itertools.chain(_in.rglob('*.qm'), _in.rglob('*.qmm')):
    try:
        qm = QM.from_file(filename)
        ext = '.qmm' if qm.data['version'] in VER_QMM else '.qm'
        out_name = _out / filename.relative_to(_in).with_suffix('.json')
        print(f'{filename} -> {out_name}')
        out_name.parent.mkdir(exist_ok=True, parents=True)
        qm.to_json(out_name)

    except:
        import traceback

        traceback.print_exc()
