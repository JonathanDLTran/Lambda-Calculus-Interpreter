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
                 Lambda, App, Let,
                 Definition,
                 Begin, Def)


def eval_expr(expr, ctx):
    """
    evaluate expr to a value and return value and updated context,
    in a non-quasiquoted environment
    """
    assert isinstance(expr, Expr)
    assert isinstance(ctx, dict)
    if isinstance(expr, Constant):
        return expr, ctx
    elif type(expr) == Var:
        return eval_var(expr, ctx)
    elif type(expr) == Quote:
        return eval_quote(expr, ctx)
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
    elif type(expr) == App:
        return eval_app(expr, ctx)


def eval_app(expr, ctx):
    assert type(expr) == App
    fun = expr.get_fun()
    fun_val, ctx1 = eval_expr(fun, ctx)
    new_ctx = deepcopy(ctx1)
    args = expr.get_args()
    arg_vals = []
    for arg in args:
        arg_val, new_ctx = eval_expr(arg, new_ctx)
        arg_vals.append(arg_val)
    if type(fun_val) == Lambda:
        fun_val_names = fun_val.get_args()
        fun_val_body = fun_val.get_body()
        final_ctx = deepcopy(new_ctx)
        if len(fun_val_names) != len(arg_vals):
            raise RuntimeError(
                f"Incorrect Arity: Function {fun_val} requires {len(fun_val_names)} \
                    arguments and {len(arg_vals)} arguments were provided.")
        for arg_name, arg_val in zip(fun_val_names, arg_vals):
            final_ctx[arg_name] = arg_val
        return eval_expr(fun_val_body, final_ctx)
    else:
        raise RuntimeError(
            f"Application must begin with function; instead {fun} was given.")


def eval_let(expr, ctx):
    assert type(expr) == Let
    bindings = expr.get_bindings()
    bodies = expr.get_bodies()
    new_ctx = deepcopy(ctx)
    for name, bind_expr in bindings:
        value, _ = eval_expr(bind_expr, ctx)
        new_ctx[name] = value
    for body_expr in bodies:
        value, new_ctx = eval_expr(body_expr, new_ctx)
    return value, new_ctx


def eval_var(expr, ctx):
    assert type(expr) == Var
    var = expr.get_var()
    if var not in ctx:
        raise RuntimeError(f"Unbound variable : {var} in frame : {ctx}")
    return ctx[var], ctx


def eval_quote(expr, ctx):
    assert type(expr) == Quote
    return expr.get_datum(), ctx


def eval_unquote(expr, ctx):
    assert type(expr) == Unquote
    raise RuntimeError(
        f"Unquote not nested in a quasiquote : {expr} | frame : {ctx}")


def eval_set(expr, ctx):
    assert type(expr) == Set
    expr_val, _ = eval_expr(expr.get_expr(), ctx)
    var = expr.get_var()
    if var not in ctx:
        raise RuntimeError(f"Variable {var} not bound in current frame {ctx}.")
    new_ctx = deepcopy(ctx)
    new_ctx[var] = expr_val
    # Undefined Return Value for a Set Expression
    return None, new_ctx


def eval_ifelse(expr, ctx):
    assert type(expr) == IfElse
    b, _ = eval_expr(expr.get_guard(), ctx)
    if b.get_value():
        return eval_expr(expr.get_fst(), ctx)
    else:
        return eval_expr(expr.get_snd(), ctx)


def eval_if(expr, ctx):
    assert type(expr) == If
    b, _ = eval_expr(expr.get_guard(), ctx)
    if b.get_value():
        return eval_expr(expr.get_expr(), ctx)
    else:
        # Undefined Return Value for a 1 sided If Expression
        return None, ctx


def eval_lambda(expr, ctx):
    assert type(expr) == Lambda
    return expr, ctx


def eval_quasiquote(expr, ctx):
    assert type(expr) == Quasiquote
    return qeval_expr(expr.get_expr(), ctx)


def qeval_expr(expr, ctx):
    assert isinstance(expr, Expr)
    assert isinstance(ctx, dict)
    if isinstance(expr, Constant):
        return expr, ctx
    elif type(expr) == Var:
        return expr, ctx
    elif type(expr) == Quote:
        # lose all unquoting inside this nested quote
        return expr, ctx
    elif type(expr) == Unquote:
        return eval_expr(expr.get_expr(), ctx)
    elif type(expr) == Quasiquote:
        # lose all unuoting inside this nested quasiquote
        return expr, ctx
    elif type(expr) == If:
        return qeval_if(expr, ctx)
    elif type(expr) == IfElse:
        return qeval_ifelse(expr, ctx)
    elif type(expr) == Set:
        return qeval_set(expr, ctx)
    elif type(expr) == Lambda:
        return qeval_lambda(expr, ctx)
    elif type(expr) == Let:
        return qeval_let(expr, ctx)
    elif type(expr) == App:
        return qeval_app(expr, ctx)


def qeval_app(expr, ctx):
    assert type(expr) == App
    args = expr.get_args()
    fun = expr.get_fun()
    new_fun, ctx1 = qeval_expr(fun, ctx)
    new_ctx = deepcopy(ctx1)
    new_args = []
    for arg in args:
        new_arg, new_ctx = qeval_expr(arg, new_ctx)
        new_args.append(new_arg)
    return App(new_fun + new_args), new_ctx


def qeval_if(expr, ctx):
    assert type(expr) == If
    guard = expr.get_guard()
    body = expr.get_expr()
    new_guard, ctx1 = qeval_expr(guard, ctx)
    new_body, ctx2 = qeval_expr(body, ctx1)
    return If(new_guard, new_body), ctx2


