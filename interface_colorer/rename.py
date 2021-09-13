import os

_a = ' — копия'
_b = '_mask'

def process():
    for path, _, files in os.walk('./'):
        for file in files:
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            # if not filename.endswith('.png'): continue

            if _a in filename:
                print(filename)
                os.rename(filename, filename.replace(_a, _b))

if __name__ == '__main__':
    process()
