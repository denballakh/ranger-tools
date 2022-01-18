from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Callable,
    Iterable,
    Optional,
    Sequence,
    overload,
    TypeVar,
    ParamSpec,
    Concatenate,
)

import sys
import warnings
import time

from enum import IntEnum
from functools import wraps
import itertools

from pprint import pprint

from rangers.std.mixin import PrintableMixin

TF = TypeVar('TF', bound=Callable)


class Repr:
    def __init__(self, s: str, /):
        self.s = s

    def __repr__(self) -> str:
        return self.s


def resolve_name(obj: object) -> object | Repr:
    if hasattr(obj, '__name__'):
        return Repr(f'<{obj.__name__}>')  # type: ignore[attr-defined]
    return obj


def argskwargs_to_string(args: Sequence[object], kwargs: dict[str, object] = None) -> str:
    args_l = (f'{resolve_name(arg)!r}' for arg in args)
    kwargs_l = (
        (f'{key!s}={resolve_name(value)!r}' for key, value in kwargs.items())
        if kwargs is not None
        else ()
    )

    return ", ".join(itertools.chain(args_l, kwargs_l))


def _(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'{func.__name__}({argskwargs_to_string(args, kwargs)}) called')
        result = func(*args, **kwargs)
        print(f'{func.__name__}({argskwargs_to_string(args, kwargs)}) = {result!r}')
        return result

    return wrapper


identity = lambda f: f


class DecoratorState(IntEnum):
    A = 0  # decorator
    B = 1  # decorator(kwargs)
    C = 2  # decorator(kwargs)(dec)
    D = 3  # decorator(kwargs)(dec)(cargs)
    E = 4  # decorator(kwargs)(dec)(cargs)(func)


# class decorator:
#     _state: DecoratorState = None

#     @_
#     def __new__(cls, __func: Optional[Callable] = None, /, **kwargs) -> decorator:
#         if __func is not None:
#             assert (
#                 not kwargs
#             ), 'Unexpected keyword arguments after position-only argument for function'
#             return cls()(__func)
#         return super().__new__(cls)

#     @_
#     def __init__(
#         self,
#         *args,
#         _state: DecoratorState = DecoratorState.A,
#         **kwargs,
#     ) -> None:
#         self._state = _state

#         if args or kwargs:
#             self(*args, **kwargs)

#     def __repr__(self):
#         return f'<{type(self).__name__}: state={self._state}>'

#     @_
#     def __call__(self, *args, **kwargs):
#         match self._state:
#             case DecoratorState.A:
#                 pass

#             case DecoratorState.B:
#                 pass

#             case DecoratorState.C:
#                 pass

#             case DecoratorState.D:
#                 pass

#             case DecoratorState.E:
#                 pass

#             case _:
#                 raise ValueError(self._state)

P = ParamSpec('P')
P1 = ParamSpec('P1')
P2 = ParamSpec('P2')
T = TypeVar('T')


def decorator(func_=None, /, enabled=True):
    if not enabled:
        return lambda f: f

    def decorator_(func):
        @wraps(func)
        def wrapper(func__=None, /, **ddkwargs):
            def decorator__(func___):
                @wraps(func___)
                def wrapper_(*args, **kwargs):
                    return func(func___, args, kwargs, **ddkwargs)

                return wrapper_

            if func__ is None:
                return decorator__
            return decorator__(func__)

        return wrapper

    if func_ is None:
        return decorator_
    return decorator_(func_)


@decorator
def warning(func, fargs, fkwargs, msg, pred):
    if pred():
        warnings.warn(msg, UserWarning)
    return func(*fargs, **fkwargs)


# input()


@decorator
def error(func, fargs, fkwargs, msg, pred, exception=Exception):
    if pred():
        raise exception(msg)
    return func(*fargs, **fkwargs)


@decorator
def not_implemented(func, fargs, fkwargs, msg=''):
    raise NotImplementedError(f'Function {func.__name__} is not implemented!\n{msg}')


@decorator
def deprecated(func, fargs, fkwargs, pred=lambda: True, msg=''):
    if pred():
        warnings.warn(f'Function {func.__name__} is deprecated!\n{msg}', DeprecationWarning)
    return func(*fargs, **fkwargs)


