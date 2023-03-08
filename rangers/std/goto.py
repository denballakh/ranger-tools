from __future__ import annotations
from collections.abc import Callable
from typing import Any, TypeVar

import types

import bytecode

__all__ = ['goto', 'label']

F = TypeVar('F', bound=Callable[..., Any])


def create_func_with_code(func: F, code: types.CodeType) -> F:
    assert isinstance(func, types.FunctionType)
    func_new = types.FunctionType(
        code,
        func.__globals__,
        func.__name__,
        func.__defaults__,
        func.__closure__,
    )
    func_new.__kwdefaults__ = func.__kwdefaults__
    func_new.__annotations__ = func.__annotations__
    func_new.__dict__ = func.__dict__.copy()
    func_new.__wrapped__ = func  # type: ignore[attr-defined]
    return func_new  # type: ignore[return-value]


def _inline_jumps(func: F) -> F:
    # assert isinstance(func, types.FunctionType), func
    aliases_goto = {name for name, obj in func.__globals__.items() if obj is goto}
    aliases_label = {name for name, obj in func.__globals__.items() if obj is label}
    assert not aliases_goto & aliases_label
    aliases = aliases_goto | aliases_label
    labels: dict[str, bytecode.Label] = {}
    label_occured: dict[str, bool] = {}

    bc = bytecode.Bytecode.from_code(func.__code__)
    bc_new = bytecode.Bytecode.from_code(func.__code__)
    bc_new.clear()

    for i1 in (it := iter(bc)):
        match i1:
            case bytecode.Instr(name='LOAD_GLOBAL', arg=(_, arg)) if arg in aliases:
                i2 = next(it)  # LOAD_ATTR
                i3 = next(it)  # POP_TOP
                assert isinstance(i2, bytecode.Instr) and i2.name == 'LOAD_ATTR', i2
                assert isinstance(i3, bytecode.Instr) and i3.name == 'POP_TOP', i3
                lbl = i2.arg
                assert isinstance(lbl, str), lbl

                if lbl not in labels:
                    labels[lbl] = bytecode.Label()

                if arg in aliases_label:
                    label_occured[lbl] = True
                    bc_new.append(labels[lbl])

                if arg in aliases_goto:
                    if label_occured.get(lbl, False):
                        bc_new.append(bytecode.Instr('JUMP_BACKWARD', arg=labels[lbl]))
                    else:
                        bc_new.append(bytecode.Instr('JUMP_FORWARD', arg=labels[lbl]))

            case _:
                bc_new.append(i1)

    bc_new.legalize()
    return create_func_with_code(func, bc_new.to_code())


class _goto:
    def __getattr__(self, attr: str) -> None:
        if attr.startswith('__') and attr.endswith('__') and len(attr) >= 5:
            # dunder
            raise AttributeError(attr)
        raise AttributeError(f'do not use goto.{attr} outside of @goto functions')

    def __call__(self, func: F, /) -> F:
        return _inline_jumps(func)


class _label:
    def __getattr__(self, attr: str) -> None:
        raise RuntimeError(f'do not use label.{attr} outside of @goto functions')


goto = _goto()
label = _label()


def _type_check() -> None:
    @goto
    def f(x: int) -> str:
        pass


def _test() -> None:
    @goto
    def gcd(a: int, b: int) -> int:
        label.start
        if a < b:
            goto.swap
        else:
            goto.main
        label.swap
        a, b = b, a
        label.main
        a, b = b, a % b
        if not a:
            goto.end
        if not b:
            goto.end
        goto.start
        label.end
        return a

    assert gcd(1, 1) == 1
    assert gcd(1, 2) == 1
    assert gcd(2, 3) == 1
    assert gcd(3, 6) == 3
    assert gcd(24, 100) == 4

    @goto
    def test_loop(l: list[int], x: int) -> list[int]:
        res: list[int] = []
        for i in l:
            if i == x:
                goto.loop2
            res.append(i)
        for i in ():
            res.append(i)
            label.loop2
        return res

    assert test_loop([1, 2, 3, 2, 4, 5], 2) == [1, 3, 2, 4, 5]


if __name__ == '__main__':
    _test()
