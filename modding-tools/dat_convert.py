# dat_convert [options] [inputs] output
# options:
# -c - cachedata
# -r - reload
# -1 - sr1
# -s - sign

import argparse

from ranger_tools.dat import DAT

parser = argparse.ArgumentParser(description='Tool for converting and merging .dat files')
parser.add_argument('inputs', metavar='F', type=str, nargs='+',
                   help='input file')
parser.add_argument('output', metavar='O', type=str,
                   help='output file')

parser.add_argument('-c', '--cache', dest='cache', action='store_true',
                   help='output is cachedata')
parser.add_argument('-t', '--type', dest='type', action='store', choices=['sr1', 'reload', 'hd'], default='hd',
                   help='type of output dat')
parser.add_argument('-s', '--sign', dest='sign', action='store_true',
                   help='sign result dat')


args = parser.parse_args()
print(args)

# result = DAT()

# for file in args.inputs:
#     if file.endswith('.txt'):
#         print(f'txt input file: {file}')
#         dat = DAT.from_txt(file)
#     elif file.endswith('.dat'):
#         print(f'dat input file: {file}')
#         dat = DAT.from_dat(file)
#     else:
#         print(f'unknown file format: {file}')
#         continue

#     print(result)
#     print(dat)

# print(f'result: {result}')

# print(f'{args.output = }')
