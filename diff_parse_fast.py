from token_constants import *
from parser_classes import *
from diff_lex import lex


def parse_float(tokens, start, end, parse_map):
    assert type(tokens) == list
    assert type(start) == int
    assert start >= 0
    assert type(end) == int
    assert end > start
    assert end <= len(tokens)
    assert len(tokens[start:end]) == 1
    assert type(tokens[start]) == float
    assert type(parse_map) == dict

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    result = Float(tokens[start])

    # add to map
    parse_map[(start, end)] = result

    return result


def parse_var(tokens, start, end, parse_map):
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

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    result = Var(tokens[start])

    # add to map
    parse_map[(start, end)] = result

    return result


def parse_binop(op, tokens, start, end, parse_map):
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

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    op_positions = []
    for i in range(len(tokens)):
        if i >= start and i < end:
            sym = tokens[i]
            if sym == op:
                op_positions.append(i)

    if op_positions == []:
        raise Exception(f"No Op {op} found in {tokens}.")

    for pos in op_positions:
        try:
            left_expr = parse_h(tokens, start, pos, parse_map)
            try:
                right_expr = parse_h(tokens, pos + 1, end, parse_map)
                result = Binop(op, left_expr, right_expr)

                # add to map
                parse_map[(start, end)] = result

                return result
            except Exception:
                pass
        except Exception:
            pass
    else:
        raise Exception(f"Failed to parse binop {tokens}.")


def parse_parens(tokens, start, end, parse_map):
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

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    result = parse_h(tokens, start + 1, end - 1, parse_map)

    # add to map
    parse_map[(start, end)] = result

    return result


def parse_unop(op, tokens, start, end, parse_map):
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

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    inner_parse = parse_h(tokens, start + 1, end, parse_map)
    result = Unop(op, inner_parse)

    # add to map
    parse_map[(start, end)] = result

    return result


def parse_const(tokens, start, end, parse_map):
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

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    result = Const(tokens[start])

    # add to map
    parse_map[(start, end)] = result

    return result


def parse_function(tokens, start, end, parse_map):
    assert type(tokens) == list
    assert type(start) == int
    assert start >= 0
    assert type(end) == int
    assert end > start
    assert end <= len(tokens)
    assert len(tokens[start:end]) >= 2
    assert tokens[start] in FUNCTIONS
    assert type(parse_map) == dict

    # check memoized
    if (start, end) in parse_map:
        return parse_map[(start, end)]

    inner_parse = parse_h(tokens, start + 1, end, parse_map)
    result = Function(tokens[start], inner_parse)

    # add to map
    parse_map[(start, end)] = result

    return result


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

    try:
        result = parse_float(tokens, start, end, parse_map)
        # add to map
        parse_map[(start, end)] = result
        return result
    except Exception:
        try:
            result = parse_const(tokens, start, end, parse_map)
            # add to map
            parse_map[(start, end)] = result
            return result
        except Exception:
            try:
                result = parse_var(tokens, start, end, parse_map)
                # add to map
                parse_map[(start, end)] = result
                return result
            except Exception:
                try:
                    result = parse_parens(tokens, start, end, parse_map)
                    # add to map
                    parse_map[(start, end)] = result
                    return result
                except Exception:
                    try:
                        result = parse_function(tokens, start, end, parse_map)
                        # add to map
                        parse_map[(start, end)] = result
                        return result
                    except Exception:
                        try:
                            for op in UNOPS:
                                try:
                                    result = parse_unop(op, tokens, start,
                                                        end, parse_map)
                                    # add to map
                                    parse_map[(start, end)] = result
                                    return result
                                except Exception:
                                    pass
                            raise Exception()
                        except Exception:
                            try:
                                for op in BINOPS:
                                    try:
                                        result = parse_binop(
                                            op, tokens, start, end, parse_map)
                                        # add to map
                                        parse_map[(start, end)] = result
                                        return result
                                    except Exception:
                                        pass
                                raise Exception()
                            except Exception:
                                raise Exception(
                                    f"Failed to match in Parse: {tokens}")


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
    if check_single_var(expr):
        return expr
    raise RuntimeError(f"More than 1 variable: {expr}.")


def test():
    s = "-6 - -5 + 4 + 3 + 2 + 1 + 0 ^ 3 + x"
    s = "x + (x * x) * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x * x"
    s = "((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3) + ((1 + 2) + 3)"
    tokens = lex(s)
    # tokens = [LN, LEFT_PAREN, 4., ADD, 3., RIGHT_PAREN, SUB, LEFT_PAREN,
    #           2., ADD, 5., ADD, 3., ADD, 3., MUL, 2., RIGHT_PAREN]
    print(parse(tokens))


if __name__ == "__main__":
    test()
