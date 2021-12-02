from rangers.robotcomplate import RC
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.json',))[0]:
    try:
        out_name = change_ext(file_rebase(filename, _in, _out), 'json', 'dat')

        print(f'{filename} -> {out_name}')

        rc = RC.from_json(filename)
        check_dir(out_name)
        rc.to_file(out_name)

    except:
        import traceback

        print(traceback.format_exc())
