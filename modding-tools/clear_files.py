import shutil

from rangers.common import tree_walker

_in = '_input/'
_out = '_output/'

for folder in tree_walker('./', root=True)[1]:
    try:
        print(f'Deleting folder {folder + "/" + _in}...')
        shutil.rmtree(folder + '/' + _in, ignore_errors=True)
        print(f'Deleting folder {folder + "/" + _out}...')
        shutil.rmtree(folder + '/' + _out, ignore_errors=True)

    except:
        import traceback

        print(traceback.format_exc())
