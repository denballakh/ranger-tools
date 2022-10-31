from pathlib import Path
import itertools
import subprocess

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for script_src in itertools.chain(_in.rglob('*.rson'), _in.rglob('*.svr')):
    try:
        script_dst = _out / script_src.relative_to(_in).with_suffix('.scr')
        script_text_dst = _out / script_src.relative_to(_in).with_suffix('.txt')
        script_dst.parent.mkdir(parents=True, exist_ok=True)

        print(f'Compiling {script_src.relative_to(_in)!s}...')

        result = subprocess.run(
            [
                'RScript.exe',
                '--cli',
                '--build',
                '--full',
                str(script_src.resolve()),
                str(script_dst.resolve()),
                str(script_text_dst.resolve()),
            ]
        )
        if result.returncode:
            print(f'Cannot compile {script_src!s} file: {result}')

    except:
        import traceback

        traceback.print_exc()
