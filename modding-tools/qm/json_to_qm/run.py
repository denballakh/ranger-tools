from rangers.qm import QM, VER_QMM
from rangers.common import tree_walker, check_dir, file_rebase, change_ext

_in = '_input/'
_out = '_output/'


check_dir(_in)
check_dir(_out)

for filename in tree_walker(_in, exts=('.json',))[0]:
    try:
        qm = QM.from_json(filename)
        ext = '.qmm' if qm.data['version'] in VER_QMM else '.qm'
        output_name = change_ext(file_rebase(filename, _in, _out), '.json', ext)
        print(f'{filename} -> {output_name}')
        check_dir(output_name)
        qm.to_file(output_name)

    except:
        import traceback

        print(traceback.format_exc())
