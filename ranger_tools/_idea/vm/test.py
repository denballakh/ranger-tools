from pprint import pprint

# from ranger_tools.io import Buffer

import vm

o = vm.OpCode

class HelperClass:
    def __init__(self, *values):
        self.values = values

    def x(self): pass
    def y(self): pass

class Lbl(HelperClass): pass
class Ref(HelperClass): pass
class Undef(HelperClass): pass

class Data(HelperClass): pass
class Filler(HelperClass): pass

class DefConst(HelperClass): pass
class Const(HelperClass): pass

class Cint(HelperClass): pass
class Cuint(HelperClass): pass

class Ret(HelperClass): pass
class Call(HelperClass): pass
class Jump(HelperClass): pass
class JumpIf(HelperClass): pass
class Func(HelperClass): pass

class Read(HelperClass): pass
class Write(HelperClass): pass

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

def generate_mem(data):
    buf = vm.VMMemory(size=0)
    const_values: dict[str, int] = {}
    const_refs: dict[int, str] = {}


    items_index = 0

    while data:
        item = data.pop(0)

        if isinstance(item, Lbl):
            name = item.values[0]
            assert name not in const_values
            const_values[name] = buf.pos

        elif isinstance(item, Ref):
            name = item.values[0]
            const_refs[buf.pos] = name
            buf.write_uint(0xFFFFFFFF) # будет перезаписано позже

        elif isinstance(item, Undef): # not implemented
            # name = item.values[0]
            # assert name in const_values
            # const_values[name] = None
            pass

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

        elif isinstance(item, Const): # ничем не отличается от Ref
            name = item.values[0]
            const_refs[buf.pos] = name
            buf.write_uint(0xFFFFFFFF) # будет перезаписано позже

        elif isinstance(item, Ret):
            data.insert(0, o.LDC)
            data.insert(1, Ref(RET_NAME))
            data.insert(2, o.JMP)

        elif isinstance(item, Call):
            funcname = item.values[0]
            data.insert(0, o.LDC)
            data.insert(1, Ref(funcname))
            data.insert(2, o.IPT)
            data.insert(3, o.LDC)
            data.insert(4, Ref(CALL_NAME))
            data.insert(5, o.JMP)

        elif isinstance(item, Jump):
            funcname = item.values[0]
            data.insert(0, o.LDC)
            data.insert(1, Ref(funcname))
            data.insert(2, o.JMP)

        elif isinstance(item, JumpIf):
            funcname = item.values[0]
            data.insert(0, o.LDC)
            data.insert(1, Ref(funcname))
            data.insert(2, o.JMZ)

        elif isinstance(item, Func):
            funcname = item.values[0]
            data.insert(0, o.ERR) # invalid op before function
            data.insert(1, Lbl(funcname))

        elif isinstance(item, Read):
            addrname = item.values[0]
            data.insert(0, o.LDC)
            data.insert(1, Ref(addrname))
            data.insert(2, o.RMM)

        elif isinstance(item, Write):
            addrname = item.values[0]
            data.insert(0, o.LDC)
            data.insert(1, Ref(addrname))
            data.insert(2, o.WMM)


        elif isinstance(item, vm.OpCode):
            buf.write_ushort(item)

        elif isinstance(item, int):
            buf.write_byte(item)

        else:
            raise TypeError('Invalid item type: {item}')

        items_index += 1

    for pos, name in const_refs.items():
        assert name in const_values, name
        buf.write_uint(const_values[name], pos=pos)

    print('Labels:')
    pprint(const_values)

    buf.pos = vm.OPCODE_SIZE
    return buf


################################################################################
################################################################################
################################################################################

CALL_NAME = '__call'
RET_NAME = '__ret'

STACK_SIZE = 16
SIZE_T = vm.ARG_SIZE

PROGRAM = [
o.ERR, # wrong opcode at 0 address for error detection

# entry point here:
Jump('main'),


Func('__exit'), # ... exitcode
    o.DUP,
    o.PRT, # prints exit code
    o.NOT,
    JumpIf('__exit_log'),
    o.LOG,
    Lbl('__exit_log'),
    o.HLT,
Undef('__exit_log'),


Data('__CS_INDEX', SIZE_T),
Data('__CS', STACK_SIZE * SIZE_T),
DefConst('__CS_SIZE_', STACK_SIZE),


Func(CALL_NAME), # ... callee caller
    DefConst('__call_FIX_', SIZE_T + 2 * vm.OPCODE_SIZE),
    Read('__CS_INDEX'),
    o.DUP,
    o.LDC, Cint(1),
    o.ADD,
    o.DUP,
    Write('__CS_INDEX'),
    o.LDC, Const('__CS_SIZE_'),
    o.LSS,
    JumpIf('__call_stack_overflow'),
    o.LDC, Cint(SIZE_T),
    o.MUL,
    o.LDC, Ref('__CS'),
    o.ADD,
    o.SWP,
    o.LDC, Const('__call_FIX_'),
    o.ADD,
    o.SWP,
    o.WMM,
    o.JMP,
    Lbl('__call_stack_overflow'),
        o.POP, o.POP, o.POP,
        o.LDC, Cint(1),
        Jump('__exit'),
Undef('__call_FIX_'),
Undef('__call_stack_overflow'),


Func(RET_NAME), # ...
    Read('__CS_INDEX'),
    o.DUP,
    o.LDC, Cint(0),
    o.EQL,
    JumpIf('__ret_stack_underflow'),
    o.LDC, Cint(-1),
    o.ADD,
    o.DUP,
    o.LDC, Cint(SIZE_T),
    o.MUL,
    o.LDC, Ref('__CS'),
    o.ADD,
    o.RMM,
    o.SWP,
    Write('__CS_INDEX'),
    o.JMP,
    Lbl('__ret_stack_underflow'),
        o.POP,
        o.LDC, Cint(1),
        Jump('__exit'),
Undef('__ret_stack_underflow'),


Func('test_func'),
    o.LDC, Cint(222),
    o.LDC, Cint(333),
    o.LDC, Cint(444),
    o.PRT,
    o.PRT,
    o.PRT,
    Ret(),



Func('factorial'),
    o.DUP,
    JumpIf('fact_nonzero_arg'),
    Lbl('fact_zero_arg'),
        o.POP,
        o.LDC, Cint(1),
        Ret(),

    Lbl('fact_nonzero_arg'),
        o.DUP,
        o.LDC, Cint(1),
        o.SWP,
        o.SUB,

        Call('factorial'),

        o.MUL,
        Ret(),
Undef('fact_zero_arg'),
Undef('fact_nonzero_arg'),



Func('main'),
    o.LDC, Cint(10),
    Call('factorial'),
    o.PRT,

    o.LDC, Cint(0),
    Jump('__exit'),



Lbl('!end'), # == len(v.memory.data)
]

################################################################################
################################################################################
################################################################################


v = vm.VM()
v.memory = generate_mem(PROGRAM)

print('')
print('OpCodes:')
pprint(list(vm.OpCode))
print('')
print('Memory:')

s = v.memory.data.hex()
s = split2len(s, 32)
s = [' '.join(split2len(i, 2)) for i in s]
print(*s, sep='\n')
print('')
print('Execution log:')
print('')

v.execute()

