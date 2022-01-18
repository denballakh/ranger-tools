from rangers.graphics.hai import HAI
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.hai'))[0]:
    try:
        output_name = change_ext(file_rebase(filename, _in, _out), '.hai', '/')
        print(f'{filename} -> {output_name}')
        hai = HAI.from_file(filename)
        check_dir(output_name)
        hai.to_image_folder(output_name)

    except:
        import traceback

        print(traceback.format_exc())
