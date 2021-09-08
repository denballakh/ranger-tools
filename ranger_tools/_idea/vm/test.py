from pprint import pprint

from ranger_tools.io import Buffer

import vm

o = vm.OpCode

class HelperClass:
    def __init__(self, *values):
        self.values = values

class Lbl(HelperClass): pass
class Ref(HelperClass): pass
class Data(HelperClass): pass
class Filler(HelperClass): pass

class DefConst(HelperClass): pass
class Const(HelperClass): pass

class Cint(HelperClass): pass
class Cuint(HelperClass): pass

# class Cbyte(HelperClass): pass
# class C(HelperClass): pass


def generate_mem(data):
    buf = vm.VMMemory(size=0)
    const_values: dict[str, int] = {}
    const_refs: dict[int, str] = {}


    items_index = 0

    while items_index < len(data):
        item = data[items_index]

        if isinstance(item, Lbl):
            name = item.values[0]
            assert name not in const_values
            const_values[name] = buf.pos

        elif isinstance(item, Ref):
            name = item.values[0]
            const_refs[buf.pos] = name
            buf.write_uint(0xFFFFFFFF)

        elif isinstance(item, Cuint):
            value = item.values[0]
            buf.write_uint(value)

        elif isinstance(item, Cint):
            value = item.values[0]
            buf.write_int(value)

        elif isinstance(item, Data):
            name = item.values[0]
            size = item.values[1]
            assert name not in const_values
            const_values[name] = buf.pos
            buf.write(b'\0' * size)

        elif isinstance(item, Filler):
            size = item.values[0]
            buf.write(b'\0' * size)

        elif isinstance(item, DefConst):
            name = item.values[0]
            value = item.values[1]
            const_values[name] = value

        elif isinstance(item, Const):
            name = item.values[0]
            const_refs[buf.pos] = name
            buf.write_uint(0xFFFFFFFF)

        else:
            buf.write_byte(item)

        items_index += 1

    for pos, name in const_refs.items():
        assert name in const_values
        buf.write_uint(const_values[name], pos=pos)

    pprint(const_values)

    buf.pos = 1
    return buf



program = [
o.ZER, # wrong opcode at 0 address

# entry point here:
o.LDC, Ref('entry_point'), o.JMP,



o.ZER,
Lbl('exit'),
    o.HLT,
o.ZER,



Data('call_stack_index', 4),
Data('call_stack', 64 * 4),
DefConst('call_stack_size', 64),

o.ZER,
Lbl('call'), # ... callee caller
    DefConst('call_fix_', 6),

    # reading call stack index
    o.LDC, Ref('call_stack_index'),
    o.RMM,
    o.DUP,
    o.LDC, Cint(1),
    o.ADD,
    o.LDC, Ref('call_stack_index'),
    o.WMM,
    # increasing CSI
    # o.RMM,
    # o.LDC, Ref('call_stack_index'),
    # o.WMM,


    # calculating ptr to addr
    o.LDC, Cint(4),
    o.MUL,
    o.LDC, Ref('call_stack'),
    o.ADD,

    # writing caller address
    o.SWP,
    o.LDC, Const('call_fix_'),
    o.ADD,
    o.SWP,
    o.WMM,


    # jump to callee address
    o.JMP,
o.ZER,




o.ZER,
Lbl('ret'), # ...
    o.LDC, Ref('call_stack_index'),
    o.RMM,
    o.LDC, Cint(-1),
    o.ADD,
    o.DUP,

    o.LDC, Cint(4),
    o.MUL,
    o.LDC, Ref('call_stack'),
    o.ADD,
    o.RMM,
    o.SWP,
    o.LDC, Ref('call_stack_index'),
    o.WMM,

    o.JMP,

o.ZER,




o.ZER,
Lbl('test_func'),
    o.LDC, Cint(222),
    o.LDC, Cint(333),
    o.LDC, Cint(444),
    o.PRT,
    o.PRT,
    o.PRT,

o.LDC, Ref('ret'), o.JMP,
o.ZER,



o.ZER,
Lbl('factorial'),
    o.DUP,
    o.LDC, Ref('fact_nonzero_arg'),
    o.JMZ,
    Lbl('fact_zero_arg'),
        o.POP,
        o.LDC, Cint(1),
        o.LDC, Ref('ret'), o.JMP,

    Lbl('fact_nonzero_arg'),
        o.DUP,
        o.LDC, Cint(1),
        o.SWP,
        o.SUB,

        o.LDC, Ref('factorial'), o.IPT,
        o.LDC, Ref('call'), o.JMP,

        o.MUL,
        o.LDC, Ref('ret'), o.JMP,
o.ZER,




o.ZER,
Lbl('entry_point'),
    o.LDC, Cint(70),

    o.LDC, Ref('factorial'), o.IPT,
    o.LDC, Ref('call'), o.JMP,

    o.PRT,

o.LDC, Ref('exit'), o.JMP,
o.ZER,
Lbl('_end'),


]

v = vm.VM()
v.memory = generate_mem(program)
# print(v.memory.data)
v.execute()

# @unique
# class OpCode(IntEnum):
#     # basic
#     ZER = 0
#     HLT = 1
#     NOP = 2

#     # io
#     PRT = 3

#     # stack
#     DUP = 4
#     POP = 5
#     GET = 6
#     ROT = 6

#     # const
#     LDC = 7

#     # mem
#     RMM = 8
#     WMM = 9

#     # jumps
#     IPT = 10
#     JMP = 11
#     JMZ = 12

#     # math
#     MUL = 13
#     DIV = 14
#     ADD = 15
#     SUB = 16

