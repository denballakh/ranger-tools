from pathlib import Path
import json
from pprint import pprint

from rangers.scr import SCR

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for file_scr in _in.rglob('*.scr'):
    try:
        print(file_scr)
        file_json = _out / file_scr.relative_to(_in).with_suffix('.json')
        file_json.parent.mkdir(parents=True, exist_ok=True)
        file_json.write_text(
            json.dumps(SCR.read_bytes(file_scr.read_bytes()), indent=2, ensure_ascii=False),
            encoding='utf-8',
        )

    except:
        import traceback

        traceback.print_exc()
