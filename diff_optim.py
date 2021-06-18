"""
diff_optim optimizes the output result of differentation following
predeined rules
"""
from parser_classes import *
from token_constants import *
from diff_parse import parse_main
from diff_lex import lex


def opt_arith(op, l, r):
    assert op in OPS
    assert type(l) == Float
    assert type(r) == Float

    v_l = l.get_f()
    v_r = r.get_f()

    if op == ADD:
        return Float(v_l + v_r)
    elif op == SUB:
        return Float(v_l - v_r)
    elif op == MUL:
        return Float(v_l * v_r)
    elif op == DIV:
        return Float(v_l / v_r)
    elif op == POW:
        return Float(v_l ** v_r)
    else:
        raise RuntimeError(
            f"Undefined operator {op} when doing arithmetic optimization.")


def opt_unop(expr):
    assert type(expr) == Unop

    op = expr.get_op()
    e = optimize(expr.get_e())

    if op == SUB and type(e) == Float and e.get_f() == 0.:
        return Float(0.)
    elif type(e) == Unop and op == SUB:
        return e.get_e()
    return Unop(op, e)


def opt_func(expr):
    assert type(expr) == Function

    f = expr.get_f()
    e = optimize(expr.get_e())

    if f == LN and type(e) == Float and e.get_f() == 0.:
        return Float(0)
    elif f == SIN and type(e) == Float and e.get_f() == 0.:
        return Float(0)
    elif f == COS and type(e) == Float and e.get_f() == 0.:
        return Float(1)
    return Function(f, e)


def opt_binop(expr):
    assert type(expr) == Binop

    op = expr.get_op()
    l = expr.get_l()
    r = expr.get_r()
    l_opt = optimize(l)
    r_opt = optimize(r)

    if type(l_opt) == Float and type(r_opt) == Float:
        return opt_arith(op, l_opt, r_opt)
    elif type(l_opt) == Float and l_opt.get_f() == 0. and op == ADD:
        return r_opt
    elif type(r_opt) == Float and r_opt.get_f() == 0. and op == ADD:
        return l_opt
    elif type(l_opt) == Float and l_opt.get_f() == 0. and op == SUB:
        return Unop(SUB, r_opt)
    elif type(r_opt) == Float and r_opt.get_f() == 0. and op == SUB:
        return l_opt
    elif type(l_opt) == Float and l_opt.get_f() == 0. and op == DIV:
        # we just define anything, including 0/0 = 0
        return Float(0)
    elif type(r_opt) == Float and r_opt.get_f() == 1. and op == DIV:
        return l_opt
    elif type(l_opt) == Float and l_opt.get_f() == 1. and op == MUL:
        return r_opt
    elif type(r_opt) == Float and r_opt.get_f() == 1. and op == MUL:
        return l_opt
    elif type(l_opt) == Float and l_opt.get_f() == 0. and op == MUL:
        return Float(0)
    elif type(r_opt) == Float and r_opt.get_f() == 0. and op == MUL:
        return Float(0)
    elif type(r_opt) == Float and r_opt.get_f() == 0. and op == POW:
        return Float(1)
    elif type(l_opt) == Float and l_opt.get_f() == 0. and op == POW:
        return Float(0)
    elif type(r_opt) == Float and r_opt.get_f() == 1. and op == POW:
        return l_opt
    elif r_opt == l_opt and op == ADD:
        return Binop(MUL, Float(2), r_opt)
    elif r_opt == l_opt and op == MUL:
        return Binop(POW, r_opt, Float(2))
    elif r_opt == l_opt and op == SUB:
        return Float(0)
    elif r_opt == l_opt and op == DIV:
        return Float(1)
    elif type(l_opt) == Unop and op == ADD:
        return optimize(Binop(SUB, r_opt, l_opt.get_e()))
    elif type(r_opt) == Unop and op == ADD:
        return optimize(Binop(SUB, l_opt, r_opt.get_e()))
    elif type(r_opt) == Unop and op == SUB:
        return optimize(Binop(ADD, l_opt, r_opt.get_e()))
    elif type(l_opt) == Unop and op == SUB:
        return optimize(Unop(SUB, Binop(ADD, l_opt.get_e(), r_opt)))
    elif type(l_opt) == Unop and op == MUL:
        return optimize(Unop(SUB, Binop(MUL, l_opt.get_e(), r_opt)))
    elif type(r_opt) == Unop and op == MUL:
        return optimize(Unop(SUB, Binop(MUL, l_opt, r_opt.get_e())))
    elif type(l_opt) == Binop and l_opt.get_op() == DIV and op == MUL:
        return optimize(Binop(DIV, Binop(MUL, l_opt.get_l(), r_opt), l_opt.get_r()))
    elif type(r_opt) == Binop and r_opt.get_op() == DIV and op == MUL:
        return optimize(Binop(DIV, Binop(MUL, l_opt, r_opt.get_l()), r_opt.get_r()))
    elif type(l_opt) == Unop and op == DIV:
        return optimize(Unop(SUB, Binop(DIV, l_opt.get_e(), r_opt)))
    elif type(r_opt) == Unop and op == DIV:
        return optimize(Unop(SUB, Binop(DIV, l_opt, r_opt.get_e())))
    elif type(l_opt) == Binop and l_opt.get_op() == DIV and op == DIV:
        return optimize(Binop(DIV, l_opt.get_l(), Binop(MUL, l_opt.get_r(), r_opt)))
    elif type(r_opt) == Binop and r_opt.get_op() == DIV and op == DIV:
        return optimize(Binop(DIV, Binop(MUL, l_opt, r_opt.get_r()), r_opt.get_l()))
    elif type(r_opt) == Unop and op == POW:
        return optimize(Binop(DIV, Float(1), Binop(POW, l_opt, r_opt.get_e())))
    elif type(l_opt) == Binop and l_opt.get_op() == POW and op == POW:
        return optimize(Binop(POW, l_opt.get_l(), Binop(MUL, l_opt.get_r(), r_opt)))
    return Binop(op, l_opt, r_opt)


def opt_float(expr):
    assert type(expr) == Float

    f = expr.get_f()
    if f < 0:
        return optimize(Unop(SUB, Float(abs(f))))
    return expr


def optimize(expr):
    assert isinstance(expr, Expr)

    if type(expr) == Float:
        return opt_float(expr)
    elif type(expr) == Const:
        return expr
    elif type(expr) == Var:
        return expr
    elif type(expr) == Unop:
        return opt_unop(expr)
    elif type(expr) == Function:
        return opt_func(expr)
    elif type(expr) == Binop:
        return opt_binop(expr)
    raise RuntimeError(f"Cannot match expression {expr} in optimize.")


def test():
    deriv = Unop(SUB, Unop(SUB, Float(1)))
    deriv = Binop(ADD, Unop(SUB, Var("f")), Float(3))
    deriv = Binop(ADD,  Float(3), Unop(SUB, Var("f")))
    deriv = Float(-3)
    deriv = Binop(SUB, Float(3), Unop(SUB, Var("f")))
    deriv = Binop(SUB, Unop(SUB, Var("f")), Float(3))
    deriv = Binop(MUL, Float(-1), Var("f"))
    deriv = Binop(MUL, Binop(DIV, Var("f"), Float(3)), Float(2))
    deriv = Binop(ADD, Var("x"), Binop(
        SUB, Function(SIN, Var("x")), Function(SIN, Var("x"))))
    optim = optimize(deriv)
    print(deriv)
    print(optim)


if __name__ == "__main__":
    test()
