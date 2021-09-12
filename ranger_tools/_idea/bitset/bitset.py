from typing import Iterator, TypeVar, Type, Union

T = TypeVar('T', bound='BitSet')

class BitSet:
    char_values = {'0', '1'}
    int_values = {0, 1, True, False}

    value: int
    size: int

    def __init__(self, value: Union[None, int, str, list, tuple, bytes, bytearray, 'BitSet'] = None, *, size: int = None):
        if size is not None:
            if size < 0: raise ValueError('Size must be positive')

        if isinstance(value, int):
            if value < 0: raise ValueError('Init value cannot be negative')
            self.value = value

            if size is not None:
                self.size = size
            else:
                self.size = value.bit_length()

        elif isinstance(value, str):
            if value.startswith('0b'):
                value = value[2:]

            if not set(value) <= self.char_values: raise ValueError(f'String must contain only {self.char_values}')

            self.value = int(value, 2)

            if size is not None:
                self.size = size
            else:
                self.size = len(value)

        elif isinstance(value, (list, tuple)):
            if not set(value) <= self.int_values: raise ValueError(f'List must contain only {self.int_values}')

            bin_string = ''.join('1' if item else '0' for item in value)
            if not bin_string:
                self.value = 0
            else:
                self.value = int(bin_string[::-1], 2)

            self.size = len(value)

        elif isinstance(value, (bytes, bytearray)):
            if size is not None:
                self.size = size
            else:
                self.size = 8 * len(value)

            self.value = int.from_bytes(value, 'little')

        elif isinstance(value, BitSet):
            self.size = value.size
            self.value = value.value

        elif value is None:
            self.value = 0
            if size is not None:
                self.size = size
            else:
                self.size = 32

        else:
            raise TypeError(f'Invalid type of init value: {value} [{value.__class__}]')

        if self.size < self.value.bit_length(): raise ValueError('Init value doesnt fit in size')

    def __str__(self) -> str:
        s = bin(self.value)[2:][::-1]
        s = '0' * (self.size - len(s)) + s
        return s

    def __repr__(self) -> str:
        return f'{type(self).__name__}(value={self.value}, size={self.size})'

    def __contains__(self, other) -> bool: pass
    def __len__(self) -> int: return self.size
    def __iter__(self) -> Iterator:
        key = 0
        while key < self.size:
            yield self[key]
            key += 1

    def __iconcat__(self, other): pass
    def __concat__(self, other) -> 'BitSet':
        obj = self.copy()
        obj.__iconcat__(other)
        return obj


    def __index__(self) -> int: return self.value
    # def __hash__(self) -> int: raise TypeError

    def __bool__(self) -> bool: return bool(self.value)
    def __not__(self) -> bool: return not self

    # def __cmp__(self, other):
    #     return not (self.value == other.value and self.size == other.size)
    def __eq__(self, other: 'BitSet') -> bool: return self.value == other.value and self.size == other.size
    def __ne__(self, other: 'BitSet') -> bool: return not self == other
    # def __lt__(self, other) -> bool: return self.__cmp__(other) < 0
    # def __le__(self, other) -> bool: return self.__cmp__(other) <= 0
    # def __gt__(self, other) -> bool: return self.__cmp__(other) > 0
    # def __ge__(self, other) -> bool: return self.__cmp__(other) >= 0


    def __getitem__(self, key: Union[int, slice]) -> Union[int, list]:
        if not 0 <= key < self.size: raise KeyError(f'Invalid key: {key}')
        return (self.value >> key) & 1

    def __setitem__(self, key: Union[int, slice], value):
        assert 0 <= key < self.size, f'Invalid key: {key}'
        assert value in self.int_values, f'Invalid value: {value}'
        self.value = self.value & (self.bit_mask() - 1 << key) | (value << key)

    def __delitem__(self, key: Union[int, slice]): pass


    def __invert__(self) -> 'BitSet': return BitSet(self.bit_mask() - self.value, size=self.size)
    # ((1 << self.size) - 1) & ~self.value
    # def __pos__(self): return BitSet(self)
    # def __neg__(self): pass
    # def __abs__(self): pass


    def __iand__(self, other: 'BitSet'):
        self.value = (self.value & other.value) & self.bit_mask()

    def __ior__(self, other: 'BitSet'):
        self.value = (self.value | other.value) & self.bit_mask()

    def __ixor__(self, other: 'BitSet'):
        self.value = (self.value ^ other.value) & self.bit_mask()

    def __ilshift__(self, other: int):
        self.value <<= other
        self.size += other

    def __irshift__(self, other: int):
        self.value >>= other
        self.size -= other


    def __and__(self, other: 'BitSet') -> 'BitSet':
        obj = self.copy()
        obj &= other
        return obj

    def __or__(self, other: 'BitSet') -> 'BitSet':
        obj = self.copy()
        obj |= other
        return obj

    def __xor__(self, other: 'BitSet') -> 'BitSet':
        obj = self.copy()
        obj ^= other
        return obj

    def __lshift__(self, other: int) -> 'BitSet':
        obj = self.copy()
        obj <<= other
        return obj

    def __rshift__(self, other: int) -> 'BitSet':
        obj = self.copy()
        obj >>= other
        return obj



    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass

    def __imul__(self, other):
        pass

    def __itruediv__(self, other):
        pass

    def __imod__(self, other):
        pass

    def __ifloordiv__(self, other):
        pass

    def __ipow__(self, other):
        pass

    def __imatmul__(self, other):
        pass


    def __add__(self, other) -> 'BitSet':
        obj = self.copy()
        obj += other
        return obj

    def __sub__(self, other) -> 'BitSet':
        obj = self.copy()
        obj -= other
        return obj

    def __mul__(self, other) -> 'BitSet':
        obj = self.copy()
        obj *= other
        return obj

    def __truediv__(self, other) -> 'BitSet':
        obj = self.copy()
        obj /= other
        return obj

    def __mod__(self, other) -> 'BitSet':
        obj = self.copy()
        obj %= other
        return obj

    def __floordiv__(self, other) -> 'BitSet':
        obj = self.copy()
        obj //= other
        return obj

    def __pow__(self, other) -> 'BitSet':
        obj = self.copy()
        obj **= other
        return obj

    def __matmul__(self, other) -> 'BitSet':
        obj = self.copy()
        obj @= other
        return obj



    def get(self, key: Union[int, slice]) -> int: return self[key]
    def set(self, key: Union[int, slice], value: int = 1): self[key] = value
    def reset(self, key: Union[int, slice]): self[key] = 0
    def flip(self, key: Union[int, slice]): self[key] = not self[key]

    def bit_mask(self) -> int:
        return 2 ** self.size - 1

    def copy(self):
        return type(self)(self)



