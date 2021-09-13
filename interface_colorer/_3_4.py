'''
Создает папки модов, готовых к использованию к игре

Нужно сделать вручную:
Создать папки модов для совместимости с ExpInfoCenter и ShuKlissan
Сконвертировать Main.txt в Main.dat в каждом моде
Положить в каждый мод CacheData.dat
'''

import os
import time
import shutil

from ranger_tools.pkg import PKG
from ranger_tools.dat import DAT

COMPRESS_PKG = True
PROFILE = False

rewrite = False

color_texts = {
    'Red':       ('150,0,0',     'красный',        'red'),
    'Blue':      ('0,0,150',     'синий',          'blue'),
    'Green':     ('0,150,0',     'зеленый',        'green'),
    'LightPink': ('188,134,162', 'светло-розовый', 'light pink'),

    'Yellow':    ('150,150,0',   'желтый',       'yellow'),
    'Magenta':   ('150,0,150',   'пурпурный',    'magenta'),
    'Orange':    ('150,75,0',    'оранжевый',    'orange'),

    'Grey':      ('127,127,127', 'серый',        'grey'),
    'DarkGrey':  ('63,63,63',    'темно-серый',  'dark-grey'),
}

priority = 11

mod_path = 'Mods/Tweaks/'
mod_name = 'UIRecolor'
section_rus = 'Твики'
section_eng = 'Tweaks'

dat_prefix = 'CFG/'
pkg_prefix = 'DATA/'


_dats = '_dats/'
_in = '3_result/'
_out = '4_output/'


special_mods = 'ShuKlissan', 'ExpInfoCenter'
spec_mod_rgb = '0,150,50'
mod_rgb = '88,188,192'
attention_rgb = '249,18,18'


def get_module_info_content(color, colors):
    assert color in color_texts, color
    assert color in colors

    rgb, text_rus, text_eng = color_texts[color]

    conflict = [c for c in colors if c != color]
    assert color not in conflict
    conflict = [mod_name + c for c in conflict]
    conflict = ','.join(conflict)
    return (f'' +
            f'Name={mod_name}{color}' + '\n' +
            f'Author=denball' + '\n' +
            f'Conflict={conflict}' + '\n' +
            f'Priority={priority}' + '\n' +
            f'Dependence=' + '\n' +
            f'Section={section_rus}' + '\n' +
            f'SectionEng={section_eng}' + '\n' +
            f'Languages=Rus,Eng' + '\n' +
            f'SmallDescription=Перекрашивает интерфейс в <color={rgb}>{text_rus}</color> цвет. <color=0,132,15>(легален)</color>' + '\n' +
            f'FullDescription=Перекрашивает интерфейс в <color={rgb}>{text_rus}</color> цвет. <color=0,132,15>(легален)</color>' + '\n' +
            f'SmallDescriptionEng=Recolors interface in <color={rgb}>{text_eng}</color> color. <color=0,132,15>(legal)</color>' + '\n' +
            f'FullDescriptionEng=Recolors interface in <color={rgb}>{text_eng}</color> color. <color=0,132,15>(legal)</color>' + '\n' +
            f'')


def get_special_module_info_content(special_mod_name, colors):
    return (f'' +
            f'Name={mod_name}_{special_mod_name}' + '\n' +
            f'Author=denball' + '\n' +
            f'Conflict=' + '\n' +
            f'Priority={priority}' + '\n' +
            f'Dependence={special_mod_name}' + '\n' +
            f'Section={section_rus}' + '\n' +
            f'SectionEng={section_eng}' + '\n' +
            f'Languages=Rus,Eng' + '\n' +
            f'SmallDescription=Добавляет совместимость с модом <color={spec_mod_rgb}>{special_mod_name}</color> для <color={mod_rgb}>{mod_name}</color>. <color=0,132,15>(легален)</color>' + '\n' +
            f'SmallDescription=<color={attention_rgb}>Внимание! Не включать без мода на перекраску интерфейса</color>' + '\n' +
            f'FullDescription=Добавляет совместимость с модом <color={spec_mod_rgb}>{special_mod_name}</color> для <color={mod_rgb}>{mod_name}</color>.' + '\n' +
            f'FullDescription=<color=0,132,15>(легален)</color>' + '\n' +
            f'FullDescription=<clr><clrEnd>' + '\n' +
            f'FullDescription=<color={attention_rgb}>Внимание! Не включать без одного из модов на перекраску интерфейса</color> <color={mod_rgb}>UIRecolor</color><color={attention_rgb}>!</color>' + '\n' +
            f'SmallDescriptionEng=Provides compatibility with <color={spec_mod_rgb}>{special_mod_name}</color> mod for <color={mod_rgb}>{mod_name}</color>. <color=0,132,15>(legal)</color>' + '\n' +
            f'SmallDescriptionEng=<color={attention_rgb}>Attention! Do not enable without mod for recoloring the interface</color>' + '\n' +
            f'FullDescriptionEng=Provides compatibility with <color={spec_mod_rgb}>{special_mod_name}</color> mod for <color={mod_rgb}>{mod_name}</color>.' + '\n' +
            f'FullDescriptionEng=<color=0,132,15>(legal)</color>' + '\n' +
            f'FullDescriptionEng=<clr><clrEnd>' + '\n' +
            f'FullDescriptionEng=<color={attention_rgb}>Attention! Do not enable without one of the mods for recoloring the interface</color><color={mod_rgb}>UIRecolor</color><color={attention_rgb}>!</color>' + '\n' +
            f'')


