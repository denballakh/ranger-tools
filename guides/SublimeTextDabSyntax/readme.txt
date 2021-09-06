Установка синтаксиса для подсветки скриптового языка и датников для Sublime Text 3:

Файл `dab.sublime-syntax` и `Monokai Classic.sublime-color-scheme` нужно положить по такому пути:
    %APPDATA%\Sublime Text 3\Packages\User
В случае portable-версии файлы нужно положить сюда:
    Папка программы\Data\Packages\User

Для нормальной работы нужно поставить тему "Monokai Pro":
- Tools > Install Package Control
- Preferences > Package Control, выбираем "Install Package"
- пишем "Monokai Pro", выбираем первую строку
- Preferences > Select Color Scheme, выбираем "Monokai Classic"
Если вы не хотите ставить новую тему, то можно сделать так:
- Preferences > Customize Color Scheme, откроется новый файл
- Вставьте в этот файл содержимое файла `Monokai Classic.sublime-color-scheme`, сохраните файл

После этого синтаксис с подсветкой будет автоматически включаться для некоторых открываемых файлов (.dump, .log).
Если этого не произошло, то можно вручную включить синтаксис для данного файла: View > Syntax > Dab's Code.

Автоматически открываемые расширения можно поменять в начале файла `dab.sublime-syntax`.
Также в этом файле можно поменять цвет подсветки операторов, нужно поправить 56 строку.

Все это работает и для Sublime Text 4.
