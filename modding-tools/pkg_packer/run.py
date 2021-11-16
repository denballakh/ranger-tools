from rangers.pkg import PKG
from rangers.common import tree_walker, check_dir, file_rebase, change_ext


_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for folder in tree_walker(_in, root=True)[1]:
    try:
        filename = file_rebase(folder, _in, _out) + '.pkg'

        print(f'{folder} -> {filename}')

        pkg = PKG.from_dir(folder)
        pkg.compress()
        check_dir(filename)
        pkg.to_pkg(filename)

    except Exception as e:
        print(f'Error with folder {folder}: {e!r}')
