from pathlib import Path
import json

from rangers.scr import SCR

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for file_json in _in.rglob('*.json'):
    try:
        print(file_json)
        file_scr = _out / file_json.relative_to(_in).with_suffix('.scr')
        file_scr.parent.mkdir(parents=True, exist_ok=True)

        file_scr.write_bytes(SCR.write_bytes(json.loads(file_json.read_text(encoding='utf-8'))))

    except:
        import traceback

        traceback.print_exc()