if TYPE_CHECKING:

    def trace(func: TF) -> TF:
        return func


else:

    @decorator(enabled=__debug__)
    def trace(func, fargs, fkwargs, msg='<trace>: ', timer=time.perf_counter, stream=sys.stdout):
        print(f'{msg}{func.__name__}({argskwargs_to_string(fargs, fkwargs)}) called', file=stream)
        t1 = timer()
        result = func(*fargs, **fkwargs)
        t2 = timer()
        tdiff = t2 - t1
        print(
            f'{msg}{func.__name__}({argskwargs_to_string(fargs, fkwargs)}) = {result} [{round(tdiff * 10 ** 6, 1)} mcs]',
            file=stream,
        )
        return result


@decorator
def catch_exceptions(func, fargs, fkwargs, exceptions=(Exception,), default=None, on_error=None):
    try:
        return func(*fargs, **fkwargs)
    except exceptions as exc:
        if on_error is not None:
            assert callable(on_error)
            on_error(exc)
        return default


@decorator
def redirected_stdout(func, fargs, fkwargs, stream):
    stdout, sys.stdout = sys.stdout, stream
    result = func(*fargs, **fkwargs)
    sys.stdout = stdout
    return result


@decorator
def redirected_stderr(func, fargs, fkwargs, stream):
    stderr, sys.stderr = sys.stderr, stream
    result = func(*fargs, **fkwargs)
    sys.stderr = stderr
    return result


@decorator(enabled=__debug__)
def timing(func, fargs, fkwargs, timer=time.perf_counter):
    t1 = timer()
    result = func(*fargs, **fkwargs)
    t2 = timer()
    return result, t2 - t1


@decorator
def once(func, fargs, fkwargs):
    if not hasattr(func, '__once_result__'):
        func.__once_result__ = func(*fargs, **fkwargs)
    return func.__once_result__


@decorator
def before(func, fargs, fkwargs, _):
    _()
    result = func(*fargs, **fkwargs)
    return result


@decorator
def after(func, fargs, fkwargs, _):
    result = func(*fargs, **fkwargs)
    _()
    return result


def part(iterable, n, fill):
    b = []
    for x in iterable:
        b.append(x)
        if len(b) == n:
            yield tuple(b)
            b = []
    if b:
        yield tuple(b + [fill] * (n - len(b)))


MAGIC_OPS = {
    ('__iadd__', '__add__'),
    ('__isub__', '__sub__'),
    ('__imul__', '__mul__'),
    ('__imatmul__', '__matmul__'),
    ('__itruediv__', '__truediv__'),
    ('__ifloordiv__', '__floordiv__'),
    ('__imod__', '__mod__'),
    ('__ipow__', '__pow__'),
    ('__ilshift__', '__lshift__'),
    ('__irshift__', '__rshift__'),
    ('__iand__', '__and__'),
    ('__ixor__', '__xor__'),
    ('__ior__', '__or__'),
}


def optimize_inplace(cls):
    for imthname, mthname in MAGIC_OPS:
        if (imethod := getattr(cls, imthname, None)) is None:
            continue

        if (method := getattr(cls, mthname, None)) is None:
            continue

        @wraps(imethod)
        def wrapper(self, other, method=method, imethod=imethod):
            print(f'ref cnt of {self} is {sys.getrefcount(self)}')
            if sys.getrefcount(self) == 4:
                print('+')
                return imethod(self, other)
            print('-')
            return method(self, other)

        setattr(cls, imthname, wrapper)

    return cls


@decorator
def profile(func, fargs, fkwargs, filename, sortby='time'):
    # calls cumulative filename line name nfl pcalls stdname time
    try:
        import cProfile
        import pstats
        import io
        from pstats import SortKey

        pr = cProfile.Profile()
        pr.enable()

        return func(*fargs, **fkwargs)

    finally:
        pr.disable()
        s = io.StringIO()
        sortby = getattr(SortKey, sortby.upper())
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()

        with open(filename, 'wt', encoding='utf-8') as file:
            file.write(s.getvalue())
