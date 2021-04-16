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

from functools import reduce

PRINT_CONS = False


OPEN_PAREN = "("
CLOSE_PAREN = ")"
OPEN_BRACKET = "["
CLOSE_BRACKET = "]"
BRACES = [
    OPEN_PAREN,
    CLOSE_PAREN,
]
QUOTATION_MARK = '\"'
TICK = "'"
BACKTICK = "`"
AT = "@"
COMMA = ","

INFIX_MARKER = "$"

DOT = "."

COMMENT = ";"
NEWLINE = "\n"
CARRIAGE_RETURN = "\r\n"
NEWLINE_CHARS = "\r\n"

SPACE = " "
TRUE = "#t"
FALSE = "#f"
ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"
EXP = "**"
CONCAT = "^"
PRINTLN = "println"
SET = "set!"
EQ = "eq?"
QUOTE = "quote"
UNQUOTE = "unquote"
QUASIQUOTE = "quasiquote"
UNQUOTE_SPLICING = "unquote-splicing"
LIST = "list"
IF = "if"
LET = "let"
LETSTAR = "let*"
AND = "and"
OR = "or"
NOT = "not"
BEGIN = "begin"
CONS = "cons"
CAR = "car"
CDR = "cdr"
DEFINE = "define"
LAMBDA = "lambda"
FOR = "for"
FORLIST = "for/list"
DEFINE_MACRO = "define-macro"
APPLY = "apply"
MAP = "map"
LT = "lt?"
GT = "gt?"
LTE = "lte?"
GTE = "gte?"
NEQ = "neq?"
COND = "cond"
ELSE = "else"
DELAY = "delay"
FORCE = "force"
CONS_STREAM = "cons-stream"
CDR_STREAM = "cdr-stream"
VARIADIC = "variadic"
APPEND = "append"
NIL = "nil"
MATCH = "match"  # very basic match
UNDERSCORE = "_"

PREPARSE_SYMBOLS_MAP = {
    TICK: QUOTE,
    BACKTICK: QUASIQUOTE,
    AT: UNQUOTE_SPLICING,
    COMMA: UNQUOTE
}


COUNTER = 0
GENERATED_SYMBOL = "gen_sym"


def gensym():
    global COUNTER
    COUNTER += 1
    return f"__{GENERATED_SYMBOL}_{COUNTER}__"


class String():
    def __init__(self, s):
        super().__init__()
        self.string = s

    def __add__(self, s):
        return String(self.string + s.string)

    def get_string(self):
        return self.string


class Lambda():
    def __init__(self, args, bodies, is_variadic):
        assert type(args) == list
        assert len(args) >= 1
        assert type(bodies) == list
        assert len(bodies) >= 1
        assert type(is_variadic) == bool
        super().__init__()
        self.args = args
        self.bodies = bodies
        self.is_variadic = is_variadic

    def get_args(self):
        return self.args

    def get_bodies(self):
        return self.bodies

    def get_is_variadic(self):
        return self.is_variadic


class Delay():
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def get_expr(self):
        return self.expr


class Cons():
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


class Macro():
    def __init__(self, args, bodies):
        assert type(args) == list
        assert len(args) >= 1
        assert type(bodies) == list
        assert len(bodies) >= 1
        super().__init__()
        self.args = args
        self.bodies = bodies

    def replicate(self):
        # need to process to generate random symbols
        args = deepcopy(self.args)
        bodies = deepcopy(self.bodies)
        sym_map = {}
        for arg in args:
            sym_map[arg] = gensym()
        self.args = [sym_map[arg] for arg in args]
        new_bodies = []
        for body in bodies:
            new_body = []
            for sym in body:
                if sym in sym_map:
                    new_body.append(sym_map[sym])
                else:
                    new_body.append(sym)
            new_bodies.append(new_body)
        self.bodies = new_bodies

    def get_args(self):
        return self.args

    def get_bodies(self):
        return self.bodies


def bool_to_str(b):
    assert type(b) == bool
    if b:
        return TRUE
    return FALSE


def lambda_to_str(expr):
    assert type(expr) == Lambda
    bodies = expr.get_bodies()
    args = expr.get_args()
    args_str = " ".join(args)
    bodies_strs = list(map(lambda b: expr_to_str(b), bodies))
    bodies_combined = " ".join(bodies_strs)
    return f'(lambda ({args_str}) {bodies_combined})'


def expr_to_str(expr):
    if type(expr) == int:
        return str(expr)
    elif type(expr) == bool:
        return bool_to_str(expr)
    elif type(expr) == str:
        return expr
    elif type(expr) == String:
        return f'"{expr.get_string()}"'
    elif type(expr) == Lambda:
        return lambda_to_str(expr)
    elif type(expr) == Cons:
        if PRINT_CONS:
            return f'(cons {expr_to_str(expr.get_left())} {expr_to_str(expr.get_right())})'
        else:
            return f'({expr_to_str(expr.get_left())} . {expr_to_str(expr.get_right())})'
    elif type(expr) == Delay:
        return f'#[promise (unforced)]'
    elif type(expr) == Macro:
        raise RuntimeError(
            f"Macro can never be an evaluated expression: {expr}")

    assert type(expr) == list
    if len(expr) == 0:
        return NIL

    # special forms:
    head = expr[0]
    if head == QUOTE:
        assert len(expr) == 2
        return f"{TICK}{expr_to_str(expr[1])}"
    elif head == QUASIQUOTE:
        assert len(expr) == 2
        return f"{BACKTICK}{expr_to_str(expr[1])}"
    elif head == UNQUOTE:
        assert len(expr) == 2
        return f"{COMMA}{expr_to_str(expr[1])}"
    elif head == UNQUOTE_SPLICING:
        assert len(expr) == 2
        return f"{AT}{expr_to_str(expr[1])}"

    output_lst = []
    for e in expr:
        output_lst.append(expr_to_str(e))
    output = f"({' '.join(output_lst)})"
    return output


