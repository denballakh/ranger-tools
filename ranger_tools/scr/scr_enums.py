from enum import IntEnum, IntFlag

__all__ = [
    'RACE',
    'RACE_FLAG',
    'OWNER_FLAG',
    'SHIP_TYPE_FLAG',
    'ECONOMY_FLAG',
    'GOVERNMENT_FLAG',
    'WEAPON',
    'VAR_TYPE',
    'FRIENDSHIP',
    'PLACE_TYPE',
    'MOVE_TYPE',
    'OP_TYPE',
    'RELATION',
    'ETHER_TYPE',
    'ITEM_TYPE',
    'EQUIPMENT_TYPE',
]

class RACE(IntEnum):
    MALOC = 0
    PELENG = 1
    PEOPLE = 2
    FEI = 3
    GAAL = 4
    KLING = 5
    NONE = 6
    PIRATECLAN = 7

class RACE_FLAG(IntFlag):
    USE = 1

    MALOC = 2
    PELENG = 4
    PEOPLE = 8
    FEI = 16
    GAAL = 32

class OWNER_FLAG(IntFlag):
    USE = 1

    MALOC = 2
    PELENG = 4
    PEOPLE = 8
    FEI = 16
    GAAL = 32

    KLING = 64
    NONE = 128
    PIRATECLAN = 256

    AS_PLAYER = 512

class SHIP_TYPE_FLAG(IntFlag):
    USE = 1

    RANGER = 1 << 1
    WARRIOR = 1 << 2
    PIRATE = 1 << 3
    TRANSPORT = 1 << 4
    LINER = 1 << 5
    DIPLOMAT = 1 << 6

    BLAZER_K0 = 1 << 7
    BLAZER_K1 = 1 << 8
    BLAZER_K2 = 1 << 9
    BLAZER_K3 = 1 << 10
    BLAZER_K4 = 1 << 11
    BLAZER_K5 = 1 << 12
    BLAZER_K6 = 1 << 26
    BLAZER_K7 = 1 << 27

    KELLER_K0 = 1 << 13
    KELLER_K1 = 1 << 14
    KELLER_K2 = 1 << 15
    KELLER_K3 = 1 << 16
    KELLER_K4 = 1 << 17
    KELLER_K5 = 1 << 18
    KELLER_K6 = 1 << 28
    KELLER_K7 = 1 << 29

    TERRON_K0 = 1 << 19
    TERRON_K1 = 1 << 20
    TERRON_K2 = 1 << 21
    TERRON_K3 = 1 << 22
    TERRON_K4 = 1 << 23
    TERRON_K5 = 1 << 24
    TERRON_K6 = 1 << 30
    TERRON_K7 = 1 << 31

    TRANCLUCATOR = 1 << 25

class ECONOMY_FLAG(IntFlag):
    USE = 1

    AGRICULTURE = 2
    INDUSTRIAL = 4
    MIXED = 8

class GOVERNMENT_FLAG(IntFlag):
    USE = 1

    ANARCHY = 2
    DICTATORSHIP = 4
    MONARCHY = 8
    REPUBLIC = 16
    DEMOCRACY = 32

class WEAPON(IntEnum):
    UNDEF = 0
    YES = 1
    NO = 2

class VAR_TYPE(IntEnum):
    UNKNOWN = 0
    INTEGER = 1
    DWORD = 2
    FLOAT = 3
    STRING = 4
    ARRAY = 9

class FRIENDSHIP(IntEnum):
    FREE = 0
    HELP = 1

class PLACE_TYPE(IntEnum):
    FREE = 0
    NEAR_PLANET = 1
    IN_PLANET = 2
    TO_STAR = 3
    NEAR_ITEM = 4
    FROM_SHIP = 5

class MOVE_TYPE(IntEnum):
    NONE = 0
    MOVE = 1
    FOLLOW = 2
    JUMP = 3
    LANDING = 4
    FREE = 5

class OP_TYPE(IntEnum):
    NORMAL = 0
    INIT = 1
    GLOBAL = 2
    DIALOGBEGIN = 3

class ETHER_TYPE(IntEnum):
    GALAXY = 0
    ETHER = 1
    SHIP = 2
    QUEST = 3
    QUESTOK = 4
    QUESTCANCEL = 5

class RELATION(IntEnum):
    WAR = 0
    BAD = 1
    NORMAL = 2
    GOOD = 3
    BEST = 4
    NOCHANGE = 5

class ITEM_TYPE(IntEnum):
    EQUIPMENT = 0  #, "Equipment"
    WEAPON = 1  #, "Weapon"
    GOODS = 2  #, "Goods"
    ARTIFACT = 3  #, "Artifact"
    USELESS = 4  #, "Useless"
    UNKNOWN = 5  #, "Unknown"

class EQUIPMENT_TYPE(IntEnum):
    FUELTANK = 0  #, "FuelTank"
    ENGINE = 1  #, "Engine"
    RADAR = 2  #, "Radar"
    SCANNER = 3  #, "Scaner"
    REPAIRROBOT = 4  #, "RepairRobot"
    CARGOHOOK = 5  #, "CargoHook"
    DEFGENERATOR = 6  #, "DefGenerator"

