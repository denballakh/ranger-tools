"""!
@file
"""

import os
import sys
from time import time
import argparse
from pathlib import Path
import shutil as sh

# import rangers
# import rangers.modding

logger = ...

CODE_OK = 0
CODE_ERR = 1

parser = argparse.ArgumentParser(
    prog='python -m rangers',
    description='Ranger-tools file converter',
    formatter_class=argparse.RawTextHelpFormatter,
)

subparsers = parser.add_subparsers(dest='cmd', required=True)


dat_parser = subparsers.add_parser(
    'dat',
    help='Converting, merging and signing .dat files',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:

    ''',
)

dat_parser.add_argument(
    '-s',
    '--sign',
    action='store_true',
    help='Sign .dat file',
)
dat_parser.add_argument(
    '-f',
    '--format',
    metavar='FMT',
    action='store',
    choices=['SR1', 'ReloadMain', 'ReloadCache', 'HDMain', 'HDCache'],
    default='HDMain',
    help='Version of .dat file',
)

dat_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input file(s)',
)
dat_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output file',
)


# parser = argparse.ArgumentParser(description='Tool for ')
# parser.add_argument('inputs', metavar='F', type=str, nargs='+',
#                    help='input file')
# parser.add_argument('output', metavar='O', type=str,
#                    help='output file')

# parser.add_argument('-c', '--cache', dest='cache', action='store_true',
#                    help='output is cachedata')
# parser.add_argument('-t', '--type', dest='type', action='store', choices=['sr1', 'reload', 'hd'], default='hd',
#                    help='type of output dat')
# parser.add_argument('-s', '--sign', dest='sign', action='store_true',
#                    help='sign result dat')


pkg_parser = subparsers.add_parser(
    'pkg',
    help='Packing, unpacking .pkg files',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:
    Pack scripts and dats in folder dir into package.pkg without compression:
        pkg -e dat -e scr -c=0 dir/ package.pkg
    Unpack package.pkg into folder dir:
        pkg package.pkg dir/
    ''',
)

pkg_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input path/file(s)',
)
pkg_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output path/file or * to print .pkg to console',
)

pkg_parser.add_argument(
    '-c',
    '--compression',
    metavar='CMPLVL',
    action='store',
    type=int,
    choices=range(-1, 10),
    default=-1,
    help='Compression level (-1 - default (=9), 0 - min, 9 - max)',
)
pkg_parser.add_argument(
    '-m',
    '--metadata',
    action='store',
    type=str,
    default='',
    help='String to include to .pkg metadata',
)
pkg_parser.add_argument(
    '-e',
    '--extensions',
    action='append',
    type=str,
    default=[],
    help='List of file extensions to pack',
)


gi_parser = subparsers.add_parser(
    'gi',
    help='Converting .gi files',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:

    ''',
)

gi_parser.add_argument(
    '-f',
    '--format',
    action='store',
    type=str,
    choices=['0_16', '0_32', '2'],
    default='2',
    help='File format '
    '(0_16 - one layer 16 bit RGB; '
    '0_32 - one layer 32 bit RGBA; '
    '2 - three layers RGBA)',
)

gi_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input path/file(s)',
)
gi_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output path/file',
)


gai_parser = subparsers.add_parser(
    'gai',
    help='Converting .gai files',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:

    ''',
)

gai_parser.add_argument(
    '-f',
    '--format',
    action='store',
    type=int,
    help='File format',
)

gai_parser.add_argument(
    '-c',
    '--compression',
    metavar='CMPLVL',
    action='store',
    type=int,
    choices=range(-1, 10),
    default=None,
    help='Compression level (-1 - default (=9), 0 - min, 9 - max)',
)

gai_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input path/file(s)',
)
gai_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output path/file',
)


script_parser = subparsers.add_parser(
    'script',
    help='Converting .scr files',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:

    ''',
)

script_parser.add_argument(
    '-t',
    '--text',
    action='store',
    type=str,
)

script_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input file',
)
script_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output file',
)


save_parser = subparsers.add_parser(
    'save',
    help='Converting .sav files',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:
    save TurnSave.sav TurnSave.json
    save TurnSave.json TurnSave.sav
    ''',
)

save_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input file',
)
save_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output file',
)