class FrozenBitSet(BitSet):
    def __hash__(self) -> int:
        return hash((self.value, self.size))

    def __setitem__(self, key, value): raise TypeError


    def __iand__(self, other: 'BitSet'):
        self = self.copy()
        self.value = (self.value & other.value) & self.bit_mask()

    def __ior__(self, other: 'BitSet'):
        self = self.copy()
        self.value = (self.value | other.value) & self.bit_mask()

    def __ixor__(self, other: 'BitSet'):
        self = self.copy()
        self.value = (self.value ^ other.value) & self.bit_mask()

    def __ilshift__(self, other: int):
        self = self.copy()
        self.value <<= other
        self.size += other

    def __irshift__(self, other: int):
        self = self.copy()
        self.value >>= other
        self.size -= other


    def __iadd__(self, other):
        self = self.copy()
        pass

    def __isub__(self, other):
        self = self.copy()
        pass

    def __imul__(self, other):
        self = self.copy()
        pass

    def __itruediv__(self, other):
        self = self.copy()
        pass

    def __imod__(self, other):
        self = self.copy()
        pass

    def __ifloordiv__(self, other):
        self = self.copy()
        pass

    def __ipow__(self, other):
        self = self.copy()
        pass

    def __imatmul__(self, other):
        self = self.copy()
        pass

