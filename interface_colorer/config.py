from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = 4096**2

PROFILE = False
randomize = False
rewrite = False

_dats = Path('_dats/')
_0 = Path('0_orig/')
_1 = Path('1_converted/')
_2 = Path('2_colored/')
_3 = Path('3_result/')
_4 = Path('4_output/')
_override = Path('override/')

modified_file_delta = 3600  # s
dat_rule_mod = False
modified_rules: list[str] = []
dat_file = Path('Main.txt')

gi_type = 2
gi_bit = 16
dither = False

COMPRESS_PKG = True
