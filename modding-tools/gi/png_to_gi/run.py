from pathlib import Path

from PIL import Image

from rangers.graphics.gi import GI

# 0 - один слой, 32 (с альфой) или 16 бит (без альфы)
# 1 -
# 2 - три слоя, 16 бит с альфой
# 3 -
# 4 -
TYPE = 0

# имеет значение только для TYPE=0
BIT_DEPTH = 32

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)

for filename in _in.rglob('*.png'):
    try:
        out_name = _out / filename.relative_to(_in).with_suffix('.gi')

        print(f'{filename} -> {out_name}')

        img = Image.open(filename)

        gi = GI.from_image(img, TYPE, BIT_DEPTH)
        out_name.parent.mkdir(exist_ok=True, parents=True)
        gi.to_gi(out_name)

    except:
        import traceback

        traceback.print_exc()
