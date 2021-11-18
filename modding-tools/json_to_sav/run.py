try:
    from rangers.sav import SAV
except ImportError:
    raise NotImplementedError('no required code') from None

from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.json',))[0]:
    try:
        out_name = change_ext(file_rebase(filename, _in, _out), 'json', 'sav')

        print(f'{filename} -> {out_name}')

        sav = SAV.from_json(filename)

        check_dir(out_name)
        sav.to_file(out_name)
    except:
        import traceback

        print(traceback.format_exc())
