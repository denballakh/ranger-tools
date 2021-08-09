import sys
sys.ps1 = ''
sys.ps2 = ''

BYTE = 'byte', 1
WORD = 'word', 2
DWORD = 'dword', 4


field_type = BYTE


init_offset = 0x560
size_in_bytes = 0x990


name = '___'
offset_length = 3
first_field = 'T___ _;'
name_prefix = '_field_'
indent = 4


print(f'struct {name} ' + '{')
print(' ' * indent + first_field)
for i in range(init_offset, size_in_bytes // field_type[1]):
    s = hex(i * field_type[1])[2:].upper()
    s = '0' * (offset_length - len(s)) + s
    print(' ' * indent + f'{field_type[0]} {name_prefix}{s};')
print('};')
