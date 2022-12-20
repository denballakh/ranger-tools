from __future__ import annotations
import time
from types import MappingProxyType
from typing import ClassVar, Final, Iterable, Mapping, Sequence

from pathlib import Path
import filecmp
import shutil
import subprocess
import os
import json

from .graphics.gi import GI
from .pkg import PKG
from .dat import DAT, DAT_SIGN_AVAILABLE

text_encoding: Final[str] = 'utf16'

if DAT_SIGN_AVAILABLE:
    legal_rus = '<color=0,132,15>(легален)</color>'
    legal_eng = '<color=0,132,15>(legal)</color>'
else:
    legal_rus = ''
    legal_eng = ''

stateless_rus: Final[str] = '<color=0,132,15>(можно подключать/отключать в течение партии)</color>'
stateless_eng: Final[str] = '<color=0,132,15>(can be enabled/disabled during the game)</color>'

unstable_rus: Final[str] = '<color=254,0,0>(нестабилен)</color>'
unstable_eng: Final[str] = '<color=254,0,0>(unstable)</color>'

dev_rus: Final[str] = '<color=254,0,0>(мод для создателей модов)</color>'
dev_eng: Final[str] = '<color=254,0,0>(mod for mods delelopers)</color>'

contentless_rus: Final[str] = '<color=254,0,0>(мод сам по себе контента не добавляет)</color>'
contentless_eng: Final[str] = '<color=254,0,0>(mod for delelopers)</color>'

warn_rus: Final[str] = '<color=254,127,0>Внимание! %s</color>'
warn_eng: Final[str] = '<color=254,127,0>Warning! %s</color>'

str_true: Final[str] = 'True'
str_false: Final[str] = 'False'


class ScriptCompilationError(Exception):
    ...


