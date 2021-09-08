from enum import Enum, IntEnum, unique
from abc import abstractmethod
import time

from ranger_tools.io import Buffer, Stack

class VMException(Exception):
    pass

class VMHaltException(VMException):
    pass

class VMOpCodeException(VMException):
    pass

def unique_ints(init = 1):
    x = init
    while True:
        yield x
        x += 1

opcode_generator = unique_ints(init=1)
OG = lambda: next(opcode_generator)

OPCODE_SIZE = 2
ARG_SIZE = 4

@unique
class OpCode(IntEnum):
    # обозначение:
    # ... a1 a2 a3
    # - означает стек, на котором находятся элементы a3, a2, a1  (a3 - на вершине стека)
    # ... - это 0 или более элементов под именованными элементами

    # basic
    ERR = 0 # wrong opcode
    HLT = OG() # halts program
    NOP = OG() # no operation

    # io
    PRT = OG() # ... a -> ...
            # prints a

    # stack
    DUP = OG() # ... a -> ... a a
    POP = OG() # ... a -> ...
    GET = OG() # ... index -> ... stack[-index]
    ROT = OG() # ... c b a -> ... a c b
    SWP = OG() # ... b a -> ... a b

    # const
    LDC = OG() # ... -> ... C
            # reads const (signed int) and pushes it

    # mem
    RMM = OG() # ... addr -> ... mem[addr]
    WMM = OG() # ... val addr -> ...
            # writes val to addr

    # jumps
    IPT = OG() # ... -> ... (instruction pointer)
    JMP = OG() # ... addr -> ...
             # jumps to addr
    JMZ = OG() # ... cond addr -> ...
             # jumps to addr if cond

    # math
    MUL = OG() # ... b a -> ... (a * b)
    DIV = OG() # ... b a -> ... (a // b)
    ADD = OG() # ... b a -> ... (a + b)
    SUB = OG() # ... b a -> ... (a - b)

    # logic
    LSS = OG() # ... b a -> ... (a < b)
    LSE = OG() # ... b a -> ... (a <= b)
    EQL = OG() # ... b a -> ... (a == b)
    NOT = OG() # ... a -> ... !a


    LOG = OG()




class VMMemory(Buffer):
    @property
    def cmdptr(self):
        return self.pos

    def __init__(self, size=1024):
        super().__init__(b'\0' * size)

# class VMAccumulator:
#     def __init__(self):
#         self.acc = 0

#     def __repr__(self) -> str:
#         return f'<Accumulator: acc={self.acc}>'

class VM:
    def __init__(self):
        self.memory = VMMemory()
        self.memory.pos = 0
        self.stack = Stack()

    def __repr__(self) -> str:
        return f'<VM: memory={self.memory} stack={self.stack}>'

    def execute(self):
        while 1:
            try:
                self.execute_cmd()
            except VMHaltException:
                # print('Halted')
                break
            except Exception as e:
                print(f'Error! state: {self}')
                raise Exception(f'Error at {self.memory.pos}') from e
            # time.sleep(0.005)

    def execute_cmd(self):
        vm = self
        mem = vm.memory
        stack = vm.stack

        opcode = mem.read_ushort()
        try:
            opcode = OpCode(opcode)
        except ValueError as e:
            raise VMOpCodeException(f'Invalid opcode: {opcode}') from e

        # print(f'Executing opcode: {opcode!r}, pos={mem.pos}')

        if opcode is OpCode.ERR:
            raise VMOpCodeException(f'ERR opcode at {mem.pos - 1}')

        elif opcode is OpCode.HLT:
            raise VMHaltException()

        elif opcode is OpCode.NOP:
            pass


        elif opcode is OpCode.PRT:
            print(f'{stack.pop()}')


        elif opcode is OpCode.DUP:
            value = stack.pop()
            stack.push(value)
            stack.push(value)

        elif opcode is OpCode.POP:
            value = stack.pop()

        elif opcode is OpCode.GET:
            index = stack.pop()
            value = stack.data[-index]
            stack.push(value)

        elif opcode is OpCode.SWP:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1)
            stack.push(v2)

        elif opcode is OpCode.ROT:
            v1 = stack.pop()
            v2 = stack.pop()
            v3 = stack.pop()
            stack.push(v1)
            stack.push(v3)
            stack.push(v2)


        elif opcode is OpCode.LDC:
            value = mem.read_int()
            stack.push(value)


        elif opcode is OpCode.RMM:
            address = stack.pop()
            value = mem.read_uint(pos=address)
            # print(f'Reading {value} from {address}')
            stack.push(value)

        elif opcode is OpCode.WMM:
            address = stack.pop()
            value = stack.pop()
            # print(f'Writing {value} to {address}')
            mem.write_uint(value, pos=address)


        elif opcode is OpCode.IPT:
            stack.push(mem.pos)

        elif opcode is OpCode.JMP:
            address = stack.pop()
            # print(f'Jumping to {address}')
            mem.pos = address

        elif opcode is OpCode.JMZ:
            address = stack.pop()
            condition = stack.pop()
            # print(f'Checking condition {condition}...')
            if condition:
                # print(f'Jumping to {address}')
                mem.pos = address


        elif opcode is OpCode.MUL:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 * v2)

        elif opcode is OpCode.DIV:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 // v2)

        elif opcode is OpCode.ADD:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 + v2)

        elif opcode is OpCode.SUB:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 - v2)


        elif opcode is OpCode.LSS:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(int(v1 < v2))

        elif opcode is OpCode.LSE:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(int(v1 <= v2))

        elif opcode is OpCode.EQL:
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(int(v1 == v2))

        elif opcode is OpCode.NOT:
            v1 = stack.pop()
            stack.push(int(not v1))


        elif opcode is OpCode.LOG:
            print('-' * 80)
            print('VM State:')
            print(f'  cmdptr = {self.memory.pos}')
            print(f'  stack = {self.stack}')
            print(f'  memory = {self.memory}')
            print('-' * 80)

        else:
            raise Exception(f'Empty code for opcode: {opcode}')

