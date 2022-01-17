import os
import shutil

from rangers.common import tree_walker

_in = '_input/'
_out = '_output/'

for base, folders, files in os.walk('./'):
    for folder in folders:
        try:
            folder = f'{base}/{folder}'.replace('//', '/')
            print(f'Deleting folder {folder + "/" + _in}...')
            shutil.rmtree(folder + '/' + _in, ignore_errors=True)
            print(f'Deleting folder {folder + "/" + _out}...')
            shutil.rmtree(folder + '/' + _out, ignore_errors=True)

        except:
            import traceback

            print(traceback.format_exc())
