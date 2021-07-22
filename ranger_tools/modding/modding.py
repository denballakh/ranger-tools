from ..dat import DAT
from ..pkg import PKG
from ..gi import GI
from ..gai import GAI
from ..scr import SCR
from ..svr import SVR

from ..common import check_dir

__all__ = [
    'ModBuilder',
    'Tools',
]

class Tools:
    @staticmethod
    def load_dat(path: str) -> DAT:
        pass

    def load(self):pass

class ModBuilder:
    def __init__(self, *, build_path='build/', in_game_path='Mods/UNKNOWNPATH/'):
        self.build_path = build_path + '/'
        self.in_game_path = in_game_path + '/'

    def merge_(self):
        pass

    def convert_dats(self, inputs, output, *, fmt='Auto', sign=False):
        if not isinstance(inputs, list):
            inputs = [inputs]

        if len(inputs) == 0:
            print('Empty files sequence. Skipping...')
            return

        output = self.build_path + output

        result = DAT()
        for file in inputs:
            if file.endswith('.txt'):
                dat = DAT.from_txt(file)
            elif file.endswith('.dat'):
                dat = DAT.from_dat(file)
            else:
                print(f'Unknown file extension: {file}. Interpret as ".dat"')
                dat = DAT.from_dat(file)
            print(dat)
            result.merge(dat)

        if fmt == 'Auto':
            if output.endswith('Lang.dat'): fmt = 'HDMain'
            elif output.endswith('Main.dat'): fmt = 'HDMain'
            elif output.endswith('CacheData.dat'): fmt = 'HDCache'
            else: fmt = 'HDMain'

        check_dir(output)
        if output.endswith('.txt'):
            result.to_txt(output)
        elif output.endswith('.dat'):
            result.to_dat(output, fmt=fmt, sign=sign)
        else:
            print(f'Unknown file extension: {output}. Interpret as ".dat"')
            result.to_dat(output, fmt=fmt, sign=sign)


    def convert_lang(self, inputs, *, lang='Rus', sign=False):
        self.convert_dats(inputs, f'CFG/{lang}/Lang.dat', fmt='HDMain', sign=sign)

    def convert_main(self, inputs, *, sign=False):
        self.convert_dats(inputs, 'CFG/Main.dat', fmt='HDMain', sign=sign)

    def convert_cachedata(self, inputs, *, sign=False):
        self.convert_dats(inputs, 'CFG/CacheData.dat', fmt='HDCache', sign=sign)

    def write_moduleinfo(self, data, *, filename='ModuleInfo.txt'):
        filename = self.build_path + filename

        content = ''
        for key, value in data.items():
            values = value.split('\n')
            for v in values:
                content += f'{key}={v}\n'

        check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    def write_install(self, pkgs, *, filename=None, lang=None):
        if not isinstance(pkgs, list):
            pkgs = [pkgs]

        if len(pkgs) == 0:
            print('Empty pkgs sequence. Skipping...')
            return

        if filename is None:
            if lang is not None:
                lang = '_' + lang
            else:
                lang = ''

            filename = f'INSTALL{lang}.TXT'

        filename = self.build_path + filename

        content = 'Packages {\n'
        for pkg in pkgs:
            content += f'    Package={pkg}\n'
        content += '}\n'

        check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    def pack_folder(self, folder_path, output, *, compress=True, metadata=b''):
        pass

    def build_script(self, input, output, *, text=None, add_to_dats=False, add_text_to_lang=False):
        pass

    def convert_img(self, inputs, output, *, opt=None, cache_data_path=False, metadata=b''):
        pass

    def convert_gai(self, *args, **kwargs):
        pass

    def convert_gis(self, *args, **kwargs):
        pass

    def apply_dat_changes(self, *args, **kwargs):
        pass

    def automatic_build(self, *args, **kwargs):
        pass




