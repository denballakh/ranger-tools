'''
Создает папки модов, готовых к использованию к игре
'''

import time
import shutil
from pathlib import Path
import textwrap

from rangers.pkg import PKG
from rangers.dat import DAT

import config

COMPRESS_PKG = config.COMPRESS_PKG

color_texts = {
    'Red': ('150,0,0', 'красный', 'red'),
    'Blue': ('0,0,150', 'синий', 'blue'),
    'Green': ('0,150,0', 'зеленый', 'green'),
    # 'LightPink': ('188,134,162', 'светло-розовый', 'light pink'),
    'Yellow': ('150,150,0', 'желтый', 'yellow'),
    'Magenta': ('150,0,150', 'пурпурный', 'magenta'),
    'Orange': ('150,75,0', 'оранжевый', 'orange'),
    'Cyan': ('0,191,191', 'голубой', 'orange'),
    'Grey': ('127,127,127', 'серый', 'grey'),
    'DarkGrey': ('63,63,63', 'темно-серый', 'dark-grey'),
    'Kling': ('0,127,0', 'клисанский', 'kling'),
    'DarkGreen': ('0,90,0', 'темно-зеленый', 'dark-green'),
    'Peleng': ('90,120,0', 'пеленгский', 'peleng'),
    'Fei': ('120,0,100', 'фэянский', 'fei'),
    #
    'Neon': ('0,255,255', 'неоновый', 'neon'),
    # 'Neon2': ('255,255,0', 'неоновый2', 'neon2'),
    # 'Neon3': ('0,255,255', 'неоновый3', 'neon3'),
}

priority = 11

mod_path = Path('Mods/Den/Den_UIRecolor/')
mod_name = 'DenUIRecolor'
section_rus = 'Den'
section_eng = 'Den'

dat_prefix = 'CFG/'
pkg_prefix = 'DATA/'


_dats = config._dats
_in = config._3
_out = config._4


special_mods = {
    # name: priority
    'ShuKlissan': 5,
    'ExpInfoCenter': 1,
    'ExtraArtSlots': 10,
    'Mod_Interface': 2,
}

spec_mod_rgb = '0,150,50'
mod_rgb = '88,188,192'
attention_rgb = '249,18,18'

additional_conflicts = [
    f'UIRecolor{x}'
    for x in (
        'Blue',
        'DarkGrey',
        'Green',
        'Grey',
        'Red',
        '_ShuKlissan',
        '_ExpInfoCenter',
        'Magenta',
        'Orange',
        'Yellow',
        'Neon',
    )
]

legal_rgb = '0,132,15'
legal_rus = 'легален'
legal_eng = 'legal'

legal_mod_rus = f'<color={legal_rgb}>({legal_rus})</color>'
legal_mod_rus_short = legal_mod_rus

legal_mod_eng = f'<color={legal_rgb}>({legal_eng})</color>'
legal_mod_eng_short = legal_mod_eng


def get_module_info_content(color: str, colors: list[str]) -> str | None:
    if color not in color_texts:
        print(f'Color {color} not in known colors: {list(color_texts)}')
        return None

    if color not in colors:
        print(f'Color {color} not in list of mods colors: {colors}')
        return None

    rgb, text_rus, text_eng = color_texts[color]

    conflict = [c for c in colors if c != color]
    assert color not in conflict
    conflict = [mod_name + c for c in conflict]
    conflicts = ','.join(conflict + additional_conflicts)

    return textwrap.dedent(
        f'''
        Name={mod_name}{color}
        Author=denball,Killi
        Conflict={conflicts}
        Priority={priority}
        Dependence=
        Section={section_rus}
        SectionEng={section_eng}
        Languages=Rus,Eng
        SmallDescription=Перекрашивает интерфейс в <color={rgb}>{text_rus}</color> цвет. {legal_mod_rus_short}
        FullDescription=Перекрашивает интерфейс в <color={rgb}>{text_rus}</color> цвет. {legal_mod_rus}
        // FullDescription=<color=255,0,0>Внимание! Требуется включенный аппаратный рендер в настройках!</color>
        SmallDescriptionEng=Recolors interface in <color={rgb}>{text_eng}</color> color. {legal_mod_eng_short}
        FullDescriptionEng=Recolors interface in <color={rgb}>{text_eng}</color> color. {legal_mod_eng}
        '''
    )


def get_special_module_info_content(special_mod_name: str, colors: list[str]) -> str | None:
    if special_mod_name not in special_mods:
        print(
            f'Special mod name {special_mod_name} not in known special mods: {list(special_mods)}'
        )
        return None

    return textwrap.dedent(
        f'''
        Name={mod_name}_{special_mod_name}
        Author=denball
        Conflict=
        Priority={special_mods[special_mod_name] + 1}
        Dependence={special_mod_name}
        Section={section_rus}
        SectionEng={section_eng}
        Languages=Rus,Eng
        SmallDescription=Добавляет совместимость с модом <color={spec_mod_rgb}>{special_mod_name}</color> для <color={mod_rgb}>{mod_name}</color>. {legal_mod_rus_short}
        SmallDescription=<color={attention_rgb}>Внимание! Не включать без мода на перекраску интерфейса</color>
        FullDescription=Добавляет совместимость с модом <color={spec_mod_rgb}>{special_mod_name}</color> для <color={mod_rgb}>{mod_name}</color>.
        FullDescription={legal_mod_rus}
        FullDescription=<clr><clrEnd>
        FullDescription=<color={attention_rgb}>Внимание! Не включать без одного из модов на перекраску интерфейса</color> <color={mod_rgb}>UIRecolor</color><color={attention_rgb}>!</color>
        SmallDescriptionEng=Provides compatibility with <color={spec_mod_rgb}>{special_mod_name}</color> mod for <color={mod_rgb}>{mod_name}</color>. {legal_mod_eng_short}
        SmallDescriptionEng=<color={attention_rgb}>Attention! Do not enable without mod for recoloring the interface</color>
        FullDescriptionEng=Provides compatibility with <color={spec_mod_rgb}>{special_mod_name}</color> mod for <color={mod_rgb}>{mod_name}</color>.
        FullDescriptionEng={legal_mod_eng}
        FullDescriptionEng=<clr><clrEnd>
        FullDescriptionEng=<color={attention_rgb}>Attention! Do not enable without one of the mods for recoloring the interface</color> <color={mod_rgb}>UIRecolor</color><color={attention_rgb}>!</color>
        '''
    )


