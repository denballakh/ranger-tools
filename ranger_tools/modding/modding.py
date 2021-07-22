from ..dat import DAT
from ..pkg import PKG
from ..gi import GI
from ..gai import GAI
from ..scr import SCR
from ..svr import SVR

import os

__all__ = [
    'ModBuilder',
]

class ModBuilder:
    '''
    Класс для сборки модов

    Пути output в функциях указаны относительно пути ModBuilder.build_path, если не указано иного
    '''
    def __init__(self, *, build_path='build/', in_game_path='Mods/UNKNOWNPATH/', clean_before_build=False, backup_path=None, backup_extensions=['.txt', '.dat', '.svr', '.scr', '.dll']):
        '''
        build_path - путь, по которому будут создаваться все файлы
        in_game_path - путь, по которому будет лежать мод в игре
            нужен для подстановки в текстовые значения
        clean_before_build - очищает папку билда перед билдом
        backup_path - путь для создания бэкапов
            перед каждым билдом будет создан бэкап по этому пути
            файл бэкапа - пакет без сжатия
        backup_extensions - расширения файлов, которые будут сохранены в бэкапе
        '''
        self.build_path = build_path + '/'
        self.ModBuilder = in_game_path + '/'
        if clean_before_build:
            self.clean_build()

        f = lambda file: '.' + file.split('.')[-1].lower() in backup_extensions
        raise NotImplementedError

    def convert_dats(self, inputs, output, *, fmt='Auto', sign=False):
        '''
        Конвертирует несколько датников в один

        inputs - список входных файлов или один файл
            файлы могут иметь расширение .txt и .dat
            формат распознается автоматически
        output - файл результата

        fmt - формат шифрования результирующего файла
            возможные значения: 'Auto', 'HDMain', 'HDCache', 'ReloadMain', 'ReloadCache', 'SR1'
            'Auto' - формат распознается автоматически на основе названия файла
        sign - подписать результирующий датник
        '''

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

        self.check_dir(output)
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
        '''
        Создает файл информации о моде

        data - словарь к информацией о моде
            значения Name, Section и SectionEng могут вычислиться автоматически на основе ModBuilder.in_game_path
            все остальные значения получат стандартное значение, если не указаны

        filename - файл результата
        '''

        filename = self.build_path + filename

        content = ''
        for key, value in data.items():
            values = value.split('\n')
            for v in values:
                content += f'{key}={v}\n'

        self.check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    def write_install(self, pkgs, *, filename=None, lang=None):
        '''
        Создает файл с путями к пакетам

        pkgs - список пакетов

        filename - файл результата
            по умолчанию 'INSTALL.TXT'
        lang - строка языка
            по умолчанию пустая строка
            значение 'RUSSIAN' изменит название файла на 'INSTALL_RUSSIAN.TXT'
            не применяется, если указано значение filename
        '''

        if not isinstance(pkgs, list):
            pkgs = [pkgs]

        if len(pkgs) == 0:
            print('Empty pkgs sequence. Skipping...')
            return

        if filename is None:
            if lang is not None and lang != '':
                lang = '_' + lang
            else:
                lang = ''

            filename = f'INSTALL{lang}.TXT'

        filename = self.build_path + filename

        content = 'Packages {\n'
        for pkg in pkgs:
            content += f'    Package={pkg}\n'
        content += '}\n'

        self.check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    def pack_folder(self, folder_path, output, *, compress=True, metadata=b''):
        '''
        Упаковывает папку в пакет

        folder_path - папка, содержимое которой нужно упаковать
        output - результирующий пакет

        compress - True/False - сжатие пакета
        metadata - метаданные, которые нужно прописать в пакет
        '''
        raise NotImplementedError

    def build_script(self, input, output, *, text=None, add_to_dats=False, add_text_to_lang=False):
        '''
        Собирает скрипт из исзодников

        input - файл исходника
        output - файл скомпилированного скрипта

        add_to_dats - пропишет скрипт в мейн и кешдату
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        add_text_to_lang - пропишет строки из скрипта в ланг
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        '''
        raise NotImplementedError

    def convert_img(self, inputs, output, *, opt=None, cache_data_path='', metadata=b''):
        '''
        Конвертирует изображения

        inputs - список входных файлов или один файл
            файлы могут иметь расширения png и gi
            если файл один, то произойдет конвертация в gi
            иначе произойдет сборка gai
        output - файл результата

        opt - опции создания ресурсов, имеет разное значение в зависимости от ситуации
        cache_data_path - пропишет ресурс в кешдату по указанному пути
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        metadata - метаданные, которые нужно прописать в пакет
        '''
        raise NotImplementedError

    def convert_gai(self, input_dir, output, *, opt=None, cache_data_path='', metadata=b''):
        raise NotImplementedError

    def convert_gis(self, input_dir, output_dir, *, opt=None, cache_data_path='', metadata=b''):
        raise NotImplementedError

    def apply_dat_changes(self, sign='Keep'):
        '''
        Применит сделанные правки в датниках
        Изменит только датники по стандартному пути

        sign - True/False/'Keep'
            подписывать ли измененные датники
            'Keep' - оставить состояние подписи в том же виде
        '''
        raise NotImplementedError

    def automatic_build(self, *args, **kwargs):
        raise NotImplementedError

    def copy_library(self, input, output, *, add_to_main=False, functions=None):
        '''
        Копирует библиотеку в папку билда

        input - входной файл
        output - результирующий файл

        add_to_main - пропишет библиотеку в мейн
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        functions - файл со списком сигнатур функций
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        '''
        raise NotImplementedError


    def copy_file(self, input, output):
        '''
        Копирует файл из одного места в другое

        input - входной файл
        output - результирующий файл
        '''
        with open(input, 'rb') as _in:
            with open(output, 'wb') as _out:
                _out.write(_in.read())

    def del_file(self, file):
        '''
        Удаляет файл
        '''
        os.remove(file)

    def del_dir(self, folder):
        '''
        Удаляет папку
        '''
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def clean_build(self):
        '''
        Очищает папку билда
        '''
        self.del_dir(self.build_path)

    def copy_dir(self, input_dir, output_dir):
        '''
        Копирует папку из одного места в другое
        Сохраняет структуру папки, работает с любым уровнем вложенности
        Перезапишет существующие папки

        input_dir - входная папка
        output_dir - результирующая папка
        '''
        raise NotImplementedError

    def check_dir(self, file):
        '''
        Создаст папку, если такой не существует
        Создаст любой необходимый уровень вложенности

        file - абсолютный путь к файлу

        Используется перед каждой записи файла для избежания ошибок отсутствующих папок
        '''
        path = file
        path = path.replace('\\', '/').replace('//', '/')
        splitted = path.split('/')[:-1]
        splitted = [name.strip('/') for name in splitted]
        splitted = [name for name in splitted if name != '']
        splitted = [name + '/' for name in splitted]
        res = './'
        for _, item in enumerate(splitted):
            res += item
            if not os.path.isdir(res):
                try:
                    os.mkdir(res)
                except FileExistsError:
                    pass

