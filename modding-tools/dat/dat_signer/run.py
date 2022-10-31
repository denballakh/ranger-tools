from pathlib import Path

from rangers.dat import DAT_SIGN_AVAILABLE, check_signed, get_sign

if not DAT_SIGN_AVAILABLE:
    raise NotImplementedError('no required code')

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
            print(f'Warning: file {filename!r} is already signed!')
            signed_data = data
        else:
            signed_data = get_sign(data) + data

        out_name.parent.mkdir(exist_ok=True, parents=True)

        with open(out_name, 'wb') as file_out:
            file_out.write(signed_data)

    except:
        import traceback

        traceback.print_exc()