score_parser = subparsers.add_parser(
    'score',
    help='Converting score files (ToServerXX.txt) to JSON [and back]',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''example:
    score ToServer01.txt ToServer01.json
    score ToServer01.json ToServer01.txt
    ''',
)

score_parser.add_argument(
    'input',
    action='store',
    type=str,
    help='Input file',
)
score_parser.add_argument(
    'output',
    action='store',
    type=str,
    help='Output file',
)


def process_dat(args):
    return CODE_ERR


def process_pkg(args):
    from rangers.pkg import PKG

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.exists() and input_path.is_file():
        if input_path.suffix != '.pkg':
            print(f'Warning: invalid extension: {input_path.suffix}')

        if str(output_path) == '*':
            from rangers.common import sizeof_fmt

            def print_pkg_item(item, indent=''):
                i = indent
                print(i+f'{item.full_path()}')
                # print(i+f'  Name: {item.name!r}')
                # print(i+f'  Type: {["raw file", "compressed file", "directory"][item.type - 1]}')
                if item.type==3:
                    print(i+f'  Number of childs: {len(item.childs)}')
                    # print(i+f'  Childs names: {[child.name for child in item.childs]!r}')
                else:
                    print(i+f'  Size: {sizeof_fmt(len(item.data))}')
                    # print(i+f'  DSize: {sizeof_fmt(item.decompressed_size())}')
                # print(i+f'  Parent name: {None if item.parent is None else item.parent.name!r}')
                print()

                for child in item.childs:
                    print_pkg_item(child, indent + '    ')

            pkg = PKG.from_pkg(str(input_path))
            print(f'Package {input_path}:')
            print(f'  Current size (approximately): {sizeof_fmt(pkg.size())}')
            print(f'  Decompressed size (approximately): {sizeof_fmt(pkg.decompressed_size())}')
            print(f'  Number of items: {pkg.count()}')
            print(f'  Number of items in root: {len(pkg.root.childs)}')
            if pkg.metadata: print(f'  Metadata: {pkg.metadata!r}')
            print()

            print_pkg_item(pkg.root)

            return CODE_OK

        # unpacking
        if not output_path.parent.is_dir():
            print(f'{output_path!r} is not dir!')
            return CODE_ERR

        pkg = PKG.from_pkg(str(input_path))
        pkg.to_dir(str(output_path))
        return CODE_OK

    if input_path.exists() and input_path.is_dir():
        # packing
        extensions = [
            suf if suf.startswith('.') else f'.{suf}' for suf in args.extensions
        ]

        if not extensions:
            pred = lambda _: True
        else:
            pred = lambda filename: Path(filename).suffix in extensions

        pkg = PKG.from_dir(str(input_path), f=pred)
        pkg.compress(args.compression)
        pkg.metadata = args.metadata.encode('utf-8')
        pkg.to_pkg(str(output_path))
        return CODE_OK

    # wrong input
    print(f'Wrong paths: {input_path!r} {output_path!r}')
    return CODE_ERR


def process_gi(args):
    return CODE_ERR


def process_gai(args):
    return CODE_ERR


def process_script(args):
    return CODE_ERR


def process_save(args):
    from rangers.sav import SAV

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file() or not input_path.exists():
        print(f'{input_path} is not file')
        return CODE_ERR

    if input_path.suffix == '.sav':
        if output_path.suffix != '.json':
            print(f'Invalid extension: {output_path.suffix}')
            return CODE_ERR


        sav = SAV.from_sav(str(input_path))
        sav.to_json(str(output_path))

        return CODE_OK

    if input_path.suffix == '.json':

        sav = SAV.from_json(str(input_path))
        sav.to_sav(str(output_path))

        return CODE_OK

    print(f'Invalid extension: {input_path.suffix}')
    return CODE_ERR



def process_score(args):
    from rangers.score import SCORE

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file() or not input_path.exists():
        print(f'{input_path} is not file')
        return CODE_ERR

    if input_path.suffix == '.txt':
        if output_path.suffix != '.json':
            print(f'Invalid extension: {output_path.suffix}')
            return CODE_ERR


        score = SCORE.from_txt(str(input_path))
        score.to_json(str(output_path))

        return CODE_OK

    if input_path.suffix == '.json':

        score = SCORE.from_json(str(input_path))
        score.to_sav(str(output_path))

        return CODE_OK

    print(f'Invalid extension: {input_path.suffix}')
    return CODE_ERR


if __name__ == "__main__":
    args = parser.parse_args()

    # print(args)

    match args.cmd:
        case 'dat':
            exitcode = process_dat(args)

        case 'pkg':
            exitcode = process_pkg(args)

        case 'gi':
            exitcode = process_gi(args)

        case 'gai':
            exitcode = process_gai(args)

        case 'script':
            exitcode = process_script(args)

        case 'save':
            exitcode = process_save(args)

        case 'score':
            exitcode = process_score(args)

        case _:
            print(f'Unknown command: {args.cmd}')
            exitcode = CODE_ERR

    if exitcode == CODE_ERR:
        print()
        print('Error occurred!')
    sys.exit(exitcode)