class ModBuilder:
    name: ClassVar[str]
    _src: Path

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} instance in {self._src}>'

    def build(self, src: Path, dst: Path) -> None:
        """
        src - folder of location of module source files
        dst - path to game folder
        """
        raise NotImplementedError

    def _build(self) -> None:
        return self.build(Path('.'), Path('.build'))

    def _folder_mtime(self, path: Path) -> float:
        return max(map(lambda file: file.stat().st_mtime, path.glob('**/*')))

    def png_to_gi(self, src: Path, dst: Path, fmt: int = 2, opt: int = 16) -> None:
        assert src.exists(), src
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            GI.from_png(src, fmt=fmt, opt=opt).to_file(dst)

    def pack_folder(self, src: Path, dst: Path, comp: int = 9) -> None:
        assert src.exists(), src
        if not dst.exists() or dst.stat().st_mtime < self._folder_mtime(src):
            dst.parent.mkdir(parents=True, exist_ok=True)
            pkg = PKG.from_folder(src)
            pkg.compress(comp)
            pkg.to_file(dst)

    def txt_to_dat(self, src: Path, dst: Path, fmt: str, sign: bool = False) -> None:
        assert src.exists()
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            DAT.from_txt(src).to_dat(dst, fmt=fmt, sign=sign)

    def str_to_dat(self, s: str, dst: Path, fmt: str, sign: bool = False) -> None:
        dst.parent.mkdir(parents=True, exist_ok=True)
        DAT.from_str(s).to_dat(dst, fmt=fmt, sign=sign)

    def json_to_dat(self, src: Path, dst: Path, fmt: str, sign: bool = False) -> None:
        assert src.exists(), src
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            DAT.from_json(src).to_dat(dst, fmt=fmt, sign=sign)

    def copy_file(self, src: Path, dst: Path) -> None:
        assert src.exists(), src
        if not dst.exists() or not filecmp.cmp(src, dst, shallow=True):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

    def copy_folder(self, src: Path, dst: Path) -> None:
        assert src.exists(), src
        for file in src.glob('**/*'):
            if not file.is_file():
                continue
            self.copy_file(file, dst / file.relative_to(src))

    def compile_script(self, src: Path, dst: Path, dst_text: Path) -> None:
        assert src.exists(), src
        if not dst.exists() or not dst_text.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst_text.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                [
                    'RScript.exe',
                    '--cli',
                    '--build',
                    '--full',
                    str(src.resolve()),
                    str(dst.resolve()),
                    str(dst_text.resolve()),
                ],
                check=True,
            )
            if result.returncode:
                raise ScriptCompilationError(result)

    def _apply_script_lang(
        self, lang: Path, script_text: Path, lang_dst: Path, script_name: str
    ) -> None:
        assert lang.exists(), lang
        assert script_text.exists(), script_text
        if (
            not lang_dst.exists()
            or lang_dst.stat().st_mtime < lang.stat().st_mtime
            or lang_dst.stat().st_mtime < script_text.stat().st_mtime
        ):
            lang_dat = DAT.from_file(lang).to_dict()
            text_dat = DAT.from_file(script_text).to_dict()
            lang_dat.setdefault('Script', {})
            lang_dat['Script'].setdefault(script_name, {})
            lang_dat['Script'][script_name].update(text_dat)
            DAT.from_dict(lang_dat).to_file(lang_dst, fmt='HDMain', sign=False)

    def _apply_script_main(self, main: Path, main_dst: Path, script_name: str) -> None:
        assert main.exists(), main
        if not main_dst.exists() or main_dst.stat().st_mtime < main.stat().st_mtime:
            print('compiling2')
            print(main)
            main_dat = DAT.from_file(main).to_dict()
            main_dat.setdefault('Data', {})
            main_dat['Data'].setdefault('Script', {})
            main_dat['Data']['Script'][script_name] = f'1,Script.{script_name}'
            DAT.from_dict(main_dat).to_file(main_dst, fmt='HDMain', sign=False)

    def _apply_script_cachedata(
        self, cachedata: Path, cachedata_dst: Path, script_name: str, script_rel_path: Path
    ) -> None:
        assert cachedata.exists(), cachedata
        if not cachedata_dst.exists() or cachedata_dst.stat().st_mtime < cachedata.stat().st_mtime:
            cachedata_dat = DAT.from_file(cachedata).to_dict()
            cachedata_dat.setdefault('Script', {})
            cachedata_dat['Script'][script_name] = str(script_rel_path)
            DAT.from_dict(cachedata_dat).to_file(cachedata_dst, fmt='HDCache', sign=False)

    def get_tempdir(self) -> Path:
        tmp = Path('./.tmp/')
        tmp.mkdir(parents=True, exist_ok=True)
        return tmp

    def get_dummy_txt(self, name: str = '.dummy.txt') -> Path:
        tmp = self.get_tempdir()
        file = tmp / name
        file.touch(exist_ok=True)
        os.utime(file, (0, 0))
        return file

    def compile_script_and_patch_dats(
        self,
        dst: Path,
        rel_path: Path,
        script_src: Path,
        script_name: str,
        lang_rus_src: Path | None,
        lang_eng_src: Path | None,
        lang_text_eng_src: Path | None,
        cachedata_src: Path | None,
        main_src: Path | None,
    ) -> None:
        tmp = self.get_tempdir()

        script_dst = dst / 'DATA' / 'Script' / f'{script_name}.scr'
        lang_rus_dst = dst / 'CFG' / 'Rus' / 'Lang.dat'
        lang_eng_dst = dst / 'CFG' / 'Eng' / 'Lang.dat'
        main_dst = dst / 'CFG' / 'Main.dat'
        cachedata_dst = dst / 'CFG' / 'CacheData.dat'

        lang_text_rus_src = tmp / 'script_text_rus.txt'

        script_rel_path = rel_path / script_dst.relative_to(dst)

        self.compile_script(script_src, script_dst, lang_text_rus_src)

        if lang_rus_src is not None:
            self._apply_script_lang(lang_rus_src, lang_text_rus_src, lang_rus_dst, script_name)

        if lang_eng_src is not None and lang_text_eng_src is not None:
            self._apply_script_lang(lang_eng_src, lang_text_eng_src, lang_eng_dst, script_name)

        if main_src is not None:
            self._apply_script_main(main_src, main_dst, script_name)

        if cachedata_src is not None:
            self._apply_script_cachedata(cachedata_src, cachedata_dst, script_name, script_rel_path)

    def make_modinfo(self, data: Mapping[str, str | int]) -> str:
        result: list[str] = []

        for key, value in data.items():
            value = str(value)
            value_lines = value.splitlines()
            value_lines = list(map(str.strip, value_lines))
            for line in value_lines:
                if line:
                    result.append(f'{key}={line}')
                else:
                    result.append(f'{key}=<clr></clr>')

        return '\n'.join(result)

    def write_modinfo(self, path: Path, content: str | Mapping[str, str | int]) -> None:
        if isinstance(content, Mapping):
            content = self.make_modinfo(content)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=text_encoding)

    def x(
        self,
        name: str | None = None,
        no_normal_resources: bool = False,
        conflict: Iterable[str] = (),
        dependence: Iterable[str] = (),
        priority: int = 0,
        author_rus: str | None = None,
        author_eng: str | None = None,
        section_rus: str | None = None,
        section_eng: str | None = None,
        languages: str | None = None,
        small_description_rus: str | None = None,
        small_description_eng: str | None = None,
        full_description_rus: str | None = None,
        full_description_eng: str | None = None,
        default_language: str = 'Rus',
        extra: Mapping[str, str] = MappingProxyType({}),
    ) -> None:
        pass

    def write_install(self, path: Path, packages: Sequence[object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            'Packages {\n' + '\n'.join(map('    Package='.__add__, map(str, packages))) + '\n}',
            encoding=text_encoding,
        )

    def build_info(self, folder: Path) -> None:
        folder.mkdir(exist_ok=True)
        (folder / '.build_info.json').write_text(
            json.dumps(
                {
                    'time': time.time(),
                    'time_text': time.asctime(time.gmtime(time.time() + 3 * 3600)),
                },
                indent=4,
            )
        )
