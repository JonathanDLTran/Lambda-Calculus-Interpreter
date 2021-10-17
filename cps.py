"""
cps.py translates scheme code in continuation passing style.
"""
LAMBDA = "lambda"
APPLY = "apply"
K = "k"
K_COUNTER = 0


def gen_k():
    global K_COUNTER
    K_COUNTER += 1
    return f"{K}_{K_COUNTER}"


def to_cps(expr):
    if type(expr) == int:
        var = gen_k()
        return [LAMBDA, var, [APPLY, var, expr]]
    elif type(expr) == bool:
        return expr
    elif expr == NIL:
        return []
    elif type(expr) == str:
        if expr in ctx:
            return ctx[expr]
        # this is a symbol under quasi
        elif in_quasi:
            return expr
    elif type(expr) == String:
        return expr
    elif type(expr) == Values:
        raise RuntimeError(
            f"Cannot evaluate Values Internal Class any further; {expr}.")

    assert type(expr) == list
    # allow greater than or equal to 1 for function with no args
    assert len(expr) >= 1

    first = expr[0]
    # Named Arithmetic Operators
    if first == ADD:
        return eval_add(expr, ctx, in_quasi)
    elif first == SUB:
        return eval_sub(expr, ctx, in_quasi)
    elif first == MUL:
        return eval_mul(expr, ctx, in_quasi)
    elif first == DIV:
        return eval_div(expr, ctx, in_quasi)
    elif first == EXP:
        return eval_exp(expr, ctx, in_quasi)
    elif first == CONCAT:
        return eval_concat(expr, ctx, in_quasi)
    # Named Special Forms
    elif first == QUOTE:
        return eval_quote(expr, ctx, in_quasi)
    elif first == PRINTLN:
        return eval_println(expr, ctx, in_quasi)
    elif first == SET:
        return eval_set(expr, ctx, in_quasi)
    elif first == EQ:
        return eval_eq(expr, ctx, in_quasi)


def main():
    pass


if __name__ == "__main__":
    main()
