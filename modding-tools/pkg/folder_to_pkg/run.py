from rangers.pkg import PKG
from rangers.common import tree_walker, check_dir, file_rebase

# 0 - без сжатия
# 9 - максимальное сжатие
COMPRESSION = 9

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for folder in tree_walker(_in, root=True)[1]:
    try:
        filename = file_rebase(folder, _in, _out) + '.pkg'

        print(f'{folder} -> {filename}')

        pkg = PKG.from_dir(folder)
        pkg.compress(COMPRESSION)
        check_dir(filename)
        pkg.to_pkg(filename)

    except:
        import traceback

        print(traceback.format_exc())
