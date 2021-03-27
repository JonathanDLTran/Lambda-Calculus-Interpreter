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
    # expr = Let([("x", Integer(3))], [Var("x")])
    # expr = Quasiquote(
    #     IfElse(Boolean(False), Set("x", Integer(1)), Integer(-1)))
    # expr = Quasiquote(Lambda(["x"], Unquote(Integer(3))))
    # expr = Quasiquote(Let([("x", Integer(3))], [Var("x")]))
    # expr = Quasiquote(Quasiquote(
    #     Unquote(IfElse(Boolean(False), Integer(3), Integer(4)))))
    # expr = Quasiquote(Quote(
    #     Unquote(IfElse(Boolean(False), Integer(3), Integer(4)))))
    # expr = Quote("a")
    # expr = App([Lambda(["x"], Var("x")), Integer(1)])
    # expr = Quasiquote(Unquote(App([Lambda(["x"], Var("x")), Integer(1)])))
    expr = Quasiquote(Quasiquote(App([Lambda(["x"], Var("x")), Integer(1)])))
    ctx = {}
    result, _ = eval_expr(expr, ctx)
    print(result)
    return result


if __name__ == "__main__":
    main()
