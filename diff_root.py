from parser_classes import *
from token_constants import *
from math import sin, cos, log
from diff import diff
from diff_lex import lex
from diff_parse_fast import parse
from diff_optim import optimize


def eval_binop(expr, v):
    assert type(expr) == Binop
    assert type(v) == float

    op = expr.get_op()
    l = expr.get_l()
    r = expr.get_r()

    if op == ADD:
        return eval_expr(l, v) + eval_expr(r, v)
    elif op == SUB:
        return eval_expr(l, v) - eval_expr(r, v)
    elif op == MUL:
        return eval_expr(l, v) * eval_expr(r, v)
    elif op == DIV:
        return eval_expr(l, v) / eval_expr(r, v)
    elif op == POW:
        return eval_expr(l, v) ** eval_expr(r, v)
    else:
        raise RuntimeError(
            f"Undefined operator {op} when doing arithmetic optimization.")


def eval_function(expr, v):
    assert type(expr) == Function
    f = expr.get_f()
    e = expr.get_e()

    if f == SIN:
        return sin(eval_expr(e, v))
    elif f == COS:
        return cos(eval_expr(e, v))
    elif f == LN:
        return log(eval_expr(e, v))
    raise RuntimeError(
        f"Undefined function {f} when doing function evaluation.")


def eval_unop(expr, v):
    assert type(expr) == Unop
    o = expr.get_op()
    e = expr.get_e()

    if o == SUB:
        return -1 * eval_expr(e, v)
    raise RuntimeError(
        f"Undefined unary operator {o} when doing unary operator evaluation.")


def eval_expr(expr, v):
    assert isinstance(expr, Expr)
    assert type(v) == float
    assert v != None

    if type(expr) == Float:
        return expr.get_f()
    elif type(expr) == Const:
        return expr.get_c()
    elif type(expr) == Var:
        return v
    elif type(expr) == Function:
        return eval_function(expr, v)
    elif type(expr) == Binop:
        return eval_binop(expr, v)
    elif type(expr) == Unop:
        return eval_unop(expr, v)


def newton_h(expr, guess, precision, niter):
    assert isinstance(expr, Expr)
    assert type(guess) == float
    assert type(precision) == float
    assert precision >= 0
    assert type(niter) == int
    assert niter >= 0

    if niter == 0:
        if abs(eval_expr(expr, guess)) < precision:
            return guess
        # no valid root found
        return None
    if abs(eval_expr(expr, guess)) < precision:
        return guess

    new_guess = guess - eval_expr(expr, guess) / (
        eval_expr(diff(expr), guess) if eval_expr(diff(expr), guess) != 0 else 10E-15)

    return newton_h(expr, new_guess, precision, niter - 1)


def newton(expr, guess, precision, niter):
    assert isinstance(expr, Expr)
    assert type(guess) == float
    assert type(precision) == float
    assert precision >= 0
    assert type(niter) == int
    assert niter >= 0

    return newton_h(expr, guess, precision, niter)


def main():
    print("Root Finding With Newton's Method")
    while True:
        try:
            string = input("expression > ")
            guess = input("guess > ")
            try:
                guess = float(guess)
            except Exception:
                raise Exception()
            precision = input("precision > ")
            try:
                precision = float(precision)
            except Exception:
                raise Exception()
            niter = input("iterations > ")
            try:
                niter = int(niter)
            except Exception:
                raise Exception()
            tokens = lex(string)
            expr = parse(tokens)
            root = newton(expr, guess, precision, niter)
            if root == None:
                print("No root was found.")
            else:
                print(root)
            print()
        except KeyboardInterrupt:
            print("Quitting...")
            exit(0)
        except Exception:
            print("Issue in expression or guess. ")
            continue


if __name__ == "__main__":
    main()
