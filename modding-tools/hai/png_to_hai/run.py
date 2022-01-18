from rangers.graphics.hai import HAI
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for folder in tree_walker(_in, root=True)[1]:
    try:
        filename = file_rebase(folder, _in, _out) + '.hai'
        print(f'{folder} -> {filename}')

        hai = HAI.from_image_folder(folder)
        check_dir(filename)
        hai.to_file(filename)

    except:
        import traceback

        print(traceback.format_exc())