def qeval_ifelse(expr, ctx):
    assert type(expr) == IfElse
    guard = expr.get_guard()
    fst = expr.get_fst()
    snd = expr.get_snd()
    new_guard, ctx1 = qeval_expr(guard, ctx)
    new_fst, ctx2 = qeval_expr(fst, ctx1)
    new_snd, ctx3 = qeval_expr(snd, ctx2)
    return IfElse(new_guard, new_fst, new_snd), ctx2


def qeval_set(expr, ctx):
    assert type(expr) == Set
    body = expr.get_expr()
    var = expr.get_var()
    new_body, ctx1 = qeval_expr(body, ctx)
    return Set(var, body), ctx1


def qeval_lambda(expr, ctx):
    assert type(expr) == Lambda
    args = expr.get_args()
    body = expr.get_body()
    new_body, ctx1 = qeval_expr(body, ctx)
    return Lambda(args, new_body), ctx1


def qeval_let(expr, ctx):
    assert type(expr) == Let
    bindings = expr.get_bindings()
    bodies = expr.get_bodies()
    names = list(map(lambda pair: pair[0], bindings))
    bind_exprs = list(map(lambda pair: pair[1], bindings))
    new_bind_exprs = []
    new_ctx = deepcopy(ctx)
    for bind_expr in bind_exprs:
        new_bind_expr, new_ctx = qeval_expr(bind_expr, new_ctx)
        new_bind_exprs.append(new_bind_expr)
    new_bindings = list(zip(names, bind_exprs))
    new_bodies = []
    for body in bodies:
        new_body, new_ctx = qeval_expr(body, new_ctx)
        new_bodies.append(new_body)
    return Let(new_bindings, new_bodies), new_ctx


def eval_definition(definition, ctx):
    assert isinstance(definition, Definition)
    assert type(ctx) == dict
    if type(definition) == Def:
        return eval_def(definition, ctx)
    elif type(definition) == Begin:
        exprs = definition.get_exprs()
        return eval_begin(definition, ctx)


def eval_def(definition, ctx):
    assert type(definition) == Def
    expr = definition.get_expr()
    val, new_ctx = eval_expr(expr, ctx)
    var = definition.get_var()
    new_ctx[var] = val
    return var, new_ctx


def eval_begin(definition, ctx):
    assert type(definition) == Begin
    exprs = definition.get_exprs()
    new_ctx = deepcopy(ctx)
    for expr in exprs:
        val, new_ctx = eval_expr(expr, new_ctx)
    return val, new_ctx


def eval_expr(expr, ctx):
    assert type(expr) == list
    if len(expr) == 0:
        raise RuntimeError(
            f"Scheme Evaluation Error: Empty Expression: {expr}")
    fst = expr[0]
    if fst == "+":
        pass


def eval_plus(expr, ctx):
    assert len(expr) > 3
    assert expr[0] == "+"
    for sub_expr in expr[1:]:
        eval_expr


def bool_to_str(b):
    assert type(b) == bool
    if b:
        return "#t"
    return "#f"


def expr_to_str(expr):
    assert type(expr) == list
    if len(expr) == 1:
        elt = expr[0]
        if type(elt) == str:
            return elt
        elif type(elt) == int:
            return str(elt)
        elif type(elt) == bool:
            return bool_to_str(elt)
    output = "("
    for i, elt in enumerate(expr):
        if type(elt) == str:
            output += elt
        elif type(elt) == int:
            output += str(elt)
        elif type(elt) == bool:
            output += bool_to_str(elt)
        elif type(elt) == list:
            output += expr_to_str(elt)
        else:
            raise RuntimeError(
                f"Expr to String Error: {elt} does not match any scheme type")
        if i != len(expr) - 1:
            output += " "
    output += ")"
    return output


OPEN_PAREN = "("
CLOSE_PAREN = ")"
OPEN_BRACKET = "["
CLOSE_BRACKET = "]"
SPACE = " "


class String():
    def __init__(self, s):
        super().__init__()
        self.string = s


def lex(string):
    str1 = string.replace(OPEN_PAREN, f"{OPEN_PAREN}{SPACE}")
    str2 = str1.replace(CLOSE_PAREN, f"{SPACE}{CLOSE_PAREN}")
    tokens = str2.split()
    new_tokens = []
    for token in tokens:
        if token == "#t":
            new_tokens.append(True)
        elif token == "#f":
            new_tokens.append(False)
        elif token.isdigit():
            new_tokens.append(int(token))
        elif token[0] == '\"' and token[-1] == '\"':
            new_tokens.append(String(token))
        else:
            new_tokens.append(token)
    return new_tokens


def parse(tokens):
    # if len(tokens) < 2:
    #     raise RuntimeError(f"Scheme Requires At Least 2 Tokens: {tokens}")
    # if tokens[0] != OPEN_PAREN:
    #     raise RuntimeError(
    #         f"Scheme Requires Expression Begin with Open Parentheses: {tokens}")
    # if tokens[-1] != CLOSE_PAREN:
    #     raise RuntimeError(
    #         f"Scheme Requires Expression End with Close Parentheses: {tokens}")

    # inner_tokens = tokens[1:-1]
    stack = [[]]
    for token in tokens:
        print(stack)
        if token == OPEN_PAREN:
            stack.append([])
        elif token == CLOSE_PAREN:
            inner_expr = stack.pop()
            stack[-1].append(inner_expr)
        else:
            stack[-1].append(token)
    print(stack)

    if len(stack) != 1:
        raise RuntimeError(
            f"Scheme Requires Open Parentheses Paired With Closing Parentheses: {tokens}")

    return stack.pop().pop()


def frontend(string):
    return parse(lex(string))


if __name__ == "__main__":
    string = r'(+ 1 (+ 3 4) (- 1 2))'
    string = r'1'
    print(expr_to_str(frontend(string)))
