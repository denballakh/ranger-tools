import os
import time
import argparse

from ..dat import DAT
from ..pkg import PKG
from ..gi import GI
from ..gai import GAI
from ..scr import SCR
from ..svr import SVR


__all__ = [
    'ModBuilder',
    'Logger',
    'DEBUG', 'VERBOSE', 'INFO', 'WARNING', 'ERROR', 'NONE',
]

DEBUG =     (-1, "DEBUG")   # дебаговый вывод разного мусора
VERBOSE =   (0, "VERBOSE")  # подробный вывод всех обрабатываемых файлов
INFO =      (1, "INFO")     # короткое описание всех выполняемых действий
WARNING =   (2, "WARNING")  # предупреждения о странных входных данных или файлах
ERROR =     (3, "ERROR")    # ошибки
NONE =      (10**10, "")    # приоритет для отключения любого вывода

class Logger:
    def __init__(self, priority, file='########.log'):
        self.priority = priority
        self.file = file
        if file:
            open(file, 'wb').close() # очищаем файл
            with open(self.file, mode='wt+') as f:
                print(f'New logger instance. Time: {time.asctime(time.gmtime())}. Local time: {time.ctime()}', file=f)


    def log(self, priority, *args, **kwargs):
        if priority[0] >= self.priority[0]:
            print(f'[{priority[1]}] ', *args, **kwargs)

            if self.file:
                if os.path.isfile(self.file):
                    mode = 'wt+'
                else:
                    mode = 'wt'

                with open(self.file, mode=mode) as f:
                    print(f'[{priority[1]}] ', *args, **kwargs, file=f)


