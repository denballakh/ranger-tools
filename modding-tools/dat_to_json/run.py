from rangers.dat import DAT
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.dat',))[0]:
    try:
        output_name = change_ext(file_rebase(filename, _in, _out), '.dat', '.txt')

        print(f'{filename} -> {output_name}')

        dat = DAT.from_dat(filename)
        check_dir(output_name)
        dat.to_json(output_name)

    except:
        import traceback

        print(traceback.format_exc())
