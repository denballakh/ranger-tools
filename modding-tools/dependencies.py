from __future__ import annotations

import os

GAME_ROOT = 'D:\\Games\\SteamLibrary\\steamapps\\common\\Space Rangers HD A War Apart\\'

section_colors = {
    'Прочие моды': '0.25,0.25,0.25',
    'Твики': '0.5,0.5,0.5',
    'Планетарные бои': '0.75,0.75,0.75',
    'Экспансия': '0,0,1',
    'Эволюция': '0,0,1',
    'Революция': '0,0,0.7',
    "Shu's Rangers": '0,1,0',
    'Солянка': '1,1,0',
    'HukMods': '1,1,0',
    'Den': '1,1,0',
    'КОТянка': '0,0.5,0.5',
    "Fairan's Vision": '1,0.5,0',
    'default': '0,0,0',
}

Conflicts = set[frozenset[str]]
Dependencies = set[tuple[str, str]]
Mods = set[str]
Sections = dict[str, str]


def col2dot(col: str) -> str:
    return '#' + ''.join(f'{int(float(x) * 255):02X}' for x in col.split(','))


def mod2col(mod: str, sections: Sections) -> str:
    if mod in sections:
        section = sections[mod]
    else:
        section = 'default'
    return section_colors[section]


def convert_ini_to_dict(content: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for s in content.split('\n'):
        if not s:
            continue
        if '=' not in s:
            continue
        key, val = s.split('=', 1)
        if key in result:
            result[key] += '\n' + val
        else:
            result[key] = val
    return result


def get_mod_infos(root: str) -> tuple[Conflicts, Dependencies, Sections, Mods]:
    conflicts: Conflicts = set()
    dependencies: Dependencies = set()
    sections: Sections = {}
    mods: Mods = set()

    for path, _, files in os.walk(root + '/Mods/'):
        for file in files:
            if file != 'ModuleInfo.txt':
                continue
            filename = '/'.join([path, file]).replace('//', '/').replace('\\', '/')
            foldername = path.replace('\\', '/').replace('//', '/').split('/')[-1]
            # print(filename)
            try:
                with open(filename, 'rt', encoding='utf-16') as fp:
                    content = fp.read()
            except:
                try:
                    with open(filename, 'rt', encoding='cp1251') as fp:
                        content = fp.read()
                except Exception as exc:
                    print(f'Error in file {filename!r}: {exc!r}')
                    continue
            data = convert_ini_to_dict(content)
            name = data['Name']
            if name.lower() != foldername.lower():
                print(
                    f'Error: mod name {name!r} doesnt match folder name {foldername!r}. Skipping...'
                )
                continue
            sections[name] = data['Section']
            mods |= {name}
            if 'Conflict' in data and data['Conflict']:
                for conf_name in data['Conflict'].replace(' ', '').split(','):
                    conflicts |= {frozenset({name, conf_name})}
            if 'Dependence' in data and data['Dependence']:
                for dep_name in data['Dependence'].replace(' ', '').split(','):
                    dependencies |= {(dep_name, name)}

    return conflicts, dependencies, sections, mods


def get_wolfram_code(
    conflicts: Conflicts,
    dependencies: Dependencies,
    sections: Sections,
    mods: Mods,
) -> str:
    undirected = '\\[UndirectedEdge]'
    directed = '\\[DirectedEdge]'

    conf_s = ''
    for a, b in conflicts:
        conf_s += f'"{a}"' + undirected + f'"{b}"' + ','
    conf_s = conf_s[:-1]
    conf_s = 'conflicts = {' + conf_s + '};\n'

    dep_s = ''
    for a, b in dependencies:
        dep_s += f'"{b}"' + directed + f'"{a}"' + ','
    dep_s = dep_s[:-1]
    dep_s = 'dependencies = {' + dep_s + '};\n'

    col_s = ''
    for mod in mods:
        section = sections[mod]
        if section in section_colors:
            color = section_colors[section]
            col_s += f'"{mod}" -> ' + '{' + color + '},'

    col_s = col_s[:-1]
    col_s = 'colors = {' + col_s + ', _->{' + section_colors['default'] + '}' + '};\n'

    code = R'''


    conflictsColored = Table[Style[x, Red], {x, conflicts}];
    dependenciesColored = Table[Style[x, Blue], {x, dependencies}];

    f[{xc_, yc_}, name_, {w_, h_}] := {
        RGBColor @@ (name /. colors),
        Disk[{xc, yc}, (w+h)/2]
    };
    g = Graph[
        Join[conflictsColored, dependenciesColored],
        VertexLabels -> "Name",
        ImageSize -> 2000,
        VertexShapeFunction -> f
    ];
    img = Image[
        g,
        ImageSize -> 2000
    ]
    '''

    result = conf_s + dep_s + col_s + code

    return result


def get_dot_code(
    conflicts: Conflicts,
    dependencies: Dependencies,
    sections: Sections,
    mods: Mods,
) -> str:
    sep = ';\n'

    used_mods: set[str] = set()
    for conflict in conflicts:
        used_mods |= set(conflict)
    for dep in dependencies:
        used_mods |= set(dep)

    conflicts_s = sep.join(
        ' -> '.join(y.replace('&', '') for y in x)
        + '[arrowhead=none, color=red, constraint=false, len=2.0]'
        for x in conflicts
    )
    dependencies_s = sep.join(
        ' -> '.join(y.replace('&', '') for y in x) + '[color=blue, constraint=false, len=2.0]'
        for x in dependencies
    )
    nodes = sep.join(
        node.replace('&', '')
        + f' [label="", xlabel={node} shape=circle, fixedsize=true, fontname="Consolas Bold", style=filled, fillcolor="{col2dot(mod2col(node, sections))}"]'
        for node in used_mods
    )

    return f'digraph G {{ mode="sgd"; \n{nodes + sep + conflicts_s + sep + dependencies_s}\n}}'


def generate_wolfram_script() -> None:
    code = get_wolfram_code(*get_mod_infos(GAME_ROOT))
    with open('_dependencies.wl', 'wt', encoding='utf-8') as file:
        file.write(code)


def generate_dot_image() -> None:
    code = get_dot_code(*get_mod_infos(GAME_ROOT))
    filename = '_dependencies.dot'
    output = filename.replace(".dot", ".png")
    with open(filename, 'wt', encoding='utf-8') as file:
        file.write(code)
    os.system(f'neato -Tpng -o {output} {filename}')
    os.system(f'{output}')


if __name__ == '__main__':
    generate_wolfram_script()
    # generate_dot_image()
    print('done')
    input()
    os._exit(0)
