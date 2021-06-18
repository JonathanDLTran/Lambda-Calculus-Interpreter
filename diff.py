from token_constants import *
from parser_classes import *
from diff_parse import parse_main
from diff_lex import lex


def contains_var(expr):
    assert isinstance(expr, Expr)

    if type(expr) == Float:
        return False
    elif type(expr) == Const:
        return False
    elif type(expr) == Var:
        return True
    elif type(expr) == Function:
        return contains_var(expr.get_e())
    elif type(expr) == Binop:
        return contains_var(expr.get_l()) or contains_var(expr.get_r())
    elif type(expr) == Unop:
        return contains_var(expr.get_e())


def diff_function(expr):
    assert type(expr) == Function

    f = expr.get_f()
    e = expr.get_e()

    if f == SIN:
        return Binop(MUL, diff(e), Function(COS, e))
    elif f == COS:
        return Binop(MUL, diff(e), Unop(SUB, Function(SIN, e)))
    elif f == LN:
        return Binop(DIV, diff(e), e)
    raise RuntimeError(f"Cannot match on function {f} in {expr}.")


def diff_binop(expr):
    assert type(expr) == Binop

    op = expr.get_op()
    l = expr.get_l()
    r = expr.get_r()

    if op == ADD or op == SUB:
        return Binop(op, diff(l), diff(r))
    elif op == MUL:
        return Binop(ADD, Binop(MUL, diff(l), r), Binop(MUL, l, diff(r)))
    elif op == DIV:
        numerator = Binop(SUB, Binop(MUL, diff(l), r), Binop(l, diff(r)))
        denominator = Binop(POW, r, Float(2.))
        return Binop(DIV, numerator, denominator)
    elif op == POW:
        if not contains_var(r):
            return Binop(MUL, r, Binop(MUL, diff(l), Binop(POW, l, Binop(SUB, r, Float(1.)))))
        left = Binop(MUL, diff(r), Function(LN, l))
        right = Binop(DIV, Binop(MUL, diff(l), r), l)
        prefix = Binop(EXP, l, r)
        return Binop(MUL, prefix, Binop(ADD, left, right))
    raise RuntimeError(f"Cannot match on binary operation {op} in {expr}.")


def diff_unop(expr):
    assert type(expr) == Unop

    op = expr.get_op()
    e = expr.get_e()

    if op == SUB:
        return Unop(SUB, diff(e))
    raise RuntimeError(f"Cannot match on unary operation {op} in {expr}.")


def diff(expr):
    assert isinstance(expr, Expr)

    if type(expr) == Float:
        return Const(float(0))
    elif type(expr) == Const:
        return Const(float(0))
    elif type(expr) == Var:
        return Const(float(1))
    elif type(expr) == Function:
        return diff_function(expr)
    elif type(expr) == Binop:
        return diff_binop(expr)
    elif type(expr) == Unop:
        return diff_unop(expr)


def main():
    print("Automatic Differentiation")
    while True:
        try:
            string = input("> ")
            tokens = lex(string)
            expr = parse_main(tokens)
            deriv = diff(expr)
            print(deriv)
        except KeyboardInterrupt:
            print("Quitting...")
            exit(0)
        except Exception:
            print("Issue in expression. ")
            continue


def test():
    s = "3 + 4"
    tokens = lex(s)
    expr = parse_main(tokens)
    deriv = diff(expr)
    print(tokens)
    print(expr)
    print(deriv)


if __name__ == "__main__":
    main()