def eval_expr(expr, ctx, in_quasi):
    if type(expr) == int:
        return expr
    elif type(expr) == bool:
        return expr
    elif expr == NIL:
        return []
    elif type(expr) == str:
        if expr in ctx:
            return ctx[expr]
        # this is a symbol under quasi
        elif in_quasi:
            return expr
    elif type(expr) == String:
        return expr

    assert type(expr) == list
    assert len(expr) >= 2

    first = expr[0]
    # Named Arithmetic Operators
    if first == ADD:
        return eval_add(expr, ctx, in_quasi)
    elif first == SUB:
        return eval_sub(expr, ctx, in_quasi)
    elif first == MUL:
        return eval_mul(expr, ctx, in_quasi)
    elif first == DIV:
        return eval_div(expr, ctx, in_quasi)
    elif first == EXP:
        return eval_exp(expr, ctx, in_quasi)
    elif first == CONCAT:
        return eval_concat(expr, ctx, in_quasi)
    # Named Special Forms
    elif first == QUOTE:
        return eval_quote(expr, ctx, in_quasi)
    elif first == PRINTLN:
        return eval_println(expr, ctx, in_quasi)
    elif first == SET:
        return eval_set(expr, ctx, in_quasi)
    elif first == EQ:
        return eval_eq(expr, ctx, in_quasi)
    elif first == QUASIQUOTE:
        return eval_quasiquote(expr, ctx, in_quasi)
    elif first == UNQUOTE:
        return eval_unquote(expr, ctx, in_quasi)
    elif first == LIST:
        return eval_list(expr, ctx, in_quasi)
    elif first == UNQUOTE_SPLICING:
        return eval_unquotesplicing(expr, ctx, in_quasi)
    elif first == IF:
        return eval_if(expr, ctx, in_quasi)
    elif first == LET:
        return eval_let(expr, ctx, in_quasi, False)
    elif first == LETSTAR:
        return eval_let(expr, ctx, in_quasi, True)
    elif first == AND:
        return eval_and(expr, ctx, in_quasi)
    elif first == OR:
        return eval_or(expr, ctx, in_quasi)
    elif first == NEQ:
        return eval_neq(expr, ctx, in_quasi)
    elif first == LT:
        return eval_lt(expr, ctx, in_quasi)
    elif first == LTE:
        return eval_lte(expr, ctx, in_quasi)
    elif first == GT:
        return eval_gt(expr, ctx, in_quasi)
    elif first == GTE:
        return eval_gte(expr, ctx, in_quasi)
    elif first == NOT:
        return eval_not(expr, ctx, in_quasi)
    elif first == BEGIN:
        return eval_begin(expr, ctx, in_quasi)
    elif first == DEFINE:
        return eval_define(expr, ctx, in_quasi)
    elif first == LAMBDA:
        return eval_lambda(expr, ctx, in_quasi)
    elif first == CAR:
        return eval_car(expr, ctx, in_quasi)
    elif first == CDR:
        return eval_cdr(expr, ctx, in_quasi)
    elif first == CONS:
        return eval_cons(expr, ctx, in_quasi)
    elif first == APPLY:
        return eval_apply(expr, ctx, in_quasi)
    elif first == MAP:
        return eval_map(expr, ctx, in_quasi)
    elif first == DEFINE_MACRO:
        return eval_define_macro(expr, ctx, in_quasi)
    elif first == COND:
        return eval_cond(expr, ctx, in_quasi)
    elif first == FOR:
        return eval_for(expr, ctx, in_quasi, False)
    elif first == FORLIST:
        return eval_for(expr, ctx, in_quasi, True)
    elif first == DELAY:
        return eval_delay(expr, ctx, in_quasi)
    elif first == FORCE:
        return eval_force(expr, ctx, in_quasi)
    elif first == CONS_STREAM:
        return eval_consstream(expr, ctx, in_quasi)
    elif first == CDR_STREAM:
        return eval_cdrstream(expr, ctx, in_quasi)
    elif first == APPEND:
        return eval_append(expr, ctx, in_quasi)
    elif first == MATCH:
        return eval_match(expr, ctx, in_quasi)
    # match on a macro
    elif type(first) != list and first in ctx and type(ctx[first]) == Macro:
        return eval_macro(expr, ctx, in_quasi)
    # return forms that are quasiquoted, comes before application
    elif in_quasi:
        return eval_in_quasi_return(expr, ctx, in_quasi)
    # forms that are applications
    elif len(expr) >= 2:
        return eval_app(expr, ctx, in_quasi)
    else:
        raise RuntimeError(f"Expression could not be matched: {expr}.")


def eval_in_quasi_return(expr, ctx, in_quasi):
    lst = []
    for e in expr:
        v = eval_expr(e, ctx, in_quasi)
        if type(v) == tuple:
            assert len(v) == 2 and v[1] == True
            vals, _ = v
            for value in vals:
                lst.append(value)
        else:
            lst.append(v)
    return lst


def eval_add(expr, ctx, in_quasi):
    assert len(expr) >= 3
    assert expr[0] == ADD
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    vals = []
    for sub_expr in expr[1:]:
        val = eval_expr(sub_expr, ctx, in_quasi)
        vals.append(val)
    return reduce(lambda val, acc: val + acc, vals, 0)