def get_install_content(mod, pkg_postfix=''):
    pkg_rel_path = mod_path + mod_name + mod + '/' + mod_name + pkg_postfix + '.pkg'
    return (
        'Packages {\n' +
        f'    Package={pkg_rel_path}\n' +
        '}'
    )


def folder_time(folder):
    result = 0.0
    for path, _, files in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            result = max(result, os.path.getmtime(filename))

    return result


def copy_file(src, dest):
    check_dir(dest)
    with open(dest, 'wb') as fout:
        with open(src, 'rb') as fin:
            fout.write(fin.read())


def check_dir(path):
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


def process():
    files = [f for f in os.listdir(_in) if os.path.isfile(os.path.join(_in, f))]
    dirs = [f for f in os.listdir(_in) if not os.path.isfile(os.path.join(_in, f))]

    for special_mod_name in special_mods:
        # Инфошки доп модов
        module_info_content = get_special_module_info_content(special_mod_name, dirs)
        outname = _out + mod_path + mod_name + '_' + special_mod_name + '/' + 'ModuleInfo.txt'
        print(outname)
        check_dir(outname)
        with open(outname, 'wt', encoding='utf16') as fp:
            fp.write(module_info_content)

        # Кешдаты доп модов
        filename = _dats + f'CacheData_{special_mod_name}.txt'
        assert os.path.isfile(filename), f'File {filename} does not exist'
        outname = _out + mod_path + mod_name + '_' + special_mod_name + '/' + dat_prefix + 'CacheData.dat'
        print(outname)
        check_dir(outname)
        dat = DAT.from_txt(filename)
        dat.to_dat(outname, 'HDCache', sign=True)

    print()

    for file in files:
        if file.endswith('.txt'):
            if '_Main.txt' not in file: continue

            # Мейны основных модов
            color = file.replace('_Main.txt', '')
            filename = _in + file
            outname = _out + mod_path + mod_name + color + '/' + dat_prefix + 'Main.dat'
            print(outname)
            check_dir(outname)
            dat = DAT.from_txt(filename)
            dat.to_dat(outname, 'HDMain', sign=True)

    for directory in dirs:
        for pkg_postfix, install_postfix in [('', ''), ('_Rus', '_RUSSIAN'), ('_Eng', '_ENGLISH')]:
            # Инсталлы основных модов
            install_content = get_install_content(directory, pkg_postfix=pkg_postfix)
            if install_content:
                outname = _out + mod_path + mod_name + directory + '/' + f'INSTALL{install_postfix}.TXT'
                print(outname)
                check_dir(outname)
                with open(outname, 'wt', encoding='utf16') as fp:
                    fp.write(install_content)

        # Инфошки основных модов
        module_info_content = get_module_info_content(directory, dirs)
        outname = _out + mod_path + mod_name + directory + '/' + 'ModuleInfo.txt'
        print(outname)
        check_dir(outname)
        with open(outname, 'wt', encoding='utf16') as fp:
            fp.write(module_info_content)

        # Кешдаты основных модов
        filename = _dats + 'CacheData.txt'
        outname = _out + mod_path + mod_name + directory + '/' + dat_prefix + 'CacheData.dat'
        print(outname)
        check_dir(outname)
        dat = DAT.from_txt(filename)
        dat.to_dat(outname, 'HDCache', sign=True)

    print()

    # Пакеты основных модов
    for directory in dirs:
        for folder, pkg_postfix in [('common', ''), ('rus', '_Rus'), ('eng', '_Eng')]:
            fullpath = _in + directory + '/' + folder
            pkg_rel_path = mod_path + mod_name + directory + '/' + mod_name + pkg_postfix + '.pkg'
            outname = _out + pkg_rel_path
            if not rewrite \
                and os.path.isfile(outname) \
                and os.path.getmtime(outname) > folder_time(fullpath):
                continue

            check_dir(outname)
            open(outname, 'wb').close()
            print(outname)

            pkg = PKG.from_dir(fullpath)
            if COMPRESS_PKG:
                pkg.compress()
            pkg.metadata = f'[[[Package for mod {mod_name + directory}. Author: denball. ({time.ctime()})]]]'.encode()
            pkg.to_pkg(outname)

        input_dir = _in + directory + '/Matrix'
        output_dir = _out + mod_path + mod_name + directory + '/Matrix'

        try:
            shutil.rmtree(output_dir)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)

        try:
            print(output_dir)
            shutil.copytree(input_dir, output_dir)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    if PROFILE:
        import cProfile
        import pstats
        import io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

    process()

    if PROFILE:
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.TIME  # CALLS CUMULATIVE FILENAME LINE NAME NFL PCALLS STDNAME TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        with open('logs/time_profiling_3_4.log', 'wt') as file:
            file.write(s.getvalue())