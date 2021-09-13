import os

def process():
    for path, _, files in os.walk('.'):
        for file in files:
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            # if not filename.endswith('.png'): continue

            if os.stat(filename).st_size == 0:
                print(filename[2:])
                os.remove(filename)

if __name__ == '__main__':
    process()
