"""
cps.py translates scheme code in continuation passing style.
"""
from constants import *
from scheme_classes import *
from eval import eval_expr, expr_to_str

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
    if first in [ADD, SUB, MUL, DIV, EXP, CONCAT, EQ, AND, OR, NEQ, LT, LTE, GT, GTE]:
        k = gen_k()
        first_arg = expr[1]
        var1 = gen_k()
        second_arg = expr[2]
        var2 = gen_k()
        return [LAMBDA, [k], [to_cps(first_arg), [LAMBDA, [var1], [to_cps(second_arg), [LAMBDA, [var2], [k, [first, var1, var2]]]]]]]
    # # Named Special Forms
    elif first == QUOTE:
        k = gen_k()
        return [LAMBDA, [k], [k, expr]]
    elif first == SET:
        k = gen_k()
        var = expr[1]
        set_expr = expr[2]
        var1 = gen_k()
        return [LAMBDA, [k], [to_cps(set_expr), [LAMBDA, [var1], [k, [SET, var, var1]]]]]
    elif first in [PRINTLN, NOT, CAR, CDR]:
        k = gen_k()
        bexpr = expr[1]
        var1 = gen_k()
        return [LAMBDA, [k], [to_cps(bexpr), [LAMBDA, [var1], [k, [first, var1]]]]]
    elif first == CONS:
        k = gen_k()
        left = expr[1]
        right = expr[2]
        var1 = gen_k()
        var2 = gen_k()
        return [LAMBDA, [k], [to_cps(left), [LAMBDA, [var1], [to_cps(right), [LAMBDA, [var2], [k, [CONS, var1, var2]]]]]]]


def main():
    tests = [
        1,
        0,
        True,
        False,
        [SUB, [ADD, 1, 2], 2],
        [MUL, 3, 4],
        [QUOTE, 3],
        [QUOTE, [ADD, 1, 2]],
        [PRINTLN, [ADD, 1, 2]],
        [SET, "x", [DIV, 3, 3]],
        [EQ, 1, [DIV, 3, 3]],
        [AND, True, False],
        [OR, False, False],
        [LT, 3, 2],
        [NOT, False],
        [NOT, True],
        [CONS, [EXP, 3, 2], [ADD, 1, 2]],
        [CAR, [CONS, [EXP, 3, 2], [ADD, 1, 2]]],
        [CDR, [CONS, [EXP, 3, 2], [ADD, 1, 2]]],
    ]
    for program in tests:
        print("-" * 70)
        print(f"Program is: {program}")
        cps = to_cps(program)
        starting = [LAMBDA, [K], K]
        result = [cps, starting]
        print(f"CPS result is: {result}")
        evaluated = expr_to_str(eval_expr(result, {}, False))
        print(f"Evaluation gives: {evaluated}")


if __name__ == "__main__":
    main()
