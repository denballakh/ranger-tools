## @file

import os
import time
# import argparse
import enum
from typing import Optional, Callable, Union, List

from ..dat import DAT
from ..pkg import PKG
from ..graphics.gi import GI
from ..graphics.gai import GAI
from ..graphics.hai import HAI
from ..rscript.scr import SCR
from ..rscript.svr import SVR


__all__ = [
    'ModBuilder',
    'Logger',
    'LL'
]

##
# Декоратор для нереализованных функций.
#
# При вызове будет брошено исключение `NotImplementedError`.
def not_implemented(func: Callable):
    def f(*args, **kwargs):
        raise NotImplementedError
    return f

##
# Декоратор для устаревших функций.
#
# При вызове в лог будет выведено сообщение.
def deprecated(func: Callable):
    def f(self, *args, **kwargs):
        self.log(LL.WARNING, f'Function {func!r} is deprecated!')
        func(self, *args, **kwargs)
    return f

##
# Декоратор для безопасного вызова функций.
#
# При возникновении исключения оно будет поймано и выведено в лог.
def safe_call(func: Callable):
    def f(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except exc:
            self.log(LL.ERROR, f'Error in function {func!r}: {exc!r}')
            return None
    return f

@enum.unique
class LL(enum.Enum):
    ## Дебаговый вывод разного мусора.
    DEBUG =   float('-inf')
    ## Подробный вывод всех обрабатываемых файлов.
    VERBOSE =  0
    ## Короткое описание всех выполняемых действий.
    INFO =     1
    ## Предупреждения о странных входных данных или файлах.
    WARNING =  2
    ## Ошибки.
    ERROR =    3
    ## Отключение любого вывода.
    NONE =     float('+inf')

##
# Класс для логгирования сообщений.
class Logger:
    ##
    # @param priority   Уровень подробности логгирования.
    # @param filename   Файл лога.
    # @param clear_file Если `True`, то файл лога будет очищен.
    def __init__(self,
            priority: LL,
            filename: Optional[str] = '########.log',
            clear_file: bool = False,
    ):
        self.priority = priority
        self.filename = filename
        if filename:
            if clear_file:
                open(filename, 'wb').close()
            with open(self.filename, mode='wt+') as f:  # type: ignore[arg-type]
                print(f'New logger instance. Time: {time.asctime(time.gmtime())}. Local time: {time.ctime()}', file=f)

    ##
    # Пишет сообщение в консоль и в файл лога (если он есть).
    #
    # Если файла лога нет, то он будет создан.
    #
    # @param priority Уровень логгирования.
    # @param args     Будет передано в функцию `print`.
    # @param kwargs   Будет передано в функцию `print`.
    def log(self, priority: LL, *args, **kwargs):
        if priority._value_ >= self.priority._value_:
            print(f'[{priority._name_}] ', *args, **kwargs)

            if self.filename:
                if os.path.isfile(self.filename):
                    mode = 'wt+'
                else:
                    mode = 'wt'

                with open(self.filename, mode=mode) as f:
                    print(f'[{priority._name_}] ', *args, **kwargs, file=f)


##
# Класс для сборки модов.
#
# Пути output в функциях указаны относительно пути ModBuilder.build_path, если не указано иного.
#
class ModBuilder:
    ##
    # @param build_path      Путь, по которому будут создаваться все файлы.
    # @param in_game_path    Путь, по которому будет лежать мод в игре (нужен для подстановки в текстовые значения).
    # @param verbosity_level Уровень подробности вывода.
    # @param log_file        Файл для логгирования.
    def __init__(self, *,
            build_path: str = 'build/',
            in_game_path: str = 'Mods/UNKNOWNPATH/',
            verbosity_level: LL = LL.INFO,
            log_file: str = '########.log'
        ):
        self.build_path = build_path + '/'
        self.in_game_path = in_game_path + '/'
        self.logger = Logger(verbosity_level, filename=log_file)


    # вспомогательные функции
    # используются пути относительно скрипта или абсолютные пути

    ##
    # Выводит сообщение в лог.
    #
    # @param priority Уровень логгирования.
    # @param args     Будет передано в функцию `print`.
    # @param kwargs   Будет передано в функцию `print`.
    def log(self, priority: LL, *args, **kwargs):
        self.logger.log(priority, *args, **kwargs)

    ##
    # Создаст папку, если такой не существует.
    #
    # Создаст любой необходимый уровень вложенности.
    # Используется перед каждой записью файла для избежания ошибок отсутствующих папок.
    #
    # @param file     Абсолютный путь к файлу.
    def check_dir(self, file: str):
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
                    self.log(LL.VERBOSE, f'Created directory {res}')
                except FileExistsError:
                    self.log(LL.ERROR, f'Directory already exists O_o: {res}. '
                        'Maybe a lot of scripts are running at the same time and trying to make this directory')

    ##
    # Копирует файл из одного места в другое.
    #
    # @param inp  Входной файл.
    # @param outp Результирующий файл.
    def copy_file(self, inp: str, outp: str):
        self.log(LL.INFO, f'Copying file from {inp} to {outp}')
        with open(inp, 'rb') as _in:
            with open(outp, 'wb') as _out:
                _out.write(_in.read())


    ##
    # Удаляет файл.
    def del_file(self, file: str):
        self.log(LL.INFO, f'Deleting file {file}')
        os.remove(file)

    ##
    # Удаляет папку.
    def del_dir(self, folder: str):
        self.log(LL.INFO, f'Deleting directory {folder}')
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


    ##
    # Копирует папку из одного места в другое.
    #
    # Сохраняет структуру папки, работает с любым уровнем вложенности.
    # Перезапишет существующие папки.
    #
    # @param input_dir  Входная папка.
    # @param output_dir Результирующая папка.
    @not_implemented
    def copy_dir(self, input_dir: str, output_dir: str):
        ...


    ##
    # Очищает папку билда.
    def clean_build(self):
        self.log(LL.INFO, )
        self.del_dir(self.build_path)

    ##
    # Создает бэкап текущих исходников.
    #
    # @param backup_path         Путь для создания бэкапов.
    #    Перед каждым билдом будет создан бэкап по этому пути.
    #    Файл бэкапа - пакет (.pkg) без сжатия.
    # @param backup_extensions   Расширения файлов, которые будут сохранены в бэкапе.
    def backup(self,
            backup_path: str, *,
            backup_extensions: tuple[str, ...] = ('.txt', '.dat', '.svr', '.scr', '.dll', '.c', '.cpp', '.py', '.json'),
            compression_level: Optional[int] = None,
        ):
        f = lambda file: '.' + file.split('.')[-1].lower() in backup_extensions
        pkg = PKG.from_dir('./', f=f)
        if compression_level is not None:
            pkg.compress(compression_level)

        filename = f'{backup_path}/backup_{int(time.time())}.pkg'
        self.log(LL.INFO, f'Packing backup file to {filename} [{pkg.size()} bytes]')
        self.log(LL.VERBOSE, f'Backup contains {pkg.count()} files')
        pkg.to_pkg(filename)


    ##
    # Упаковывает папку в пакет.
    #
    # @param folder_path - папка, содержимое которой нужно упаковать.
    # @param output - результирующий пакет.
    # @param compression_level - уровень сжатия пакета.
    # @param metadata - метаданные, которые нужно прописать в пакет.
    # @param f - функция `filename: str -> bool`, определяющая, нужно ли добавлять файл в пакет.
    def pack_folder(self,
            folder_path: str,
            output: str, *,
            compression_level: int = 9,
            metadata: bytes = b'',
            f: Callable = lambda _: True
    ):
        pkg = PKG.from_dir(folder_path, f)
        if compression_level is not None:
            pkg.compress(compression_level)

        if pkg.size() == 0:
            self.log(LL.WARNING, f'Size of package {output} is zero.')
            if pkg.count() == 0:
                self.log(LL.WARNING, f'Package {output} contains no files')

        self.log(LL.INFO, f'Packing directory {folder_path} to {output}')
        self.log(LL.VERBOSE, f'Package size: {pkg.size()}, compression level: {compression_level}')
        pkg.metadata = metadata
        pkg.to_pkg(output)


    ##
    # Конвертирует несколько датников в один.
    #
    # @param inputs - список входных файлов или один файл.
    #    файлы могут иметь расширение .txt и .dat.
    #    формат распознается автоматически.
    # @param output - файл результата.
    # @param fmt - формат шифрования результирующего файла.
    #    возможные значения: `Auto`, `HDMain`, `HDCache`, `ReloadMain`, `ReloadCache`, `SR1`.
    #    'Auto' - формат распознается автоматически на основе названия файла.
    # @param sign - подписать ли результирующий датник.
    def convert_dats(self, inputs: Union[str, list[str]], output: str, *, fmt: str = 'Auto', sign: bool = False):

        if not isinstance(inputs, list):
            inputs = [inputs]

        if len(inputs) == 0:
            self.log(LL.WARNING, 'Empty files sequence. Skipping...')
            return

        output = self.build_path + output

        result = DAT()
        for file in inputs:
            if file.endswith('.txt'):
                dat = DAT.from_txt(file)
            elif file.endswith('.dat'):
                dat = DAT.from_dat(file)
            else:
                self.log(LL.WARNING, f'Unknown file extension: {file}. Interpret as ".dat"')
                dat = DAT.from_dat(file)
            self.log(LL.DEBUG, dat)
            result.merge(dat)
        self.log(LL.DEBUG, result)

        if result.is_empty():
            self.log(LL.WARNING, f'DAT {output} is empty. Skipping...')
            return

        if fmt == 'Auto':
            if output.endswith('Lang.dat'): fmt = 'HDMain'
            elif output.endswith('Main.dat'): fmt = 'HDMain'
            elif output.endswith('CacheData.dat'): fmt = 'HDCache'
            else:
                fmt = 'HDMain'
                self.log(LL.WARNING, f'Cannot automatically detect file format: {output}. Interpret as {fmt}')

        self.log(LL.VERBOSE, f'Saving resultding dat to {output}')
        self.check_dir(output)
        if output.endswith('.txt'):
            result.to_txt(output)
        elif output.endswith('.dat'):
            result.to_dat(output, fmt=fmt, sign=sign)
        else:
            self.log(LL.WARNING, f'Unknown file extension: {output}. Interpret as ".dat"')
            result.to_dat(output, fmt=fmt, sign=sign)


    ##
    #
    def convert_lang(self, inputs: Union[str, list[str]], *, lang: str = 'Rus', sign: bool = False):
        self.convert_dats(inputs, f'CFG/{lang}/Lang.dat', fmt='HDMain', sign=sign)

    ##
    #
    def convert_main(self, inputs: Union[str, list[str]], *, sign: bool = False):
        self.convert_dats(inputs, 'CFG/Main.dat', fmt='HDMain', sign=sign)

    ##
    #
    def convert_cachedata(self, inputs: Union[str, list[str]], *, sign: bool = False):
        self.convert_dats(inputs, 'CFG/CacheData.dat', fmt='HDCache', sign=sign)

    ##
    # Создает файл информации о моде.
    #
    # @param data - словарь к информацией о моде.
    #    значения `Name`, `Section` и `SectionEng` могут вычислиться автоматически на основе ```ModBuilder.in_game_path```.
    #    все остальные значения получат стандартное значение, если не указаны.
    #
    # @param filename - файл результата.
    def write_moduleinfo(self, data: Optional[dict[str, str]] = None, *, filename: str = 'ModuleInfo.txt'):
        try:
            module_name = self.in_game_path.replace('\\', '/').split('/')[-1]
        except KeyError:
            self.log(LL.WARNING, f'Cannot get module name from "in_game_path": {self.in_game_path}')
            module_name = 'UNKNOWN_MODULE_NAME'

        try:
            section_name = self.in_game_path.replace('\\', '/').split('/')[-2]
        except KeyError:
            self.log(LL.WARNING, f'Cannot get section name from "in_game_path": {self.in_game_path}')
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

        self.log(LL.INFO, f'Saving module info to {filename}')
        filename = self.build_path + filename
        self.check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    ##
    # Создает файл с путями к пакетам.
    #
    # @param pkgs - список пакетов.
    #
    # @param filename - файл результата.
    #     по умолчанию `INSTALL.TXT`.
    # @param lang - строка языка.
    #     по умолчанию пустая строка.
    #     значение `RUSSIAN` изменит название файла на `INSTALL_RUSSIAN.TXT`.
    #     не применяется, если указано значение `filename`.
    def write_install(self, pkgs: Union[str, list[str]], *, filename=None, lang=None):

        if not isinstance(pkgs, list):
            pkgs = [pkgs]

        if len(pkgs) == 0:
            self.log(LL.WARNING, 'Empty pkgs sequence. Skipping...')
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
        self.log(LL.INFO, f'Saving install info to {filename}')
        self.check_dir(filename)
        with open(filename, 'wt') as file:
            file.write(content)

    ##
    # Конвертирует изображения.
    #
    # @param inputs - список входных файлов или один файл.
    #     файлы могут иметь расширения `png` и `gi`.
    #     если файл один, то произойдет конвертация в `gi`.
    #     иначе произойдет сборка `gai`.
    # @param output - файл результата.
    #
    # @param opt - опции создания ресурсов, имеет разное значение в зависимости от ситуации.
    # @param cache_data_path - пропишет ресурс в кешдату по указанному пути.
    #     эти правки потом будет необходимо применить функцией ```ModBuilder.apply_dat_changes```.
    # @param metadata - метаданные, которые нужно прописать в пакет.
    @not_implemented
    def convert_img(self, inputs: Union[str, list[str]], output: str, *, opt: object = None, cache_data_path: str = '', metadata: bytes = b''):
        ...

    def convert_gai(self, input_dir: str, output: str, **kwargs):
        files = os.listdir(input_dir)
        self.convert_img([input_dir + file for file in files], output, **kwargs)

    def convert_gis(self, input_dir: str, output_dir: str, **kwargs):
        files = os.listdir(input_dir)
        for file in files:
            out_file = '.'.join(file.split('.')[:-1]) + '.gi'
            self.convert_img(input_dir + file, output_dir + out_file, **kwargs)

    ##
    # Собирает скрипт из исходников.
    #
    # @param input - файл исходника.
    # @param output - файл скомпилированного скрипта.
    #
    # @param add_to_dats - пропишет скрипт в мейн и кешдату.
    #     эти правки потом будет необходимо применить функцией ```ModBuilder.apply_dat_changes```.
    # @param add_text_to_lang - пропишет строки из скрипта в ланг.
    #     эти правки потом будет необходимо применить функцией ```ModBuilder.apply_dat_changes```.
    @not_implemented
    def build_script(self, input: str, output: str, *, text=None, add_to_dats=False, add_text_to_lang=False):
        ...

    ##
    # Копирует библиотеку в папку билда.
    #
    # @param input - входной файл.
    # @param output - результирующий файл.
    #
    # @param add_to_main - пропишет библиотеку в мейн.
    #     эти правки потом будет необходимо применить функцией ```ModBuilder.apply_dat_changes```.
    # @param functions - файл со списком сигнатур функций.
    #     эти правки потом будет необходимо применить функцией ```ModBuilder.apply_dat_changes```.
    @not_implemented
    def copy_library(self, input: str, output: str, *, add_to_main: bool = False, functions: Optional[str] = None):
        ...


    ##
    # Применит сделанные правки в датниках.
    # И пропишет пакеты в инсталлы.
    #
    # @param sign - `True`/`False`/`"Keep"`.
    #     подписывать ли измененные датники.
    #     `Keep` - оставить состояние подписи в том же виде.
    # @param paths - словарь с ключами `"Lang"`, `"Main"`, `"CacheData"`.
    #     пути датников для изменения
    @not_implemented
    def apply_changes(self, paths: Optional[dict[str, str]] = None, sign: Union[bool, str] = 'Keep'):
        default_paths = {
            'Lang': 'CFG/Rus/Lang.dat',
            'Main': 'CFG/Main.dat',
            'CacheData': 'CFG/CacheData.dat',
            'RUSSIAN': 'INSTALL_RUSSIAN.TXT',
            'ENGLISH': 'INSTALL_ENGLISH.TXT',
            'COMMON': 'inSTALL.TXT',
        }
        ...

    ##
    #
    @not_implemented
    def automatic_build(self, *args, **kwargs):
        ...

    ##
    #
    @not_implemented
    def autoconvert_dir(self, *args, **kwargs):
        ...




##
# Функция для рекурсивного билда сборок модов
#
# В корне сборки нужно создать файл с этими строками:
#
# ```py
# from ranger_tools.modding import build_sub_mods
# build_sub_mods()
# ```
#
# Автоматически распознаются только `bat`-файлы и `py`-скрипты с именами: `%%_build`, `build_%%`, `%%`, `build`,
# где `%%` - имя папки.
# Приоритет `bat`-файлов выше, чем у `py`-скриптов. Порядок перебора имен написан выше.
def build_sub_mods():
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
