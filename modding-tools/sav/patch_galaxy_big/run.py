from __future__ import annotations
from typing import Any
import random as rnd
from pathlib import Path

try:
    from rangers.sav import SAV
except ImportError:
    raise NotImplementedError('no required code') from None

NEW_CONS = 50  # сколько секторов создать
NEW_STARS = 5  # сколько систем в каждом новом секторе создать
NEW_PLANETS = 3

_in = Path('_input/')
_out = Path('_output/')

_in.mkdir(exist_ok=True, parents=True)
_out.mkdir(exist_ok=True, parents=True)


def new_cons(id: int) -> dict[str, Any]:
    return dict(
        id=id,
        _09=True,
        _88=0,
        _0C=67.5,
        _10=10.2,
        stars_id=[],
        constellations_id=[],
        p_bound=[],
        p_bound_hidden=[],
        rect=[0, 0, 0, 0],
        point=[0, 0],
        lines=[],
        _80=[],
        _84=[],
    )


def new_star(id: int, con_id: int, planet: dict[str, Any]) -> dict[str, Any]:
    return dict(
        id=id,
        gen_seed=0,
        rnd_seed=0,
        name='#',
        pos=[rnd.randint(0, 150), rnd.randint(0, 100)],
        _01C=250,
        fon_image=rnd.randint(1, 5),
        planets=[planet],
        asteroids=[],
        ships=[],
        items_in_space=[],
        drop_list=[],
        missiles=[],
        con_id=con_id,
        _032='Process.Normal',
        battle=False,
        _040=10,
        _041=90,
        owner=rnd.randint(0, 4),
        _04A=0,
        series=rnd.randint(0, 2),
        custom_faction='',
        safe_radius=300.0,
        damage_radius=290.0,
        radius=250,
        graph_object_type='Star.0' + str(rnd.randint(0, 4)),
        _0F1=False,
        _080=0,
        _070=401,
        _074=61,
        _084=0,
        _088=0,
        _08C=0,
        _078=0,
        no_come_kling=False,
        _0DC=0,
        _0E0='',
        _0E4=[],
    )


def new_planet(id: int, rangers_cnt: int) -> dict[str, Any]:
    return dict(
        id=id,
        gen_seed=0,
        rnd_seed=0,
        name='new planet',
        pos=[rnd.randint(500, 1000), rnd.randint(500, 1000)],
        angle_speed=rnd.uniform(2, 7),
        _030=0,
        radius=10 * rnd.randint(6, 9),
        water_total=100,
        water_complete=0,
        land_total=100,
        land_complete=0,
        hill_total=100,
        hill_complete=0,
        orbit_cnt=0,
        is_visited=0,
        invention_levels=[1] * 20,
        cur_invention=1,
        cur_invention_points=10.0,
        _064=30,
        _065=10,
        population=200000,
        eco=rnd.randint(0, 2),
        _070=50000,
        owner=rnd.randint(0, 4),
        race=rnd.randint(0, 4),
        gov=rnd.randint(0, 2),
        goods=[
            dict(
                count=0,
                e_price=0,
                sell_price=0,
                buy_price=0,
                count_2=0,
                _100=0,
            )
            for i in range(8)
        ],
        relation_to_rangers=[100] * rangers_cnt,
        equipment_store_items=[],
        warriors=[],
        spawned_rangers_count=0,
        _11C=2,
        _120=0,
        _124=0,
        _128=0,
        graph_radius=60,
        graph_name='Planet.00' + str(rnd.randint(0, 4)),
        graph_planet_14=94,
        graph_planet_type=1,
        graph_planet_3C=9,
        _108=56,
        sputniks=[],
        gone_items=[],
        no_landing=False,
        no_shop_update=False,
        is_rogeria=False,
        _164_s='',
    )


def modify_sav(sav: SAV) -> None:
    sav_data = sav.data
    galaxy = sav_data['data3']
    cons_l = galaxy['cons']
    stars_l = galaxy['stars']

    con_id = cons_l[-1]['id']
    star_id = stars_l[-1]['id']
    planet_id = stars_l[-1]['planets'][-1]['id']
    rangers_cnt = len(galaxy['rangers'])

    for i in range(NEW_CONS):
        con_id += 1

        cons = new_cons(con_id)
        cons_l.append(cons)

        for i in range(NEW_STARS):
            star_id += 1

            planet_id += 1
            star = new_star(star_id, con_id, new_planet(planet_id, rangers_cnt))
            galaxy['planets'].append(planet_id)
            cons['stars_id'].append(star_id)
            stars_l.append(star)

            for i in range(NEW_PLANETS - 1):
                planet_id += 1
                planet = new_planet(planet_id, rangers_cnt)
                galaxy['planets'].append(planet_id)

                star['planets'].append(planet)


# from rangers._drafts.decorator import profile

# @profile(filename='_prof.log', sortby='calls')
def main() -> None:
    for filename in _in.rglob('*.sav'):
        try:
            out_name = _out / filename.relative_to(_in)

            print(f'{filename} -> {out_name}')

            sav = SAV.from_file(filename)
            modify_sav(sav)

            out_name.parent.mkdir(exist_ok=True, parents=True)
            sav.to_file(out_name)
        except:
            import traceback

            traceback.print_exc()


if __name__ == '__main__':
    main()
