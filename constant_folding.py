from ast import *

ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"


def fold_int_bop(left, right, op):
    assert type(left) == IntValue and type(right) == IntValue
    if op == ADD:
        return IntValue(left.get_value() + right.get_value())
    elif op == SUB:
        return IntValue(left.get_value() - right.get_value())
    elif op == MUL:
        return IntValue(left.get_value() * right.get_value())
    elif op == DIV:
        return IntValue(left.get_value() // right.get_value())
    raise RuntimeError(
        f"Unsupported int binary oepration in constant folding: {left} {op} {right}")


def fold_bop(expr):
    assert type(expr) == Bop
    left = fold_expr(expr.get_left())
    right = fold_expr(expr.get_right())
    op = expr.get_bop()

    if type(left) == IntValue and type(right) == IntValue:
        return fold_int_bop(left, right, op)
    print(f"Currently not supported constant folding {expr}.")
    return expr


def fold_expr(expr):
    assert isinstance(expr, Expr)
    if type(expr) == IntValue:
        return expr
    elif type(expr) == BoolValue:
        return expr
    elif type(expr) == FloatValue:
        return expr
    elif type(expr) == StrValue:
        return expr
    elif type(expr) == VarValue:
        return expr
    elif type(expr) == Bop:
        return fold_bop(expr)


def main():
    pass


def test():
    expr = Bop(ADD, IntValue(3), IntValue(4))
    result = fold_expr(expr)
    print(result)


if __name__ == "__main__":
    test()
