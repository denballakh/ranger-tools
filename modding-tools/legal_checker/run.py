from rangers.dat import DAT_SIGN_AVAILABLE, check_signed
from rangers.common import tree_walker, check_dir

if not DAT_SIGN_AVAILABLE:
    raise NotImplementedError('no required code')

_in = '_input/'

bad_files = list[str]()
signed_files = list[str]()

check_dir(_in)

for filename in tree_walker(_in, exts=('.dat',))[0]:
    print(f'Checking {filename + "...":70} ', end='')

    with open(filename, 'rb') as file:
        data = file.read()

    if check_signed(data):
        print('ok')
        signed_files.append(filename)
    else:
        print('ERROR!')
        bad_files.append(filename)


print()

if not bad_files:
    print('All files are signed!')

else:
    print('This files are not signed:')
    print('\n'.join(bad_files))
    print()
    print('This files are signed:')
    print('\n'.join(signed_files))
    print()
