from PIL import Image

from rangers.graphics.gi import GI
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

# 0 - один слой, 32 (с альфой) или 16 бит (без альфы)
# 1 -
# 2 - три слоя, 16 бит с альфой
# 3 -
# 4 -
TYPE = 0

# имеет значение только для TYPE=0
BIT_DEPTH = 32

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.png',))[0]:
    try:
        out_name = change_ext(file_rebase(filename, _in, _out), 'png', 'gi')

        print(f'{filename} -> {out_name}')

        img = Image.open(filename)

        gi = GI.from_image(img, TYPE, BIT_DEPTH)
        check_dir(out_name)
        gi.to_gi(out_name)

    except:
        import traceback

        print(traceback.format_exc())
