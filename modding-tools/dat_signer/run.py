from rangers.dat import DAT_SIGN_AVAILABLE, check_signed, get_sign
from rangers.common import tree_walker, check_dir, file_rebase

if not DAT_SIGN_AVAILABLE:
    raise NotImplementedError('no required code')

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.dat',))[0]:
    try:
        out_name = file_rebase(filename, _in, _out)

        print(f'{filename} -> {out_name}')

        with open(filename, 'rb') as file_in:
            data = file_in.read()

        if check_signed(data):
            print(f'Warning: file {filename!r} is already signed!')
            signed_data = data
        else:
            signed_data = get_sign(data) + data

        check_dir(out_name)

        with open(out_name, 'wb') as file_out:
            file_out.write(signed_data)

    except:
        import traceback

        print(traceback.format_exc())
