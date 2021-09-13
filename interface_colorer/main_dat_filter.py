from _1_2 import dat_prefixes

_in = '_dats/Main.txt'
_out = '1_converted/Main.txt'

with open(_in, 'rt') as fp:
    inp = fp.read()

result = ''

# print(dat_prefixes)

for s in inp.split('\n'):
    if '{' in s or '}' in s:
        result += s + '\n'
        continue

    for prefix in dat_prefixes:
        if not prefix.endswith('='):
            prefix = prefix + '='

        if prefix in s:
            result += s + '\n'
            break

with open(_out, 'wt') as fp:
    fp.write(result)