def get_install_content(mod: str, pkg_postfix: str = '') -> str:
    pkg_rel_path = mod_path / (mod_name + mod) / (mod_name + pkg_postfix + '.pkg')
    return f'Packages {{\n    Package={pkg_rel_path}\n}}\n'


def folder_time(folder: Path) -> float:
    result = 0.0
    for file in folder.rglob('**/*'):
        if not file.is_file():
            continue
        result = max(result, file.stat().st_mtime)

    return result



def main() -> None:
    files = [f.relative_to(_in) for f in _in.glob('*') if f.is_file()]
    dirs = [f.relative_to(_in) for f in _in.glob('*') if f.is_dir()]

    for special_mod_name in special_mods:
        # Инфошки доп модов
        module_info_content = get_special_module_info_content(special_mod_name, [*map(str,dirs)])
        if module_info_content is not None:
            outname = _out / mod_path / (mod_name + '_' + special_mod_name) / 'ModuleInfo.txt'
            print(outname)
            outname.parent.mkdir(parents=True, exist_ok=True)
            with open(outname, 'wt', encoding='utf16') as fp:
                fp.write(module_info_content)

        # Кешдаты доп модов
        filename = _dats / f'CacheData_{special_mod_name}.txt'
        assert filename.is_file(), f'File {filename} does not exist'
        outname = (
            _out / mod_path / (mod_name + '_' + special_mod_name) / dat_prefix / 'CacheData.dat'
        )
        print(outname)
        outname.parent.mkdir(parents=True, exist_ok=True)
        dat = DAT.from_txt(Path(filename))
        dat.to_dat(Path(outname), 'HDCache', sign=True)

    print()

    for file in files:
        if file.suffix == '.txt':
            if '_Main.txt' not in file.name:
                continue

            # Мейны основных модов
            color = file.name.replace('_Main.txt', '')
            filename = _in / file
            outname = _out / mod_path / (mod_name + color) / dat_prefix / 'Main.dat'
            print(outname)
            outname.parent.mkdir(parents=True, exist_ok=True)
            dat = DAT.from_txt(Path(filename))
            dat.to_dat(Path(outname), 'HDMain', sign=True)

    for directory in dirs:
        for pkg_postfix, install_postfix in [('', ''), ('_Rus', '_RUSSIAN'), ('_Eng', '_ENGLISH')]:
            # Инсталлы основных модов
            install_content = get_install_content(str(directory), pkg_postfix=pkg_postfix)
            if install_content:
                outname = (
                    _out / mod_path / (mod_name + str(directory)) / f'INSTALL{install_postfix}.TXT'
                )
                print(outname)
                outname.parent.mkdir(parents=True, exist_ok=True)
                with open(outname, 'wt', encoding='utf16') as fp:
                    fp.write(install_content)

        # Инфошки основных модов
        module_info_content = get_module_info_content(str(directory), [*map(str,dirs)])
        if module_info_content is not None:
            outname = _out / mod_path / (mod_name + str(directory)) / 'ModuleInfo.txt'
            print(outname)
            outname.parent.mkdir(parents=True, exist_ok=True)
            with open(outname, 'wt', encoding='utf16') as fp:
                fp.write(module_info_content)

        # Кешдаты основных модов
        filename = _dats / 'CacheData.txt'
        outname = _out / mod_path / (mod_name + str(directory)) / dat_prefix / 'CacheData.dat'
        print(outname)
        outname.parent.mkdir(parents=True, exist_ok=True)
        dat = DAT.from_txt(filename)
        dat.to_dat(outname, 'HDCache', sign=True)

    print()

    # Пакеты основных модов
    for directory in dirs:
        for folder, pkg_postfix in [('common', ''), ('rus', '_Rus'), ('eng', '_Eng')]:
            fullpath = _in / directory / folder
            pkg_rel_path = mod_path / (mod_name + str(directory)) / (mod_name + pkg_postfix + '.pkg')
            outname = _out / pkg_rel_path
            if outname.is_file() and outname.stat().st_mtime > folder_time(fullpath):
                continue

            outname.parent.mkdir(parents=True, exist_ok=True)
            outname.touch()
            print(outname)

            pkg = PKG.from_folder(Path(fullpath))
            if COMPRESS_PKG:
                pkg.compress()
            pkg.metadata = f'[[[Package for mod {mod_name + str(directory)}. Author: denball. ({time.ctime()})]]]'.encode()
            pkg.to_file(Path(outname))

        # input_dir = _in / directory / 'Matrix'
        # output_dir = _out / mod_path / (mod_name + str(directory)) / 'Matrix'

        # try:
        #     shutil.rmtree(output_dir)
        # except FileNotFoundError:
        #     pass
        # except Exception as e:
        #     print(e)

        # try:
        #     print(output_dir)
        #     shutil.copytree(input_dir, output_dir)
        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    main()
