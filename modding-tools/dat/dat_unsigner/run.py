from rangers.dat import DAT_SIGN_AVAILABLE, check_signed, unsign_data
from rangers.common import tree_walker, check_dir, file_rebase

if not DAT_SIGN_AVAILABLE:
    print('Warning! Cannot check dat sign')
    print()

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

        if DAT_SIGN_AVAILABLE:
            if check_signed(data):
                unsigned_data = unsign_data(data)
            else:
                print(f'Warning: file {filename!r} is already unsigned!')
                unsigned_data = data

        else:
            unsigned_data = data[8:]

        check_dir(out_name)

        with open(out_name, 'wb') as file_out:
            file_out.write(unsigned_data)

    except:
        import traceback

        print(traceback.format_exc())
