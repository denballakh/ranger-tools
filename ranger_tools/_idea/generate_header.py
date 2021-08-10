import sys
sys.ps1 = ''
sys.ps2 = ''

GAP = '_gap', 1
GAP_32 = '_gap_32', 4
BYTE = 'byte', 1
WORD = 'word', 2
DWORD = 'dword', 4


field_type = GAP_32


init_offset = 0x4
size_in_bytes = 0x4c


name = '__struct_name__'
offset_length = 2
first_field = '__cls* cls;'
name_prefix = '_'
indent = 4


print(f'struct {name} ' + '{')
print(' ' * indent + first_field)
for i in range(init_offset // field_type[1], size_in_bytes // field_type[1]):
    s = hex(i * field_type[1])[2:].upper()
    s = '0' * (offset_length - len(s)) + s
    print(' ' * indent + f'{field_type[0]} {name_prefix}{s};')
print('};')
