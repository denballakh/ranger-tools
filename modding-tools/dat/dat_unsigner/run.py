from pathlib import Path

from rangers.dat import check_signed, unsign_data

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.dat'):
    try:
        out_name = _out / filename.relative_to(_in)

        print(f'{filename} -> {out_name}')

        with open(filename, 'rb') as file_in:
            data = file_in.read()

        if check_signed(data):
            unsigned_data = unsign_data(data)
        else:
            print(f'Warning: file {filename!r} is already unsigned!')
            unsigned_data = data

        out_name.parent.mkdir(exist_ok=True, parents=True)

        with open(out_name, 'wb') as file_out:
            file_out.write(unsigned_data)

    except:
        import traceback

        traceback.print_exc()
