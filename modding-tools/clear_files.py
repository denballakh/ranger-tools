import shutil

from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = 'input/'
_out = 'output/'

for folder in tree_walker('./', root=True)[1]:
    try:
        print(f'Deleting folder {folder + "/" + _in}...')
        shutil.rmtree(folder + '/' + _in, ignore_errors=True)
        print(f'Deleting folder {folder + "/" + _out}...')
        shutil.rmtree(folder + '/' + _out, ignore_errors=True)

    except Exception as e:
        print(f'Error with folder {folder}: {e!r}')
