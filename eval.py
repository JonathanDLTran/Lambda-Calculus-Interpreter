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

from functools import reduce


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
    if type(expr) == int:
        return expr
    elif type(expr) == bool:
        return expr
    elif type(expr) == str:
        return ctx[expr]
    elif type(expr) == String:
        return expr

    assert type(expr) == list
    assert len(expr) >= 3

    first = expr[0]
    if first == "+":
        return eval_add(expr, ctx)
    elif first == "-":
        return eval_sub(expr, ctx)
    elif first == "*":
        return eval_mul(expr, ctx)
    elif first == "/":
        return eval_div(expr, ctx)


def eval_add(expr, ctx):
    assert len(expr) >= 3
    assert expr[0] == "+"
    vals = []
    for sub_expr in expr[1:]:
        val = eval_expr(sub_expr, ctx)
        vals.append(val)
    return reduce(lambda val, acc: val + acc, vals, 0)


def eval_sub(expr, ctx):
    assert len(expr) >= 3
    assert expr[0] == "-"
    vals = []
    first = expr[1]
    first_val = eval_expr(first, ctx)
    for sub_expr in expr[2:]:
        val = eval_expr(sub_expr, ctx)
        vals.append(val)
    vals = [first_val] + list(map(lambda v: -v, vals))
    return reduce(lambda val, acc: val + acc, vals, 0)


def eval_mul(expr, ctx):
    assert len(expr) >= 3
    assert expr[0] == "*"
    vals = []
    for sub_expr in expr[1:]:
        val = eval_expr(sub_expr, ctx)
        vals.append(val)
    return reduce(lambda val, acc: val * acc, vals, 1)


def eval_div(expr, ctx):
    assert len(expr) == 3
    assert expr[0] == "/"
    first = eval_expr(expr[1], ctx)
    second = eval_expr(expr[2], ctx)
    return int(first/second)


OPEN_PAREN = "("
CLOSE_PAREN = ")"
# OPEN_BRACKET = "["
# CLOSE_BRACKET = "]"
BRACES = [
    OPEN_PAREN,
    CLOSE_PAREN,
]
SPACE = " "
TRUE = "#t"
FALSE = "#f"


class String():
    def __init__(self, s):
        super().__init__()
        self.string = s

    def get_string(self):
        return self.string


def bool_to_str(b):
    assert type(b) == bool
    if b:
        return TRUE
    return FALSE


def expr_to_str(expr):
    if type(expr) == int:
        return str(expr)
    elif type(expr) == bool:
        return bool_to_str(expr)
    elif type(expr) == str:
        return expr
    elif type(expr) == String:
        return expr.get_string()

    assert type(expr) == list
    output_lst = []
    for e in expr:
        output_lst.append(expr_to_str(e))
    output = f"({' '.join(output_lst)})"
    return output


def lex(string):
    str1 = string.replace(OPEN_PAREN, f"{OPEN_PAREN}{SPACE}")
    str2 = str1.replace(CLOSE_PAREN, f"{SPACE}{CLOSE_PAREN}")
    tokens = str2.split()
    new_tokens = []
    for token in tokens:
        if token == TRUE:
            new_tokens.append(True)
        elif token == FALSE:
            new_tokens.append(False)
        elif token.isdigit():
            new_tokens.append(int(token))
        elif token[0] == '\"' and token[-1] == '\"':
            new_tokens.append(String(token))
        else:
            new_tokens.append(token)

    return new_tokens


def parse(tokens):
    assert type(tokens) == list
    assert len(tokens) > 0

    if len(tokens) == 1:
        token = tokens[0]
        if token in BRACES:
            raise RuntimeError(
                f"Scheme Requires At Least 1 Open and Close Parentheses: {token} was provided")
        if type(token) == int:
            return token
        elif type(token) == str:
            return token
        elif type(token) == bool:
            return token
        elif type(token) == String:
            return token
        elif type(token) == list:
            # preparsed already from recursion
            return token
        else:
            raise RuntimeError(f"Scheme does not recognize token {token}.")

    # is a list form
    if len(tokens) < 2:
        raise RuntimeError(f"Scheme Requires At Least 2 Tokens: {tokens}")
    if tokens[0] != OPEN_PAREN:
        raise RuntimeError(
            f"Scheme Requires Expression Begin with Open Parentheses: {tokens}")
    if tokens[-1] != CLOSE_PAREN:
        raise RuntimeError(
            f"Scheme Requires Expression End with Close Parentheses: {tokens}")

    inner_tokens = tokens[1:-1]
    assert len(inner_tokens) >= 2

    exprs = []
    stack = [[]]
    num_open_parens = 0
    for token in inner_tokens:
        if num_open_parens < 0:
            raise RuntimeError(
                f"Too Many Closing Parentheses: Scheme Requires Open \
                    Parentheses Paired With Closing Parentheses: {tokens}")
        if token == OPEN_PAREN:
            num_open_parens += 1
            stack.append([])
            stack[-1].append(token)
        elif token == CLOSE_PAREN:
            num_open_parens -= 1
            stack[-1].append(token)
            top = stack.pop()
            top_expr = parse(top)
            stack[-1].append(top_expr)
        else:
            if num_open_parens == 0:
                stack[-1].append(parse([token]))
            else:
                stack[-1].append(token)
    else:
        if num_open_parens != 0:
            raise RuntimeError(
                f"Missing Closing Parentheses: Scheme Requires Open \
                    Parentheses Paired With Closing Parentheses: {tokens}")

    return stack.pop()


def frontend(string):
    return parse(lex(string))


if __name__ == "__main__":
    string = r'(+ 1 (+ 3 4) (- 1 2))'
    string = r'1'
    string = r'#t'
    string = r'(/ (+ 2 (* 2 3) (- 0 1) (+ 1 3 4)) (+ 2 3))'
    # string = r'(+ 1 2 3)'
    # string = r'(- 0 1)'
    # string = r'(* 3 4 5)'
    # string = r'(/ 3 4)'
    print(expr_to_str(frontend(string)))
    context = {}
    print(expr_to_str(eval_expr(frontend(string), context)))
