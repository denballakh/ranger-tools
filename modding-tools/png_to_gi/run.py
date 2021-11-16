from PIL import Image

from rangers.graphics.gi import GI
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.png',))[0]:
    try:
        out_name = change_ext(file_rebase(filename, _in, _out), 'png', 'gi')

        print(f'{filename} -> {out_name}')

        img = Image.open(filename)

        gi = GI.from_image(img, 0, 32)
        check_dir(out_name)
        gi.to_gi(out_name)

    except Exception as e:
        print(f'Error with file {filename}: {e!r}')
