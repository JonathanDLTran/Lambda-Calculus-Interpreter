from ast import *


def is_def():
    pass


def is_use():
    pass


def is_expr(expr):
    assert isinstance(expr, Expr)


def get_expr_uses(expr):
    assert isinstance(expr, Expr)
    assert is_expr(expr)


def prop_func(func):
    assert type(func) == Function


def prop_for():
    pass


def prop_while():
    pass


def prop_if():
    pass


def prop_program():
    pass


def prop():
    pass


def main():
    pass


def test():
    pass


if __name__ == "__main__":
    test()