def eval_sub(expr, ctx, in_quasi):
    assert len(expr) >= 3
    assert expr[0] == SUB
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    vals = []
    first = expr[1]
    first_val = eval_expr(first, ctx, in_quasi)
    for sub_expr in expr[2:]:
        val = eval_expr(sub_expr, ctx, in_quasi)
        vals.append(val)
    vals = [first_val] + list(map(lambda v: -v, vals))
    return reduce(lambda val, acc: val + acc, vals, 0)


def eval_mul(expr, ctx, in_quasi):
    assert len(expr) >= 3
    assert expr[0] == MUL
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    vals = []
    for sub_expr in expr[1:]:
        val = eval_expr(sub_expr, ctx, in_quasi)
        vals.append(val)
    return reduce(lambda val, acc: val * acc, vals, 1)


def eval_div(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == DIV
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return int(first/second)


def eval_exp(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == EXP
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return first ** second


def eval_concat(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == CONCAT
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    assert type(first) == String
    second = eval_expr(expr[2], ctx, in_quasi)
    assert type(second) == String
    return first + second


def eval_lt(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == LT
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return first < second


def eval_gt(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == GT
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return first > second


def eval_lte(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == LTE
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return first <= second


def eval_gte(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == GTE
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return first >= second


def eval_neq(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 3
    assert expr[0] == NEQ
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    first = eval_expr(expr[1], ctx, in_quasi)
    second = eval_expr(expr[2], ctx, in_quasi)
    return first != second


def eval_quote(expr, ctx, in_quasi):
    # does not matter if it is in quasi or not
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == QUOTE
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    # no eval
    return expr[1]


def eval_println(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    assert expr[0] == PRINTLN
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    # make println variadic in nature
    vals = list(map(lambda e: eval_expr(e, ctx, in_quasi), expr[1:]))
    strings = list(map(lambda v: expr_to_str(v), vals))
    print(" ".join(strings))
    # return an int
    return 0


def eval_set(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == SET
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    var = expr[1]
    # var must be a python string
    assert type(var) == str
    val = eval_expr(expr[2], ctx, in_quasi)
    # mutate context
    ctx[var] = val
    return 0


def eval_eq(expr, ctx, in_quasi):
    assert len(expr) == 3
    assert expr[0] == EQ
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    fst = eval_expr(expr[1], ctx, in_quasi)
    snd = eval_expr(expr[2], ctx, in_quasi)
    return fst == snd


def eval_unquote(expr, ctx, in_quasi):
    assert len(expr) == 2
    assert expr[0] == UNQUOTE
    if in_quasi:
        return eval_expr(expr[1], ctx, False)
    raise RuntimeError(f"Unquote not located within quasiquote: {expr}.")


def eval_quasiquote(expr, ctx, in_quasi):
    assert len(expr) == 2
    assert expr[0] == QUASIQUOTE
    if in_quasi:
        # if quasiquote nested within quasiquote, just return expr
        return expr
    return eval_expr(expr[1], ctx, True)


def eval_unquotesplicing(expr, ctx, in_quasi):
    assert len(expr) == 2
    assert expr[0] == UNQUOTE_SPLICING
    if in_quasi:
        try:
            return eval_list(expr[1], ctx, False), True
        except:
            raise RuntimeError(
                f"Inner Form in Unquote-Splicing must be a list form: {expr}.")
    raise RuntimeError(
        f"Unquote-Splicing must be located within quasiquote: {expr}.")


def eval_list(expr, ctx, in_quasi):
    assert len(expr) >= 2
    assert expr[0] == LIST
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    lst = []
    for sub_expr in expr[1:]:
        lst.append(eval_expr(sub_expr, ctx, in_quasi))
    return lst


def eval_if(expr, ctx, in_quasi):
    assert len(expr) >= 4
    assert expr[0] == IF
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    b = eval_expr(expr[1], ctx, in_quasi)
    # require to be explicitly true
    if b == True:
        return eval_expr(expr[2], ctx, in_quasi)
    return eval_expr(expr[3], ctx, in_quasi)


def eval_let(expr, ctx, in_quasi, update_let):
    # if update_let = True, then acts like let*
    assert len(expr) >= 3
    assert (expr[0] == LET and not update_let) or (
        expr[0] == LETSTAR and update_let)
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    bindings = expr[1]
    for binding in bindings:
        assert type(binding) == list
        assert len(binding) == 2
        (name, e) = binding
        if update_let:
            ctx[name] = eval_expr(e, ctx, in_quasi)
        else:
            if name not in ctx:
                ctx[name] = eval_expr(e, ctx, in_quasi)
    bodies = expr[2:]
    v = None
    for body in bodies:
        v = eval_expr(body, ctx, in_quasi)
    return v


def eval_and(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    assert expr[0] == AND
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    values = []
    for e in expr[1:]:
        b = eval_expr(e, ctx, in_quasi)
        assert type(b) == bool
        values.append(b)
    return reduce(lambda v, acc: v and acc, values, True)


def eval_or(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    assert expr[0] == OR
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    values = []
    for e in expr[1:]:
        b = eval_expr(e, ctx, in_quasi)
        assert type(b) == bool
        values.append(b)
    return reduce(lambda v, acc: v or acc, values, False)


def eval_not(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == NOT
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    b = eval_expr(expr[1], ctx, in_quasi)
    assert type(b) == bool
    return not b


def eval_begin(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    assert expr[0] == BEGIN
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    v = None
    for e in expr[1:]:
        v = eval_expr(e, ctx, in_quasi)
    return v


def eval_define(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == DEFINE
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    names = expr[1]
    if type(names) == list and len(names) > 1:
        # is a functional define
        assert len(names) >= 2
        function_name = names[0]
        args = names[1:]
        is_variadic = False
        final_args = []
        for i, arg in enumerate(args):
            if i != len(args) - 1:
                assert type(arg) == str
                final_args.append(arg)
            else:
                # last argument can be called Variadic
                if type(arg) == list:
                    assert len(arg) == 2
                    fst, snd = arg
                    assert fst == VARIADIC
                    assert type(snd) == str
                    is_variadic = True
                    final_args.append(snd)
                else:
                    assert type(arg) == str
                    final_args.append(arg)
        bodies = expr[2:]
        ctx[function_name] = Lambda(final_args, bodies, is_variadic)
        return function_name
    else:
        # variable define
        assert type(names) == str
        e = expr[2]
        assert expr[3:] == []
        ctx[names] = eval_expr(expr[2], ctx, in_quasi)
        return names


def eval_lambda(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == LAMBDA
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    params = expr[1]
    final_params = []
    is_variadic = False
    for i, param in enumerate(params):
        if i != len(params) - 1:
            assert type(param) == str
            final_params.append(param)
        else:
            # last argument can be called Variadic
            if type(param) == list:
                assert len(param) == 2
                fst, snd = param
                assert fst == VARIADIC
                assert type(snd) == str
                is_variadic = True
                final_params.append(snd)
            else:
                assert type(param) == str
                final_params.append(param)
    bodies = expr[2:]
    return Lambda(final_params, bodies, is_variadic)


def eval_app(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    _lambda = eval_expr(expr[0], ctx, in_quasi)
    assert type(_lambda) == Lambda
    args = list(map(lambda a: eval_expr(a, ctx, in_quasi), expr[1:]))
    param_names = _lambda.get_args()
    is_variadic = _lambda.get_is_variadic()
    if (not is_variadic and len(param_names) != len(args)) or len(param_names) > len(args):
        raise RuntimeError(
            f"Arities Mismatch in application: expected: {len(param_names)}, got {len(args)} instead.")
    bodies = _lambda.get_bodies()
    bodies_w_begin = [BEGIN] + bodies
    if (not is_variadic):
        for (param, arg) in zip(param_names, args):
            assert type(param) == str
            ctx[param] = arg
        return eval_expr(bodies_w_begin, ctx, in_quasi)
    common_length = len(param_names)
    for (param, arg) in zip(param_names[:common_length - 1], args[:common_length - 1]):
        assert type(param) == str
        ctx[param] = arg
    # variadic part
    ctx[param_names[common_length - 1]
        ] = eval_expr([LIST] + args[common_length - 1:], ctx, in_quasi)
    return eval_expr(bodies_w_begin, ctx, in_quasi)


def eval_cons(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 3
    assert expr[0] == CONS
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    left = eval_expr(expr[1], ctx, in_quasi)
    right = eval_expr(expr[2], ctx, in_quasi)
    return Cons(left, right)


def eval_car(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == CAR
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    c = eval_expr(expr[1], ctx, in_quasi)
    assert type(c) == Cons
    return c.get_left()


def eval_cdr(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == CDR
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    c = eval_expr(expr[1], ctx, in_quasi)
    assert type(c) == Cons
    return c.get_right()


def eval_apply(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == APPLY
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    function = expr[1]
    lst = []
    for a in expr[2:-1]:
        lst.append(a)
    # last arg must be a list
    lst += eval_expr(expr[-1], ctx, in_quasi)
    new_expr = [function] + lst
    return eval_expr(new_expr, ctx, in_quasi)


def eval_map(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == MAP
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    function = expr[1]
    lists = []
    for lst in expr[2:]:
        val = eval_expr(lst, ctx, in_quasi)
        assert type(val) == list
        lists.append(val)
    # last arg must be a list
    assert len(lists) > 0
    l = len(lists[0])
    for lst in lists:
        assert len(lst) == l
    tupled_lists = list(zip(*lists))
    to_eval_lists = []
    for tup in tupled_lists:
        to_eval_lists.append([function] + list(tup))
    final_list = list(map(lambda lst: eval_expr(
        lst, ctx, in_quasi), to_eval_lists))
    return final_list


def eval_define_macro(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == DEFINE_MACRO
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    binding = expr[1]
    bodies = expr[2:]
    assert len(binding) >= 2
    name = binding[0]
    params = binding[1:]
    macro = Macro(params, bodies)
    ctx[name] = macro
    return name


def eval_delay(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == DELAY
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    return Delay(expr[1])


def eval_consstream(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 3
    assert expr[0] == CONS_STREAM
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    new_expr = [CONS, expr[1], [DELAY, expr[2]]]
    return eval_expr(new_expr, ctx, in_quasi)


def eval_cdrstream(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == CDR_STREAM
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    new_expr = [FORCE, [CDR, expr[1]]]
    return eval_expr(new_expr, ctx, in_quasi)


def eval_force(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) == 2
    assert expr[0] == FORCE
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    delay_expr = eval_expr(expr[1], ctx, in_quasi)
    assert type(delay_expr) == Delay
    return eval_expr(delay_expr.get_expr(), ctx, in_quasi)


def eval_macro(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    assert expr[0] in ctx and type(ctx[expr[0]]) == Macro
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    # at each use, we need to replicate the macro to get new fresh symbols
    macro_name = expr[0]
    macro = ctx[macro_name]
    macro.replicate()
    ctx[macro_name] = macro
    # finished replication of macro
    new_expr = deepcopy(expr)
    macro = ctx[macro_name]
    macro_expr = [LAMBDA, macro.get_args(), [BEGIN] + macro.get_bodies()]
    new_expr = [macro_expr, *new_expr[1:]]
    return eval_expr(new_expr, ctx, in_quasi)


def eval_cond(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 2
    assert expr[0] == COND
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    clauses = expr[1:]
    for i, clause in enumerate(clauses):
        assert type(clause) == list
        assert len(clause) == 2
        test, e = clause
        if test == ELSE and i != len(clauses) - 1:
            raise RuntimeError(f"Else must be last condition in cond: {expr}.")
        if test == ELSE:
            return eval_expr(e, ctx, in_quasi)
        b = eval_expr(test, ctx, in_quasi)
        assert type(b) == bool
        # if true on condition, evaluate other side
        if b:
            return eval_expr(e, ctx, in_quasi)
    # undefined return on no matching conditions
    return 0


def eval_for(expr, ctx, in_quasi, is_forlist):
    assert type(expr) == list
    assert len(expr) >= 3
    assert (expr[0] == FOR and not is_forlist) or (
        expr[0] == FORLIST and is_forlist)
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    bindings = expr[1]
    bodies = expr[2:]
    new_bodies = [BEGIN] + bodies
    variables = []
    lists = []
    for binding in bindings:
        assert type(binding) == list
        assert len(binding) == 2
        var, lst = binding
        assert type(var) == str
        variables.append(var)
        value_lst = eval_expr(lst, ctx, in_quasi)
        lists.append(value_lst)
    final_list = []
    for values in zip(*lists):
        val_list = list(values)
        for var, val in zip(variables, values):
            ctx[var] = val
        final_val = eval_expr(new_bodies, ctx, in_quasi)
        final_list.append(final_val)
    if is_forlist:
        return final_list
    # for does not return list
    return 0


def eval_append(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == APPEND
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    lists = expr[1:]
    evaluated_lists = []
    for lst in lists:
        evaluated_lists.append(eval_expr(lst, ctx, in_quasi))
    final_lst = []
    for lst in evaluated_lists:
        assert type(lst) == list
        for v in lst:
            final_lst.append(v)
    return final_lst


def match_pattern(value, pattern, ctx, in_quasi, add_bindings):
    """
    returns True when pattern matches else False,
    When add_bindings is true, does side effects like updating context when 
    pattern matches but does not evaluate body. Otherwise, when add_bindings
    is false, no side effects on context.
    Never has side effects on in_quasi

    Recursive descends through pattern and value to create strongest matching.
    """
    if type(pattern) != list:
        if pattern == UNDERSCORE:
            # match all, no bindings updated
            return True
        if pattern == NIL:
            return value == []
        # pattern is a string --> understood to be a variable
        if type(pattern) == str:
            # update binding
            if add_bindings:
                ctx[pattern] = value
            return True
        # pattern must be a literal
        return pattern == value

    assert type(pattern) == list
    assert len(pattern) >= 2

    head = pattern[0]
    if head == QUOTE:
        assert len(pattern) == 2
        datum = pattern[0]
        return datum == value
    elif head == LIST:
        assert len(pattern) >= 2
        binders = pattern[1:]
        if type(value) == list:
            if len(value) != len(binders):
                return False
            for var, val in zip(binders, value):
                result = match_pattern(val, var, ctx, in_quasi, add_bindings)
                if not result:
                    return False
            return True
        return False
    elif head == CONS:
        assert len(pattern) >= 3
        left = pattern[1]
        right = pattern[2]
        if type(value) == Cons:
            lval = value.get_left()
            lresult = match_pattern(lval, left, ctx, in_quasi, add_bindings)
            if not lresult:
                return False

            rval = value.get_right()
            rresult = match_pattern(rval, right, ctx, in_quasi, add_bindings)
            if not rresult:
                return False

            return True
        return False


def eval_match(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) >= 3
    assert expr[0] == MATCH
    if in_quasi:
        return handle_quasi(expr, ctx, in_quasi)
    val_expr = expr[1]
    clauses = expr[2:]
    val = eval_expr(val_expr, ctx, in_quasi)
    # can add more patterns as one desires
    for clause in clauses:
        assert type(clause) == list
        assert len(clause) >= 2
        pattern = clause[0]
        bodies = clause[1:]
        final_bodies = [BEGIN] + bodies
        # no side effect match
        match = match_pattern(val, pattern, ctx, in_quasi, False)
        if match:
            # binding and have side effects for context
            match_pattern(val, pattern, ctx, in_quasi, True)
            return eval_expr(final_bodies, ctx, in_quasi)
    # no match , return any value, say 0
    return 0


def handle_quasi(expr, ctx, in_quasi):
    assert type(expr) == list
    assert len(expr) > 1
    remainder = []
    for e in expr:
        v = eval_expr(e, ctx, in_quasi)
        if type(v) == tuple:
            assert len(v) == 2
            (lst, _) = v
            assert type(lst) == list
            for elt in lst:
                remainder.append(elt)
        else:
            remainder.append(v)
    return remainder


def remove_comments(string):
    """
    takes a raw string, and any line with a comment
    has the comment removed to the end of the line
    """
    new_string = ""
    in_comment = False
    for c in string:
        if c == COMMENT and not in_comment:
            in_comment = True
        elif c in NEWLINE_CHARS and in_comment:
            in_comment = False
        elif in_comment:
            continue
        else:
            new_string += c
    return new_string


def split_tokens(string):
    """
    Does not supported nested string data

    Tokenizes string
    """
    tokens = []
    in_string = False
    current_string = ''
    current_chunk = ''
    for c in string:
        if c == QUOTATION_MARK and not in_string:
            in_string = True
            current_string += c
            # clear current chunk
            current_chunk_tokens = current_chunk.split()
            tokens += current_chunk_tokens
            current_chunk = ''
        elif c == QUOTATION_MARK and in_string:
            in_string = False
            current_string += c
            # clear current string
            tokens.append(current_string)
            current_string = ''
        elif in_string:
            current_string += c
        else:
            current_chunk += c
    # finish by clearing current chunk
    if current_chunk != '':
        current_chunk_tokens = current_chunk.split()
        tokens += current_chunk_tokens
        current_chunk = ''

    # if string not completed at end, illegal program
    if current_string != '':
        raise RuntimeError(f"String Not Terminated: {string}.")

    return tokens


def check_brackets_matching(string):
    """
    checks if all brackets are matching
    """
    stack = []
    for c in string:
        if c == OPEN_PAREN:
            stack.append(c)
        elif c == CLOSE_PAREN:
            if len(stack) > 0 and stack[-1] == OPEN_PAREN:
                stack.pop()
            else:
                return False
        elif c == OPEN_BRACKET:
            stack.append(c)
        elif c == CLOSE_BRACKET:
            if len(stack) > 0 and stack[-1] == OPEN_BRACKET:
                stack.pop()
            else:
                return False
        else:
            continue
    if stack != []:
        return False
    return True


def lex(string):
    if not check_brackets_matching(string):
        raise RuntimeError(f"Unmatched brackets/braces in program: {string}.")
    no_comments_str = remove_comments(string)
    no_open_brackets = no_comments_str.replace(OPEN_BRACKET, OPEN_PAREN)
    no_close_brackets = no_open_brackets.replace(CLOSE_BRACKET, CLOSE_PAREN)
    str1 = no_close_brackets.replace(OPEN_PAREN, f"{OPEN_PAREN}{SPACE}")
    str2 = str1.replace(CLOSE_PAREN, f"{SPACE}{CLOSE_PAREN}")
    str3 = str2.replace(COMMA, f"{SPACE}{COMMA}{SPACE}")
    str4 = str3.replace(AT, f"{SPACE}{AT}{SPACE}")
    str5 = str4.replace(TICK, f"{SPACE}{TICK}{SPACE}")
    str6 = str5.replace(BACKTICK, f"{SPACE}{BACKTICK}{SPACE}")
    tokens = split_tokens(str6)
    new_tokens = []
    for token in tokens:
        if token == TRUE:
            new_tokens.append(True)
        elif token == FALSE:
            new_tokens.append(False)
        elif token.isdigit():
            new_tokens.append(int(token))
        elif token[0] == QUOTATION_MARK and token[-1] == QUOTATION_MARK:
            new_tokens.append(String(token[1:-1]))
        else:
            new_tokens.append(token)

    return new_tokens


def preparse(tokens):
    """
    preparse adds in parsing for tick, backtick, add, comma
    """
    assert type(tokens) == list
    assert len(tokens) > 0

    l = len(tokens)
    i = 0
    while i < l:

        stack = []
        token = tokens[i]
        if token in PREPARSE_SYMBOLS_MAP:
            replacement_symbol = PREPARSE_SYMBOLS_MAP[token]
            next_idx = i + 1
            if next_idx >= l:
                raise RuntimeError(f"No More Tokens: Ended on Tick {tokens}.")
            while tokens[next_idx] in PREPARSE_SYMBOLS_MAP:
                next_idx += 1
                if next_idx >= l:
                    raise RuntimeError(
                        f"No More Tokens: Ended on Tick {tokens}.")
            _next = tokens[next_idx]

            if _next == OPEN_PAREN:
                remainder = tokens[next_idx:]
                stop_idx = None
                for idx, tok in enumerate(remainder, next_idx):
                    if tok == OPEN_PAREN:
                        stack.append(tok)
                    elif tok == CLOSE_PAREN:
                        if stack == []:
                            raise RuntimeError(
                                f"Too Many Closing Parentheses: {tokens}.")
                        stack.pop()
                        if stack == []:
                            stop_idx = idx
                            break

                tokens = tokens[0:i] + \
                    [OPEN_PAREN, replacement_symbol] + \
                    tokens[i + 1:next_idx] + \
                    tokens[next_idx:stop_idx + 1] + \
                    [CLOSE_PAREN] + tokens[stop_idx+1:]
            else:
                tokens = tokens[0:i] + \
                    [OPEN_PAREN, replacement_symbol] + \
                    tokens[i + 1:next_idx] + \
                    [tokens[next_idx], CLOSE_PAREN] + \
                    tokens[next_idx + 1:]

        i += 1
        l = len(tokens)

    return tokens


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
    # empty list form
    if len(tokens) == 2:
        if tokens == [OPEN_PAREN, CLOSE_PAREN]:
            return NIL
    if len(tokens) < 2:
        raise RuntimeError(
            f"Scheme Requires At Least 2 Tokens if not Empty List: {tokens}")
    if tokens[0] != OPEN_PAREN:
        raise RuntimeError(
            f"Scheme Requires Expression Begin with Open Parentheses: {tokens}")
    if tokens[-1] != CLOSE_PAREN:
        raise RuntimeError(
            f"Scheme Requires Expression End with Close Parentheses: {tokens}")

    inner_tokens = tokens[1:-1]
    assert len(inner_tokens) >= 1

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


def create_cons(collector):
    if DOT not in collector:
        return collector
    assert len(collector) >= 1
    if len(collector) == 1:
        assert collector[0] != DOT
        return collector[0]
    # create cons with left to right precedence
    assert collector[1] == DOT
    item = create_cons(collector[2:])
    if len(item) == 1:
        item = item[0]
    assert collector[0] != DOT
    if type(item) == list:
        assert len(item) >= 3
        assert item[-1] != DOT
    else:
        assert item != DOT
    return [CONS, collector[0], item]


def dot_reader(parsed):
    if type(parsed) != list:
        return parsed
    # is list
    assert type(parsed) == list
    # recursively dot read
    new_parsed = deepcopy(parsed)
    for i, elt in enumerate(parsed):
        new_parsed = new_parsed[:i] + [dot_reader(elt)] + new_parsed[i + 1:]
    # finish by combining dots
    final_parsed = []
    collector = []
    for elt in new_parsed:
        # elt is not a dot cases
        if elt != DOT and collector == []:
            collector.append(elt)
        elif elt != DOT and collector[-1] == DOT:
            collector.append(elt)
        elif elt != DOT and collector[-1] != DOT:
            final_parsed += create_cons(collector)
            collector = []
            collector.append(elt)
        # elt is a dot case
        elif elt == DOT and collector == []:
            raise RuntimeError(
                f"Dot cannot be beginning of expression: {parsed}.")
        elif elt == DOT and collector[-1] == DOT:
            raise RuntimeError(
                f"Dot cannot follow dot in expression: {parsed}.")
        elif elt == DOT and collector[-1] != DOT:
            collector.append(elt)
        else:
            raise RuntimeError(
                f"Impossible Failure to match in Dot parsing: {parsed}. ")
    else:
        # if collector ends in DOT: this is an error:
        if collector != [] and collector[-1] == DOT:
            raise RuntimeError(f"Cannot End Expression with Dot: {parsed}.")
        # clear out collector when for loop finishes
        final_parsed += create_cons(collector)
        collector = []

    return final_parsed


def reorder_infix(parsed):
    if type(parsed) != list:
        return parsed
    # is list
    assert type(parsed) == list
    l = len(parsed)
    # only odd will have reordering of infix, if even, return now
    if l % 2 == 0:
        return parsed
    # recursively apply infix reordering
    new_parsed = []
    for elt in parsed:
        new_parsed.append(reorder_infix(elt))
    # gather operators
    operators = set()
    for i, elt in enumerate(new_parsed):
        if i % 2 == 1:
            if type(elt) == str and len(elt) >= 2 and INFIX_MARKER == elt[0] and INFIX_MARKER == elt[-1]:
                operators.add(elt[1:-1])
    # continue if only one infix operator
    if len(operators) == 0:
        return new_parsed
    if len(operators) > 1:
        raise RuntimeError(
            f"Only 1 Infix Operator can be used in an expression: {parsed}.")
    op = list(operators)[0]
    final_parsed = []
    for i, elt in enumerate(new_parsed):
        if i % 2 == 1:
            if type(elt) == str and len(elt) >= 2 and elt[1:-1] == op:
                continue
            else:
                raise RuntimeError(
                    f"Expected Infix Operator In Odd Position: {parsed}.")
        else:
            final_parsed.append(elt)
    # add on infix operator at end
    final_parsed = [op] + final_parsed
    return final_parsed


def postparse(parsed):
    """
    postparse expands out correctly any specified infix operators
    and also expands out infix dot notation for pairs, which significantly
    differs from the actual scheme implementation because I disagree
    with the fact that dot notation can generally not be read in to the 
    scheme reader.
    """
    parsed = dot_reader(parsed)
    parsed = reorder_infix(parsed)
    return parsed


def frontend(string):
    return postparse(parse(preparse(lex(string))))


if __name__ == "__main__":
    tests = [r'(+ 1 (+ 3 4) (- 1 2))',
             r'1',
             r'#t',
             r'(/ (+ 2 (* 2 3) (- 0 1) (+ 1 3 4)) (+ 2 3))',
             r'(+ 1 2 3)',
             r'(- 0 1)',
             r'(* 3 4 5)',
             r'(/ 3 4)',
             r'(** 2 3)',
             r'(println (quote (1 2 4)))',
             r'(eq? 1 2)',
             r'(list 1 (+ 1 2) 3)',
             r'(quasiquote (list 3 (unquote (+ 2 3))))',
             r'(quasiquote (quasiquote (unquote (+ 2 3))))',
             r'"Hello"',
             r'(quasiquote (3 (unquote-splicing (list 3 4)) 5))',
             r'(if #t (+ 2 3) (- 0 1))',
             r'(let ((x 3) (x 4)) (+ x 2))',
             r'(let* ((x 3) (x 4)) (+ x 2))',
             r'(and #t #t #f #f #t)',
             r'(or #t #t #f #f #t)',
             r'(not #f)',
             r'(not #t)',
             r'(begin 2 (+ 2 3) (if #f (- 2 3) (+ 3 4)))',
             r'(^ "hello" "world")',
             r'(begin (let ((x 3) (x 4)) (+ x 2)) (set! x 5) x)',
             r'(begin (define x 3) x)',
             r'(begin (define (f x) x))',
             r'(lambda (x y) (+ x y))',
             r'((lambda (x y) (+ x y)) 2 3)',
             r'((lambda (x) (+ x 0)) 2)',
             r'(begin (define (f x) (* x x)) (f 3))',
             r'(cons 2 3)',
             r'(car (cons 2 3))',
             r'(cdr (cons 2 3))',
             r'(apply + 2 1 4 (quote (1 2)))',
             r'(map * (quote (1 2 3)) (quote (1 2 3)) (quote (1 2 3)))',
             r'(define-macro (when x y) (eq? x y))',
             r'(begin (define-macro (when x y) (eq? x y)) (when 3 4))',
             r'(neq? 1 2)',
             r'(neq? 0 0)',
             r'(lt? 0 0)',
             r'(gt? 1 0)',
             r'(lte? 0 1)',
             r'(gte? 2 3)',
             r'(cond (#t (+ 3 4)) (else 4))',
             r'(cond (#f (+ 3 4)) (else 4))',
             r'(for ((i (list 1 2 3)) (j (list 4 5 6))) (+ i j) (- i j))',
             r'(for/list ((i (list 1 2 3)) (j (list 4 5 6))) (+ i j) (- i j))',
             r'(delay (/ 1 0))',
             r'(force (delay (/ 2 1)))',
             r'(begin (define p (delay (/ 1 1))) (force p))',
             r'(begin (define (decr count) (if (eq? count 0) (println "Done") (begin (println count) (decr (- count 1))) )) (decr 3))',
             r'(cons-stream 2 3)',
             r'(cdr-stream (cons-stream 2 3))',
             r'(define my-list (lambda ((variadic x)) x))',
             r'(begin (define my-list (lambda ((variadic x)) x)) (my-list 2 3 4))',
             r'(list (quote (1 2)) (quote (3 4)))',
             r'(append (quote (1 2)) (quote (3 4)))',
             r'(append (quote ((1 2) (3 4))) (quote ((5 6) (7 8))))',
             r'(begin (define (f x (variadic y)) (append y (list x))) (f 1 2 3))',
             r'(begin (define f (lambda (x (variadic y)) (append y (list x)))) (f 1 2 3))',
             r'(define p (delay (begin (print "hi") (/ 1 0))))',
             r'nil',
             r'()',
             r'(match 3 (_ (+ 2 3) (- 0 4)) (_ (+ 2 4) (- 5 6)))',
             r'(begin (match 3 (i (+ 2 i))))',
             r'(begin (match 3 (3 (+ 2 4))))',
             r'(match nil (nil (+ 2 4)))',
             r'(match (cons 2 3) ((cons i j) (+ i j)))',
             r'(match (list 2 3 (+ 4 5)) ((list i j k) (+ i j k)))',
             r'(match (list 2 3 (list 6 7)) ((list i j k) (+ i j) k))',
             r'(match (list 2 3 (list 6 7)) ((list i j (list k l)) (+ i j k l)))',
             r'(match (list 1 (list 2 3) (list 4 5) (list 6 7)) ((list (list a b) (list c d) (list k l)) (+ a b c d k l)))',
             r'(match (list 1 (list 2 3) (list 4 5) (list 6 7)) ((list x (list a b) (list c d) (list k l)) (+ x a b c d k l)))',
             r'(match (cons (cons 3 (cons 3 6)) 3) ((cons (cons a (cons b c)) d) (+ a b c d)))',
             r'(match (cons (cons 3 (cons 3 6)) (list 2 3)) ((cons (cons a (cons b c)) d) (+ a b c) d))',
             r'(match (cons (cons 3 (cons 3 6)) (list 3 3)) ((cons (cons a (cons b c)) (list d e)) (+ a b c d e)))',
             r'""',
             r'"hello world"',
             r'(^ (^ "hello" " ") "world")',
             r'(quote (quote 3))',
             r'(quote (quote (quote (4 (quote 3)))))',
             r'(quasiquote (quasiquote 3))',
             r"'hello",
             r"'3",
             r"'#t",
             r"'(+ 3 2)",
             r"'(+ 3 '(+ 4 3))",
             r"'(+ '(+ 4 3) 3)",
             r"`3",
             r"''3",
             r"`3",
             r"`'3",
             r"``(+ 3 '2)",
             r"`(+ 3 ,(+ 2 3))",
             r"`(+ ,(- 2 3) ,(+ 2 3) ,1)",
             r"`,`(+ ,(- 2 3) ,(+ 2 3) ,1)",
             r"(+ `3 '3)",
             r"`(+ 3 @(list 3 (+ 2 3)))",
             r"'(+ 3 @(list 3 (+ 2 3)))",
             r"`(+ 3 @(list 3 '(+ 2 3)))",
             r"(println (+ 2 3) (+ 3 4) (- 0 3) (+ 9 9))",
             r"(+ [+ 2 3] 4)",
             ";hello this is a comment\n (+ 2 3);2 3\n;2 3",
             r"[3 . 4]",
             r"((3 . (2 . 3)) . (2 . 5))",
             r"(3 . 4 . 5)",
             r"(1 . (3 . 4 . 5) . 2)",
             r"(0 . (1 . (2 . 3) . 4))",
             r"(0 . 1 . 2 . 3 . 4 . 5 . 6)",
             r"(0 . 1)",
             r"(0 . 1 . 2)",
             r"(0 . 1 . (2 . 3 . 4) . 5 . 6 . 7)",
             r"(0 . (1 . (2 . 3 . 4)) . (5 . 6 . 7))",
             r"((0 . (1 . (2 . 3 . 4))) . (5 . 6 . 7))",
             r"(1 $+$ 2)",
             r"(1 $+$ 2 $+$ 3)",
             r"(1 $+$ 2 $+$ 3 $+$ 4)",
             r"(1 $-$ 2 $-$ 3)",
             r"(1 $-$ 2 $-$ (1 $*$ 2 $*$ 3 $*$ 4 $*$ 5 $*$ 6))",
             r"(1 $+$ ((2 $*$ 3) $-$ 4))"]
    for string in tests:
        print("-" * 70)
        print(expr_to_str(frontend(string)))
        context = {}
        print(expr_to_str(eval_expr(frontend(string), context, False)))
