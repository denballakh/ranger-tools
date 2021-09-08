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


@unique
class OpCode(IntEnum):
    # обозначение:
    # ... a1 a2 a3
    # - означает стек, на котором находятся элементы a3, a2, a1  (a3 - на вершине стека)
    # ... - это 0 или более элементов под именованными элементами

    # basic
    ZER = 0 # wrong opcode
    HLT = 1 # halts program
    NOP = 2 # no operation

    # io
    PRT = 3 # ... a -> ...
            # prints a

    # stack
    DUP = 4 # ... a -> ... a a
    POP = 5 # ... a -> ...
    GET = 6 # ... index -> ... stack[-index]
    ROT = 17 # ... c b a -> ... a c b
    SWP = 18 # ... b a -> ... a b

    # const
    LDC = 7 # ... -> ... C
            # reads const (signed int) and pushes it

    # mem
    RMM = 8 # ... addr -> ... mem[addr]
    WMM = 9 # ... val addr -> ...
            # writes val to addr

    # jumps
    IPT = 10 # ... -> ... (instruction pointer)
    JMP = 11 # ... addr -> ...
             # jumps to addr
    JMZ = 12 # ... cond addr -> ...
             # jumps to addr if cond

    # math
    MUL = 13 # ... b a -> ... (a * b)
    DIV = 14 # ... b a -> ... (a // b)
    ADD = 15 # ... b a -> ... (a + b)
    SUB = 16 # ... b a -> ... (a - b)




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
                print('Halted')
                break
            except Exception as e:
                print(f'Error! state: {self}')
                raise Exception from e
            # time.sleep(0.005)

    def execute_cmd(self):
        vm = self
        mem = vm.memory
        stack = vm.stack

        b0 = mem.read_byte()
        try:
            opcode = OpCode(b0)
        except ValueError as e:
            raise VMOpCodeException(f'Invalid opcode: {b0}') from e

        # print(f'Executing opcode: {opcode!r}, pos={mem.pos}')

        if opcode is OpCode.ZER:
            raise VMOpCodeException(f'Zero opcode at {mem.pos - 1}')

        elif opcode is OpCode.HLT:
            raise VMHaltException(f'Halting...')

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

        else:
            raise Exception(f'Empty code for opcode: {opcode}')

