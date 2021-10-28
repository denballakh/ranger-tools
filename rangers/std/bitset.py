from typing import Iterator, TypeVar, Type, Union

__all__ = 'BitSet', 'FrozenBitSet'

T = Union['BitSet', 'FrozenBitSet']

class FrozenBitSet:
    '''

    '''
    char_values = {'0', '1'}
    int_values = {0, 1}

    value: int
    size: int

    def __init__(self, value: Union[None, int, str, list, tuple, bytes, bytearray, T] = None, *, size: int = None):
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

        elif isinstance(value, (FrozenBitSet, BitSet)):
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
        s = bin(self.value)[2:]
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
    def __concat__(self, other) -> T:
        obj = self.copy()
        obj.__iconcat__(other)
        return obj


    def __index__(self) -> int: return self.value
    def __int__(self) -> int: return self.value
    # def __hash__(self) -> int: raise TypeError

    def __bool__(self) -> bool: return bool(self.value)
    def __not__(self) -> bool: return not self

    def __eq__(self, other: Union[T, int, tuple, object]) -> bool:
        if isinstance(other, BitSet):
            return self.value == other.value and self.size == other.size

        if isinstance(other, int):
            return self.value == other

        if isinstance(other, tuple):
            return self.value == other[0] and self.size == other[1]

        raise TypeError(f'Invalid type: {type(other)}')

    def __ne__(self, other: Union[T, int, tuple, object]) -> bool:
        return not self == other

    # def __cmp__(self, other):
    #     return not (self.value == other.value and self.size == other.size)
    # def __lt__(self, other) -> bool: return self.__cmp__(other) < 0
    # def __le__(self, other) -> bool: return self.__cmp__(other) <= 0
    # def __gt__(self, other) -> bool: return self.__cmp__(other) > 0
    # def __ge__(self, other) -> bool: return self.__cmp__(other) >= 0


    def __getitem__(self, key: Union[int, slice]) -> Union[int, list]:
        if isinstance(key, slice):
            raise NotImplementedError

        elif isinstance(key, int):
            if not 0 <= key < self.size: raise KeyError(f'Invalid key: {key}')
            return (self.value >> key) & 1

        else:
            raise TypeError

    def __setitem__(self, key: Union[int, slice], value):
        if isinstance(key, slice):
            raise NotImplementedError

        elif isinstance(key, int):
            assert 0 <= key < self.size, f'Invalid key: {key}'
            assert value in self.int_values, f'Invalid value: {value}'
            self.value = self.value & (self.bit_mask() - 1 << key) | (value << key)

        else:
            raise TypeError

    def __delitem__(self, key: Union[int, slice]):
        raise NotImplementedError



    def __invert__(self) -> T:
        return self.new(self.bit_mask() - self.value, size=self.size)
    # ((1 << self.size) - 1) & ~self.value


    def __iand__(self, other: T):
        self.value = (self.value & other.value) & self.bit_mask()
        return self

    def __ior__(self, other: T):
        self.value = (self.value | other.value) & self.bit_mask()
        return self

    def __ixor__(self, other: T):
        self.value = (self.value ^ other.value) & self.bit_mask()
        return self

    def __ilshift__(self, other: Union[int, T]):
        if isinstance(other, int):
            self.value <<= other
            self.size += other

        elif isinstance(other, (FrozenBitSet, BitSet)):
            pass

        else:
            raise TypeError(f'Invalid type: {type(other)}')
        return self

    def __irshift__(self, other: Union[int, T]):
        if isinstance(other, int):
            self.value >>= other
            self.size -= other

        elif isinstance(other, (FrozenBitSet, BitSet)):
            pass

        else:
            raise TypeError(f'Invalid type: {type(other)}')
        return self



    # def __pos__(self): return self.new(self)
    # def __neg__(self): pass
    # def __abs__(self): pass


    def __and__(self, other: T) -> T:
        obj = self.copy()
        obj &= other
        return obj

    def __or__(self, other: T) -> T:
        obj = self.copy()
        obj |= other
        return obj

    def __xor__(self, other: T) -> T:
        obj = self.copy()
        obj ^= other
        return obj

    def __lshift__(self, other: Union[int, T]) -> T:
        obj = self.copy()
        obj <<= other
        return obj

    def __rshift__(self, other: Union[int, T]) -> T:
        obj = self.copy()
        obj >>= other
        return obj


    def __rand__(self, other: T) -> T:
        return self & other

    def __ror__(self, other: T) -> T:
        return self | other

    def __rxor__(self, other: T) -> T:
        return self ^ other

    def __rlshift__(self, other: Union[int, T]) -> T:
        pass

    def __rrshift__(self, other: Union[int, T]) -> T:
        pass



    def __iadd__(self, other):
        pass
        return self

    def __isub__(self, other):
        pass
        return self

    def __imul__(self, other):
        pass
        return self

    def __itruediv__(self, other):
        pass
        return self

    def __imod__(self, other):
        pass
        return self

    def __ifloordiv__(self, other):
        pass
        return self

    def __ipow__(self, other):
        pass
        return self

    def __imatmul__(self, other):
        pass
        return self


    def __add__(self, other) -> T:
        obj = self.copy()
        obj += other
        return obj

    def __sub__(self, other) -> T:
        obj = self.copy()
        obj -= other
        return obj

    def __mul__(self, other) -> T:
        obj = self.copy()
        obj *= other
        return obj

    def __truediv__(self, other) -> T:
        obj = self.copy()
        obj /= other
        return obj

    def __mod__(self, other) -> T:
        obj = self.copy()
        obj %= other
        return obj

    def __floordiv__(self, other) -> T:
        obj = self.copy()
        obj //= other
        return obj

    def __pow__(self, other) -> T:
        obj = self.copy()
        obj **= other
        return obj

    def __matmul__(self, other) -> T:
        obj = self.copy()
        obj @= other
        return obj


    def __radd__(self, other) -> T:
        pass

    def __rsub__(self, other) -> T:
        pass

    def __rmul__(self, other) -> T:
        pass

    def __rtruediv__(self, other) -> T:
        pass

    def __rmod__(self, other) -> T:
        pass

    def __rfloordiv__(self, other) -> T:
        pass

    def __rpow__(self, other) -> T:
        pass

    def __rmatmul__(self, other) -> T:
        pass


    def __divmod__(self, other):
        return self // other, self % other

    def __rdivmod__(self, other):
        return other // self, other % self



    def get(self, key: Union[int, slice]) -> Union[int, list]: return self[key]
    def set(self, key: Union[int, slice], value: int = 1): self[key] = value
    def reset(self, key: Union[int, slice]): self[key] = 0
    def flip(self, key: Union[int, slice]): self[key] = not self[key]

    def bit_mask(self) -> int:
        return (1 << self.size) - 1

    def copy(self) -> T:
        return type(self)(self)

    def new(self, *args, **kwargs) -> T:
        return type(self)(*args, **kwargs)

    def all(self) -> bool: return self.value == self.bit_mask()
    def any(self) -> bool: return bool(self.value)

    def all_one(self) -> bool: return self.all()
    def any_one(self) -> bool: return self.any()

    def all_zero(self) -> bool: return not self.any()
    def any_zero(self) -> bool: return not self.all()

    def copy_from(self, other: T):
        self.value = other.value
        self.size = other.size




class BitSet(FrozenBitSet):
    def __hash__(self) -> int:
        return hash((self.value, self.size))

    def __setitem__(self, key, value): raise TypeError
    def __delitem__(self, key): raise TypeError


    def __iconcat__(self, other: T): return self.__concat__(other)

    def __iand__(self, other: T): return self & other
    def __ior__(self, other: T): return self | other
    def __ixor__(self, other: T): return self ^ other
    def __ilshift__(self, other: Union[int, T]): return self << other
    def __irshift__(self, other: Union[int, T]): return self >> other

    def __iadd__(self, other): return self + other
    def __isub__(self, other): return self - other
    def __imul__(self, other): return self * other
    def __itruediv__(self, other): return self / other
    def __imod__(self, other): return self % other
    def __ifloordiv__(self, other): return self // other
    def __ipow__(self, other): return self ** other
    def __imatmul__(self, other): return self @ other

