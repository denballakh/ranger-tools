Конвертеры принимают файлы в папке `_input` и создают новые файлы в папке `_output`\
Чтобы запустить конвертер - запустите `run.bat`, лежащий в соответствующей папке.\
Запуск любого конвертера создаст папки `_input` и `_output`, если их не было.

**dat_sign_checker** - **Не работает**\
**dat_signer** - **Не работает**\
**dat_unsigner** - *Частично работает*

**dat_to_json** - особый формат\
**dat_to_txt** - совместимый с блокпаром формат
**txt_to_dat**

**gi_to_png** - поддерживаются не все форматы\
**png_to_gi** - по умолчанию в 32-битный подформат 0-го формата, можно настроить в файле

**hai_to_png**
**png_to_hai**

**json_to_robotcomplate** - `robotcomplate.dat` - файл в документах, хранит время прохождения карт\
**robotcomplate_to_json**

**folder_to_pkg** - по умолчанию максимальное сжатие, можно настроить в файле\
**pkg_to_folder**

**json_to_sav**\
**sav_to_json**

**json_to_qm**\
**qm_to_json**

**compile** - компилирует скрипты


Остальное:
**clear_files** - чистит папки `_input` и `_output` во всех конвертерах.\
**dependencies** - генерирует код для создания графа зависимостей и конфликтов модов. Необходим установленный пакет `Graphviz`.\
**key_brute_force** - перебирает ключи шифрования датников.
