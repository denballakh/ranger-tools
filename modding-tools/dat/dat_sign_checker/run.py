from pathlib import Path

from rangers.dat import check_signed

_in = Path('_input/')
_in.mkdir(exist_ok=True, parents=True)

bad_files = list[Path]()
signed_files = list[Path]()

for filename in _in.rglob('*.dat'):
    print(f'Checking {filename}... ', end='')

    with open(filename, 'rb') as file:
        data = file.read()

    if check_signed(data):
        print('ok')
        signed_files.append(filename)
    else:
        print('err')
        bad_files.append(filename)


print()

if not bad_files:
    print('All files are signed!')

else:
    print('This files are not signed:')
    print('\n'.join(map(str, bad_files)))
    print()
    print('This files are signed:')
    print('\n'.join(map(str, signed_files)))
    print()
