from ast import (Expr,
                 Var,
                 Constant, Boolean, Integer, String,
                 Quote, Unquote, Quasiquote,
                 If, IfElse,
                 Set,
                 Lambda, App, Let)
from eval import eval_expr


def main():
    # expr = IfElse(Boolean(False), Integer(3), Integer(4))
    # expr = Lambda(["x"], Let([('x', Integer(3))], [Integer(3)]))
    expr = Let([("x", Integer(3))], [Var("x")])
    ctx = {}
    result, _ = eval_expr(expr, ctx)
    print(result)
    return result


if __name__ == "__main__":
    main()
