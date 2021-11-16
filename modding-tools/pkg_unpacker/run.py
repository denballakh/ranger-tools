from rangers.pkg import PKG
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.pkg',))[0]:
    try:
        folder = change_ext(file_rebase(filename, _in, _out), '.pkg', '/')

        print(f'{filename} -> {folder}')

        pkg = PKG.from_pkg(filename)
        check_dir(folder)
        pkg.to_dir(folder)



    except Exception as e:
        print(f'Error with file {filename}: {e!r}')

