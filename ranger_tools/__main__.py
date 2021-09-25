import os
import sys
import time
import argparse
import pathlib
import shutil

from . import modding


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='cmd')


dat_parser = subparsers.add_parser('dat', help='-')

dat_parser.add_argument('-s', '--sign', action='store_true')
dat_parser.add_argument('-f', '--format', action='store', choices=['SR1', 'ReloadMain', 'ReloadCache', 'HDMain', 'HDCache'], default='HDMain')

dat_parser.add_argument('input', action='store', type=str)
dat_parser.add_argument('output', action='store', type=str)



pkg_parser = subparsers.add_parser('pkg', help='-')

pkg_parser.add_argument('input', action='store', type=str)
pkg_parser.add_argument('output', action='store', type=str)

pkg_parser.add_argument('-c', '--compression', action='store', type=int, choices=range(-1, 10), default=None)
pkg_parser.add_argument('-m', '--metadata', action='store', type=str, default='')
pkg_parser.add_argument('-e', '--extensions', action='append', type=str, default=[])




gi_parser = subparsers.add_parser('gi', help='-')

gi_parser.add_argument('-f', '--format', action='store', type=str, choices=['0_16', '0_32', '2'], default='2')

gi_parser.add_argument('input', action='store', type=str)
gi_parser.add_argument('output', action='store', type=str)



gai_parser = subparsers.add_parser('gai', help='-')

# gai_parser.add_argument('-f', '--format', action='store', type=int)
# gai_parser.add_argument('-b', '--bits', action='store', choices=[16, 32], type=int)
gai_parser.add_argument('-c', '--compression', action='store', type=int, choices=range(-1, 10), default=None)

gai_parser.add_argument('input', action='store', type=str)
gai_parser.add_argument('output', action='store', type=str)



script_parser = subparsers.add_parser('script', help='-')

script_parser.add_argument('-t', '--text', action='store', type=str)

script_parser.add_argument('input', action='store', type=str)
script_parser.add_argument('output', action='store', type=str)



save_parser = subparsers.add_parser('save', help='-')

save_parser.add_argument('input', action='store', type=str)
save_parser.add_argument('output', action='store', type=str)


args = parser.parse_args()

print(args)


match args.cmd:
    case 'dat':
        pass

    case 'pkg':
        pass

    case 'gi':
        pass

    case 'gai':
        pass

    case 'script':
        pass

    case 'save':
        pass

    case _:
        print(f'Unknown command: {args.cmd}')

