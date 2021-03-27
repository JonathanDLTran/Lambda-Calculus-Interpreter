"""
Evaluates scheme definitions and expressions

Citations:
Grammar and Evaluation Semantics:
https://inst.eecs.berkeley.edu/~cs61a/sp19/articles/scheme-spec.html#quasiquote
https://ds26gte.github.io/tyscheme/index-Z-H-5.html
Racket Guide for quoting:
https://docs.racket-lang.org/reference/quasiquote.html
Grammar:
https://www.cs.cmu.edu/Groups/AI/html/r4rs/r4rs_6.html
https://www.scheme.com/tspl2d/grammar.html
https://www.scheme.com/tspl4/grammar.html
"""

from copy import deepcopy

from ast import (Expr,
                 Var,
                 Constant, Boolean, Integer, String,
                 Quote, Unquote, Quasiquote,
                 If, IfElse,
                 Set,
                 Lambda, App, Let)


def eval_expr(expr, ctx):
    """
    evaluate expr to a value and return value and updated context,
    in a non-quasiquoted environment
    """
    assert isinstance(expr, Expr)
    assert isinstance(ctx, dict)
    if isinstance(expr, Constant):
        return eval_constant(expr, ctx)
    elif type(expr) == Var:
        return eval_var(expr, ctx)
    elif type(expr) == Quote:
        return expr.get_datum(), ctx
    elif type(expr) == Unquote:
        return eval_unquote(expr, ctx)
    elif type(expr) == Quasiquote:
        return eval_quasiquote(expr, ctx)
    elif type(expr) == If:
        return eval_if(expr, ctx)
    elif type(expr) == IfElse:
        return eval_ifelse(expr, ctx)
    elif type(expr) == Set:
        return eval_set(expr, ctx)
    elif type(expr) == Lambda:
        return eval_lambda(expr, ctx)
    elif type(expr) == Let:
        return eval_let(expr, ctx)


def eval_let(expr, ctx):
    assert type(expr) == Let
    bindings = expr.get_bindings()
    bodies = expr.get_bodies()
    new_ctx = deepcopy(ctx)
    for name, bind_expr in bindings:
        new_ctx[name] = eval_expr(bind_expr, ctx)
    for body_expr in bodies:
        value, new_ctx = eval_expr(body_expr, new_ctx)
    return value, new_ctx


def eval_constant(expr, ctx):
    assert isinstance(expr, Constant)
    if type(expr) == Boolean:
        return expr.get_value(), ctx
    elif type(expr) == Integer:
        return expr.get_value(), ctx
    elif type(expr) == String:
        return expr.get_value(), ctx


def eval_var(expr, ctx):
    assert type(expr) == Var
    var = expr.get_var()
    if var not in ctx:
        raise RuntimeError(f"Unbound variable : {var} in frame : {ctx}")
    return ctx[var], ctx


def eval_unquote(expr, ctx):
    assert type(expr) == Unquote
    raise RuntimeError(
        f"Unquote not nested in a quasiquote : {expr} | frame : {ctx}")


def eval_set(expr, ctx):
    assert type(expr) == Set
    expr_val = eval_expr(expr.get_expr(), ctx)
    var = expr.get_var()
    if var not in ctx:
        raise RuntimeError(f"Variable {var} not bound in current frame {ctx}.")
    new_ctx = deepcopy(ctx)
    new_ctx[var] = expr_val
    # Undefined Return Value for a Set Expression
    return None, new_ctx


def eval_ifelse(expr, ctx):
    assert type(expr) == IfElse
    b = eval_expr(expr.get_guard(), ctx)
    if b:
        return eval_expr(expr.get_fst(), ctx)
    else:
        return eval_expr(expr.get_snd(), ctx)


def eval_if(expr, ctx):
    assert type(expr) == If
    b = eval_expr(expr.get_guard(), ctx)
    if b:
        return eval_expr(expr.get_expr(), ctx)
    else:
        # Undefined Return Value for a 1 sided If Expression
        return None, ctx


def eval_lambda(expr, ctx):
    assert type(expr) == Lambda
    return expr, ctx


def eval_quasiquote(expr, ctx):
    assert type(expr) == Unquote


def eval_inside_quasiquote(expr, ctx):
    pass
