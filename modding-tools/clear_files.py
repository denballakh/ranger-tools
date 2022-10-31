from pathlib import Path
import shutil
import itertools

for folder in itertools.chain(Path.cwd().rglob('_input'), Path.cwd().rglob('_output')):
    try:
        print(f'Deleting {folder}...')
        shutil.rmtree(folder)

    except:
        import traceback

        traceback.print_exc()
