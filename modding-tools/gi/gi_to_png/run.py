from rangers.graphics.gi import GI
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.gi',))[0]:
    try:
        out_name = change_ext(file_rebase(filename, _in, _out), 'gi', 'png')

        print(f'{filename} -> {out_name}')

        gi = GI.from_gi(filename)
        img = gi.to_image()

        check_dir(out_name)
        img.save(out_name)

    except:
        import traceback

        print(traceback.format_exc())
