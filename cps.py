"""
cps.py translates scheme code in continuation passing style.
"""
from constants import *
from scheme_classes import *
from eval import eval_expr

K = "k"
K_COUNTER = 0


def gen_k():
    global K_COUNTER
    K_COUNTER += 1
    return f"{K}_{K_COUNTER}"


def to_cps(expr):
    if type(expr) == int:
        var = gen_k()
        return [LAMBDA, [var], [var, expr]]
    elif type(expr) == bool:
        var = gen_k()
        return [LAMBDA, [var], [var, expr]]
    elif expr == NIL:
        var = gen_k()
        return [LAMBDA, [var], [var, expr]]
    elif type(expr) == str:
        var = gen_k()
        return [LAMBDA, [var], [var, expr]]
    elif type(expr) == String:
        var = gen_k()
        return [LAMBDA, [var], [var, expr]]
    elif type(expr) == Values:
        raise RuntimeError(
            f"Cannot evaluate Values Internal Class any further; {expr}.")

    assert type(expr) == list
    # allow greater than or equal to 1 for function with no args
    assert len(expr) >= 1

    first = expr[0]
    # Named Arithmetic Operators
    if first in [ADD, SUB, MUL, DIV, EXP, CONCAT]:
        k = gen_k()
        first_arg = expr[1]
        var1 = gen_k()
        second_arg = expr[2]
        var2 = gen_k()
        return [LAMBDA, [k], [to_cps(first_arg), [LAMBDA, [var1], [to_cps(second_arg), [LAMBDA, [var2], [k, [first, var1, var2]]]]]]]
    # # Named Special Forms
    # elif first == QUOTE:
    #     return eval_quote(expr, ctx, in_quasi)
    # elif first == PRINTLN:
    #     return eval_println(expr, ctx, in_quasi)
    # elif first == SET:
    #     return eval_set(expr, ctx, in_quasi)
    # elif first == EQ:
    #     return eval_eq(expr, ctx, in_quasi)


def main():
    program = [SUB, [ADD, 1, 2], 2]
    cps = to_cps(program)
    starting = [LAMBDA, [K], K]
    result = [cps, starting]
    print(result)
    evaled = eval_expr(result, {}, False)
    print(evaled)


if __name__ == "__main__":
    main()
