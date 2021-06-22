from token_constants import *
from parser_classes import *
from diff_lex import lex


FLOAT = "float"
CONST = "const"
VAR = "var"
UNOP = "unop"
FUNC = "func"
BINOP = "binop"
PARENS = "parens"


def parse_float(tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) == 1
        assert type(tokens[start]) == float
        assert type(parse_map) == dict
    except Exception:
        return None

    return Float(tokens[start])


def parse_var(tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) == 1
        assert type(tokens[start]) == str
        assert tokens[start] not in CONSTANTS
        assert type(parse_map) == dict
    except Exception:
        return None

    return Var(tokens[start])


def parse_binop(op, tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert op in BINOPS
        assert op in tokens
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) >= 3
        assert type(parse_map) == dict
    except Exception:
        return None

    op_positions = []
    for i in range(len(tokens)):
        if i >= start and i < end:
            sym = tokens[i]
            if sym == op:
                op_positions.append(i)

    if op_positions == []:
        return None

    for pos in op_positions:
        left_expr = parse_h(tokens, start, pos, parse_map)
        if left_expr != None:
            right_expr = parse_h(tokens, pos + 1, end, parse_map)
            if right_expr != None:
                return Binop(op, left_expr, right_expr)

    return None


def parse_parens(tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) >= 3
        assert tokens[start] == LEFT_PAREN
        assert tokens[end - 1] == RIGHT_PAREN
        assert type(parse_map) == dict
    except Exception:
        return None

    return parse_h(tokens, start + 1, end - 1, parse_map)


def parse_unop(op, tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert op in UNOPS
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) >= 2
        assert tokens[start] == op
        assert type(parse_map) == dict
    except Exception:
        return None

    inner_parse = parse_h(tokens, start + 1, end, parse_map)
    return Unop(op, inner_parse)


def parse_const(tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) == 1
        assert type(tokens[start]) == str
        assert tokens[start] in CONSTANTS
        assert type(parse_map) == dict
    except Exception:
        return None

    return Const(tokens[start])


def parse_function(tokens, start, end, parse_map):
    try:
        assert type(tokens) == list
        assert type(start) == int
        assert start >= 0
        assert type(end) == int
        assert end > start
        assert end <= len(tokens)
        assert len(tokens[start:end]) >= 2
        assert tokens[start] in FUNCTIONS
        assert type(parse_map) == dict
    except Exception:
        return None

    inner_parse = parse_h(tokens, start + 1, end, parse_map)
    return Function(tokens[start], inner_parse)


def parse_h(tokens, start, end, parse_map):
    assert type(tokens) == list
    assert type(start) == int
    assert start >= 0
    assert type(end) == int
    assert end > start
    assert end <= len(tokens)
    assert type(parse_map) == dict

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    float_res = parse_float(tokens, start, end, parse_map)
    if float_res != None:
        parse_map[(start, end)] = float_res
        return float_res

    const_res = parse_const(tokens, start, end, parse_map)
    if const_res != None:
        parse_map[(start, end)] = const_res
        return const_res

    var_res = parse_var(tokens, start, end, parse_map)
    if var_res != None:
        parse_map[(start, end)] = var_res
        return var_res

    parens_res = parse_parens(tokens, start, end, parse_map)
    if parens_res != None:
        parse_map[(start, end)] = parens_res
        return parens_res

    func_res = parse_function(tokens, start, end, parse_map)
    if func_res != None:
        parse_map[(start, end)] = func_res
        return func_res

    unop_res = None
    for op in UNOPS:
        unop_res = parse_unop(op, tokens, start, end, parse_map)
        if unop_res != None:
            parse_map[(start, end)] = unop_res
            return unop_res

    binop_res = None
    for op in BINOPS:
        binop_res = parse_binop(op, tokens, start, end, parse_map)
        if binop_res != None:
            parse_map[(start, end)] = binop_res
            return binop_res

    parse_map[(start, end)] = None
    return None


def get_vars(expr):
    assert isinstance(expr, Expr)

    if type(expr) == Float:
        return []
    elif type(expr) == Const:
        return []
    elif type(expr) == Var:
        return [expr.get_var()]
    elif type(expr) == Function:
        return get_vars(expr.get_e())
    elif type(expr) == Binop:
        return get_vars(expr.get_l()) + get_vars(expr.get_r())
    elif type(expr) == Unop:
        return get_vars(expr.get_e())


def check_single_var(expr):
    assert isinstance(expr, Expr)

    return len(set(get_vars(expr))) <= 1


def parse(tokens):
    assert type(tokens) == list

    parse_map = dict()
    expr = parse_h(tokens, 0, len(tokens), parse_map)
    if expr == None:
        raise RuntimeError(f"Failed to parse: {tokens}.")
    if check_single_var(expr):
        return expr
    raise RuntimeError(f"More than 1 variable: {expr}.")


def test():
    s = "-6 - -5 + 4 + 3 + 2 + 1 + 0 ^ 3 + x"
    s = "x + (x * x) * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x"
    s = "((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3)"
    tokens = lex(s)
    # tokens = [LN, LEFT_PAREN, 4., ADD, 3., RIGHT_PAREN, SUB, LEFT_PAREN,
    #           2., ADD, 5., ADD, 3., ADD, 3., MUL, 2., RIGHT_PAREN]
    print(parse(tokens))


if __name__ == "__main__":
    test()
