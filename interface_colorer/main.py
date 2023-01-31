import os
import time as t
from time import time

def process() -> None:
    t0 = time()

    import _0_1
    import _1_2
    import _2_3
    import _3_4
    import clear_empty


    t1 = time()

    # _0_1.process()
    print()
    t2 = time()

    _1_2.main()
    print()
    t3 = time()

    _2_3.main()
    print()
    t4 = time()

    t.sleep(60)
    t5 = time()
    _3_4.main()
    print()
    t6 = time()


    print('\n' * 5)
    print(f'Import time: {round(t1 - t0, 3)} s')
    print(f'Conversion from game to png: {round(t2 - t1, 3)} s')
    print(f'Coloring time: {round(t3 - t2, 3)} s')
    print(f'Conversion from png to game: {round(t4 - t3, 3)} s')
    print(f'Packing to PKG: {round(t6 - t5, 3)} s')
    print(f'Waiting 10 seconds...')
    t.sleep(10)
    print(f'Empty files:\n')

    clear_empty.main()

    print()


if __name__ == "__main__":
    process()