class ModBuilder:
    '''
    Класс для сборки модов

    Пути output в функциях указаны относительно пути ModBuilder.build_path, если не указано иного
    '''
    def __init__(self, *,
            build_path='build/',
            in_game_path='Mods/UNKNOWNPATH/',
            verbosity_level=INFO,
            log_file='########.log'
        ):
        '''
        build_path - путь, по которому будут создаваться все файлы
        in_game_path - путь, по которому будет лежать мод в игре
            нужен для подстановки в текстовые значения
        verbosity_level - уровень подробности вывода
        log_file - файл для логгирования
        '''
        self.build_path = build_path + '/'
        self.in_game_path = in_game_path + '/'
        self.logger = Logger(verbosity_level, file=log_file)

    #####
    # вспомогательные функции
    #####
    # используются пути относительно скрипта или абсолютные пути

    def log(self, priority, *args, **kwargs):
        self.logger.log(priority, *args, **kwargs)

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
                    self.log(VERBOSE, f'Created directory {res}')
                except FileExistsError:
                    self.log(ERROR, f'Directory already exists O_o: {res}. '
                        'Maybe a lot of scripts are running at the same time and trying to make this directory')

    def copy_file(self, input, output):
        '''
        Копирует файл из одного места в другое

        input - входной файл
        output - результирующий файл
        '''
        self.log(INFO, f'Copying file from {input} to {output}')
        with open(input, 'rb') as _in:
            with open(output, 'wb') as _out:
                _out.write(_in.read())

    def del_file(self, file):
        '''
        Удаляет файл
        '''
        self.log(INFO, f'Deleting file {file}')
        os.remove(file)

    def del_dir(self, folder):
        '''
        Удаляет папку
        '''
        self.log(INFO, f'Deleting directory {folder}')
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def copy_dir(self, input_dir, output_dir):
        '''
        Копирует папку из одного места в другое
        Сохраняет структуру папки, работает с любым уровнем вложенности
        Перезапишет существующие папки

        input_dir - входная папка
        output_dir - результирующая папка
        '''
        raise NotImplementedError

    #####
    # функции для работы с модом
    #####
    # используются пути относительно скрипта или абсолютные пути для входных файлов
    # для выходных файлов используются пути относительно пути build_path
    #     (который может быть абсолютным или относительно скрипта)

    # работа с файлами
    def clean_build(self):
        '''
        Очищает папку билда
        '''
        self.log(INFO, )
        self.del_dir(self.build_path)

    def backup(self,
            backup_path, *,
            backup_extensions=('.txt', '.dat', '.svr', '.scr', '.dll', '.c', '.cpp', '.py', '.json'),
            compression_level=None,
        ):
        '''
        backup_path - путь для создания бэкапов
            перед каждым билдом будет создан бэкап по этому пути
            файл бэкапа - пакет без сжатия
        backup_extensions - расширения файлов, которые будут сохранены в бэкапе
        '''
        f = lambda file: '.' + file.split('.')[-1].lower() in backup_extensions
        pkg = PKG.from_dir('./', f=f)
        if compression_level is not None:
            pkg.compress(compression_level)

        filename = f'{backup_path}/backup_{int(time.time())}.pkg'
        self.log(INFO, f'Packing backup file to {filename} [{pkg.size()} bytes]')
        self.log(VERBOSE, f'Backup contains {pkg.count()} files')
        pkg.to_pkg(filename)

    def pack_folder(self, folder_path, output, *, compression_level=9, metadata=b'', f=lambda _: True):
        '''
        Упаковывает папку в пакет

        folder_path - папка, содержимое которой нужно упаковать
        output - результирующий пакет

        compression_level - уровень сжатия пакета
        metadata - метаданные, которые нужно прописать в пакет
        '''
        pkg = PKG.from_dir(folder_path, f)
        if compression_level is not None:
            pkg.compress(compression_level)

        if pkg.size() == 0:
            self.log(WARNING, f'Size of package {output} is zero.')
            if pkg.count() == 0:
                self.log(WARNING, f'Package {output} contains no files')

        self.log(INFO, f'Packing directory {folder_path} to {output}')
        self.log(VERBOSE, f'Package size: {pkg.size()}, compression level: {compression_level}')
        pkg.to_pkg(output)

    # датники
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
            self.log(WARNING, 'Empty files sequence. Skipping...')
            return

        output = self.build_path + output

        result = DAT()
        for file in inputs:
            if file.endswith('.txt'):
                dat = DAT.from_txt(file)
            elif file.endswith('.dat'):
                dat = DAT.from_dat(file)
            else:
                self.log(WARNING, f'Unknown file extension: {file}. Interpret as ".dat"')
                dat = DAT.from_dat(file)
            self.log(DEBUG, dat)
            result.merge(dat)
        self.log(DEBUG, result)

        if result.is_empty():
            self.log(WARNING, f'DAT {output} is empty. Skipping...')
            return

        if fmt == 'Auto':
            if output.endswith('Lang.dat'): fmt = 'HDMain'
            elif output.endswith('Main.dat'): fmt = 'HDMain'
            elif output.endswith('CacheData.dat'): fmt = 'HDCache'
            else:
                fmt = 'HDMain'
                self.log(WARNING, f'Cannot automatically detect file format: {output}. Interpret as {fmt}')

        self.log(VERBOSE, f'Saving resultding dat to {output}')
        self.check_dir(output)
        if output.endswith('.txt'):
            result.to_txt(output)
        elif output.endswith('.dat'):
            result.to_dat(output, fmt=fmt, sign=sign)
        else:
            self.log(WARNING, f'Unknown file extension: {output}. Interpret as ".dat"')
            result.to_dat(output, fmt=fmt, sign=sign)

    def convert_lang(self, inputs, *, lang='Rus', sign=False):
        self.convert_dats(inputs, f'CFG/{lang}/Lang.dat', fmt='HDMain', sign=sign)

    def convert_main(self, inputs, *, sign=False):
        self.convert_dats(inputs, 'CFG/Main.dat', fmt='HDMain', sign=sign)

    def convert_cachedata(self, inputs, *, sign=False):
        self.convert_dats(inputs, 'CFG/CacheData.dat', fmt='HDCache', sign=sign)

    # текстовики
    def write_moduleinfo(self, data=None, *, filename='ModuleInfo.txt'):
        '''
        Создает файл информации о моде

        data - словарь к информацией о моде
            значения Name, Section и SectionEng могут вычислиться автоматически на основе ModBuilder.in_game_path
            все остальные значения получат стандартное значение, если не указаны

        filename - файл результата
        '''
        try:
            module_name = self.in_game_path.replace('\\', '/').split('/')[-1]
        except KeyError:
            self.log(WARNING, 'Cannot get module name from in_game_path')
            module_name = 'UNKNOWN_MODULE_NAME'

        try:
            section_name = self.in_game_path.replace('\\', '/').split('/')[-2]
        except KeyError:
            self.log(WARNING, 'Cannot get section name from in_game_path')
            section_name = 'UNKNOWN_SECTION_NAME'

        section_names = {
            'Tweaks':           ('Твики', 'Tweaks'),
            'OtherMods':        ('Прочие моды', 'Other mods'),
            'Expansion':        ('Экспансия', 'Expansion'),
            'Evolution':        ('Эволюция', 'Evolution'),
            'Revolution':       ('Революция', 'Revolution'),
            'ShusRangers':      ('Shu\'s Rangers', 'Shu\'s Rangers'),
            'Kotyanka':         ('КОТянка', 'Kotyanka'),
            'AnotherMods':      ('HukMods', 'HukMods'),
            'Solyanka':         ('Солянка', 'Solyanka'),
            'PlanetaryBattles': ('Планетарные бои', 'Planetary Battles'),
            'Fairan\'s Vision': ('Fairan\'s Vision', 'Fairan\'s Vision'),
            # '': ('', ''),
        }

        default = {
            'Name': module_name,
            'Author': 'UNKNOWN_AUTHOR',
            'Conflict': '',
            'Priority': '0',
            'Dependence': '',
            'Languages': 'Rus',

            'Section': section_names[section_name] if section_name in section_names else '',
            'SmallDescription': f'короткое описание мода {module_name}',
            'FullDescription': f'полное описание мода {module_name}',

            'SectionEng': section_names[section_name] if section_name in section_names else '',
            'SmallDescriptionEng': f'small description {module_name}',
            'FullDescriptionEng': f'full description {module_name}',
        }

        moduleinfo_data = default
        if data is not None:
            moduleinfo_data.update(data)

        content = ''
        for key, value in moduleinfo_data.items():
            values = value.split('\n')
            for v in values:
                content += f'{key}={v}\n'

        self.log(INFO, f'Saving module info to {filename}')
        filename = self.build_path + filename
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
            self.log(WARNING, 'Empty pkgs sequence. Skipping...')
            return

        if filename is None:
            if lang is not None and lang != '' and lang != 'COMMON':
                lang = '_' + lang
            else:
                lang = ''

            filename = f'INSTALL{lang}.TXT'

        content = 'Packages {\n'
        for pkg in pkgs:
            content += f'    Package={pkg}\n'
        content += '}\n'

        filename = self.build_path + filename
        self.log(INFO, f'Saving install info to {filename}')
        self.check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    # графика
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

    def convert_gai(self, input_dir, output, **kwargs):
        files = os.listdir(input_dir)
        self.convert_img([input_dir + file for file in files], output, **kwargs)

    def convert_gis(self, input_dir, output_dir, **kwargs):
        files = os.listdir(input_dir)
        for file in files:
            out_file = '.'.join(file.split('.')[:-1]) + '.gi'
            self.convert_img(input_dir + file, output_dir + out_file, **kwargs)

    # бинарники
    def build_script(self, input, output, *, text=None, add_to_dats=False, add_text_to_lang=False):
        '''
        Собирает скрипт из исходников

        input - файл исходника
        output - файл скомпилированного скрипта

        add_to_dats - пропишет скрипт в мейн и кешдату
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        add_text_to_lang - пропишет строки из скрипта в ланг
            эти правки потом будет необходимо применить функцией ModBuilder.apply_dat_changes
        '''
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


    def apply_changes(self, paths=None, sign='Keep'):
        '''
        Применит сделанные правки в датниках
        И пропишет пакеты в инсталлы

        sign - True/False/'Keep'
            подписывать ли измененные датники
            'Keep' - оставить состояние подписи в том же виде
        paths - словарь с ключами 'Lang', 'Main', 'CacheData'
            пути датников для изменения
        '''
        default_paths = {
            'Lang': 'CFG/Rus/Lang.dat',
            'Main': 'CFG/Main.dat',
            'CacheData': 'CFG/CacheData.dat',
            'RUSSIAN': 'INSTALL_RUSSIAN.TXT',
            'ENGLISH': 'INSTALL_ENGLISH.TXT',
            'COMMON': 'inSTALL.TXT',
        }
        raise NotImplementedError

    def automatic_build(self, *args, **kwargs):
        raise NotImplementedError

    def autoconvert_dir(self, *args, **kwargs):
        raise NotImplementedError




def build_sub_mods():
    '''
    Функция для рекурсивного билда целых сборок

    В корне каждой сборки нужно создать файл с этими строками:

    from ranger_tools.modding import build_sub_mods
    build_sub_mods()

    Автоматически распознаются только батники и py-скрипты с именами:
        %%_build
        build_%%
        %%
        build
    где %% - имя папки
    Приоритет батников выше, чем у py-скриптов. Порядок перебора имен написан выше
    '''
    for mod in os.listdir('./'):
        for bat_file in (
                f'{mod}/{mod}_build.bat',
                f'{mod}/build_{mod}.bat',
                f'{mod}/{mod}.bat',
                f'{mod}/build.bat'
            ):
            if os.path.isfile(bat_file):
                os.system(bat_file)
                continue

        for python_file in (
                f'{mod}/{mod}_build.py',
                f'{mod}/build_{mod}.py',
                f'{mod}/{mod}.py',
                f'{mod}/build.py'
            ):
            if os.path.isfile(python_file):
                os.system(f'python {python_file}')
                continue
