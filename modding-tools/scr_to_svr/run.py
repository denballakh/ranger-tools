from rangers.rscript.scr import SCR
from rangers.rscript.converter import scr_to_svr
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input'
_out = '_output'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.scr',))[0]:
    try:
        out_name = change_ext(file_rebase(filename, _in, _out), 'scr', 'svr')

        print(f'{filename} -> {out_name}')

        scr = SCR.from_scr(filename)
        svr = scr_to_svr(scr)
        check_dir(out_name)
        svr.to_svr(out_name)


    except Exception as e:
        print(f'Error with file {filename}: {e!r}')
