import re

from .scr import SCR
from .svr import SVR
from .enums import *


def scr_to_svr(scr: SCR) -> SVR:
    tr: list[tuple[str, str]] = []

    def get_op(svr, text):
        op = svr.add('Top')
        op.type = OP_TYPE.NORMAL
        op.expression = text.strip().replace('\'', '"')

        # strings = re.findall('"([^"]*)"|\'([^\']*)\'', op.expression)
        strings = re.findall('".*?"|\'.*?\'', op.expression)
        # print(strings)

        for s_ in strings:
            s = s_[1:-1]
            if s == 'Ship.Akrin.':
                print(1)

            flag = 1
            for _, ts in tr:
                if ts == s:
                    flag = 0
                    break
            if flag:
                if len(tr) == 0:
                    tid = '0'
                else:
                    tid = str(int(tr[-1][0]) + 1)
                print(s)
                tr.append((tid, s))

        return op

    assert scr.version == 7
    svr = SVR()
    svr.viewpos.x = -100
    svr.viewpos.y = -100

    svr.name = "script_name"
    svr.filename = "D:\\script.scr"

    svr.textfilenames[0][1] = 'D:\\script_rus.txt'
    svr.translations = tr

    for scr_var in scr.globalvars:
        svr_var = svr.add("TVar")
        svr_var.text = scr_var.name
        svr_var.type = VAR_TYPE_DECOMPILATION[scr_var.type]
        svr_var.init_value = str(scr_var.value)
        svr_var.is_global = True

    local_vars_exclude = []
    for s in scr.stars:
        for p in s.planets:
            local_vars_exclude.append(p.name)
        local_vars_exclude.append(s.name)
    for s in scr.states:
        local_vars_exclude.append(s.name)
    for s in scr.dialogs:
        local_vars_exclude.append(s.name)
    for s in scr.groups:
        local_vars_exclude.append(s.name)
    for s in scr.places:
        local_vars_exclude.append(s.name)
    for s in scr.items:
        local_vars_exclude.append(s.name)

    for scr_var in scr.localvars:
        if scr_var.name in local_vars_exclude:
            continue
        svr_var = svr.add("TVar")
        svr_var.text = scr_var.name
        svr_var.type = VAR_TYPE_DECOMPILATION[scr_var.type]
        svr_var.init_value = str(scr_var.value)
        svr_var.is_global = False

    if scr.globalcode:
        code = get_op(svr, scr.globalcode)
        code.type = OP_TYPE.GLOBAL

    if scr.initcode:
        code = get_op(svr, scr.initcode)
        code.type = OP_TYPE.INIT

    if scr.turncode:
        code = get_op(svr, scr.turncode)
        code.type = OP_TYPE.NORMAL

    if scr.dialogbegincode:
        code = get_op(svr, scr.dialogbegincode)
        code.type = OP_TYPE.DIALOGBEGIN

    for dialog in scr.dialogs:
        dial = svr.add('TDialog')
        dial.text = dialog.name
        if dialog.code:
            op = get_op(svr, dialog.code)
            svr.link(dial, op)

    for scr_msg in scr.dialog_msgs:
        msg = svr.add('TDialogMsg')
        msg.text = scr_msg.command
        if scr_msg.code:
            op = get_op(svr, scr_msg.code)
            svr.link(msg, op)

    for scr_answer in scr.dialog_answers:
        ans = svr.add('TDialogAnswer')
        ans.text = scr_answer.command
        ans.msg = scr_answer.answer
        if scr_answer.code:
            op = get_op(svr, scr_answer.code)
            svr.link(ans, op)

    for scr_star in scr.stars:
        star = svr.add('TStar')

        star.text = scr_star.name
        star.constellation = scr_star.constellation
        star.no_kling = scr_star.no_kling
        star.no_come_kling = scr_star.no_come_kling

        for scr_starlink in scr_star.starlinks:
            raise NotImplementedError

        for scr_planet in scr_star.planets:
            planet = svr.add('TPlanet')
            planet.text = scr_planet.name
            planet.race = scr_planet.race
            planet.owner = scr_planet.owner
            planet.economy = scr_planet.economy
            planet.government = scr_planet.government
            planet.range = scr_planet.range
            planet.dialog = scr_planet.dialog
            svr.link(planet, star)

        for scr_ship in scr_star.ships:
            ship = svr.add('TStarShip')
            ship.text = ''
            ship.count = scr_ship.count
            ship.owner = scr_ship.owner
            ship.type = scr_ship.type
            ship.is_player = scr_ship.is_player
            ship.speed = scr_ship.speed
            ship.weapon = scr_ship.weapon
            ship.cargohook = scr_ship.cargohook
            ship.emptyspace = scr_ship.emptyspace
            ship.status = scr_ship.status
            ship.strength = scr_ship.strength
            ship.ruins = scr_ship.ruins
            svr.link(ship, star)

    for scr_state in scr.states:
        state = svr.add('TState')
        state.text = scr_state.name
        state.type = scr_state.type
        state.obj = scr_state.object
        state.attack_groups = scr_state.attack
        state.item = scr_state.take_item
        state.take_all = scr_state.take_all
        state.out_msg = scr_state.out_msg
        state.in_msg = scr_state.in_msg

        state.type = scr_state.type
        state.type = scr_state.type
        if scr_state.ether:
            print(f'Dont know how to decompile ether: {scr_state.ether}')
        if scr_state.code:
            op = get_op(svr, scr_state.code)
            svr.link(state, op)

    for scr_gr in scr.groups:
        gr = svr.add('TGroup')
        gr.text = scr_gr.name
        gr.owner = scr_gr.owner
        gr.type = scr_gr.type
        gr.count = scr_gr.count
        gr.speed = scr_gr.speed
        gr.weapon = scr_gr.weapon
        gr.cargohook = scr_gr.cargohook
        gr.emptyspace = scr_gr.emptyspace
        gr.add_player = scr_gr.add_player
        gr.status = scr_gr.status
        gr.search_dist = scr_gr.search_distance
        gr.dialog = scr_gr.dialog
        gr.strength = scr_gr.strength
        gr.ruins = scr_gr.ruins

        planet = svr.find(scr_gr.planet)
        svr.link(gr, planet)

        state = svr.get('TState', scr_gr.state)
        svr.link(gr, state)

    for link in scr.grouplinks:
        print('untested code')

        l = svr.link(svr.get('TGroup', link.begin), svr.get('TGroup', link.end))
        l.relations = link.relations
        l.war_weight = link.war_weight

    for scr_place in scr.places:
        place = svr.add('TPlace')
        place.text = scr_place.name
        place.type = scr_place.type
        place.angle = scr_place.angle
        place.dist = scr_place.distance
        place.radius = scr_place.radius

        place.obj = scr_place.object
        if scr_place.star:
            star = svr.find(scr_place.star)
            svr.link(place, star)

    for scr_item in scr.items:
        item = svr.add('TItem')
        item.text = scr_item.name
        item.kind = scr_item.kind
        item.type = scr_item.type
        item.size = scr_item.size
        item.level = scr_item.level
        item.radius = scr_item.radius
        item.owner = scr_item.owner
        item.useless = scr_item.useless
        if scr_item.place:
            place = svr.find(scr_item.place)
            svr.link(item, place)

    return svr
