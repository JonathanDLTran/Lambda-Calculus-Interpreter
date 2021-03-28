from ast import (Expr,
                 Var,
                 Constant, Boolean, Integer, String,
                 Quote, Unquote, Quasiquote,
                 If, IfElse,
                 Set,
                 Lambda, App, Let,
                 Begin, Def)
from eval import eval_expr, eval_definition
import lexer
import parser


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
    # expr = Quasiquote(Quasiquote(App([Lambda(["x"], Var("x")), Integer(1)])))
    # definition = Begin([App([Lambda(["x"], Var("x")), Integer(1)]), Quasiquote(
    #     Unquote(App([Lambda(["x"], Var("x")), Integer(1)])))])
    definition = Begin([Let([("x", Integer(10))], [Var("x")]), Var("x")])
    ctx = {}
    result, _ = eval_definition(definition, ctx)
    print(result)
    return result


if __name__ == "__main__":
    main()
