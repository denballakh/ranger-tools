import os
import time



t = time.time()

for disk in {'C:\\', 'D:\\'}:
    for path, _, files in os.walk(disk):
        for file in files:
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            if not filename.endswith('.py'): continue
            if os.path.getmtime(filename) > t - 3600 * 40:
                print(filename)

