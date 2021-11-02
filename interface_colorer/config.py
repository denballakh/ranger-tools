__all__ = [
    'PROFILE',
    'randomize',
    'rewrite',

    '_0', '_1', '_2', '_3', '_4',

    '_dats',
    'modified_file_delta',
    'dat_rule_mod',
    'modified_rules',
    'dat_file',

    'gi_type',
    'gi_bit',

    'COMPRESS_PKG',

]

PROFILE = True
randomize = False
rewrite = False

_dats = '_dats/'
_0 = '0_orig/'
_1 = '1_converted/'
_2 = '2_colored/'
_3 = '3_result/'
_4 = '4_output/'

modified_file_delta = 3600  # s
dat_rule_mod = False
modified_rules: list[str] = []
dat_file = 'Main.txt'

gi_type = 2
gi_bit = 16

COMPRESS_PKG = False
