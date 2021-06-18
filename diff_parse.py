from token_constants import *
from parser_classes import *


def parse_float(tokens):
    assert type(tokens) == list
    assert len(tokens) == 1
    assert type(tokens[0]) == float

    return Float(tokens[0])


def parse_var(tokens):
    assert type(tokens) == list
    assert len(tokens) == 1
    assert type(tokens[0]) == str
    assert tokens[0] not in CONSTANTS

    return Var(tokens[0])


def parse_binop(op, tokens):
    assert type(tokens) == list
    assert len(tokens) >= 3
    assert op in BINOPS
    assert op in tokens

    op_positions = []
    for i in range(len(tokens)):
        sym = tokens[i]
        if sym == op:
            op_positions.append(i)

    if op_positions == []:
        raise Exception(f"No Op {op} found in {tokens}.")

    for pos in op_positions:
        try:
            left_expr = parse(tokens[:pos])
            try:
                right_expr = parse(tokens[pos + 1:])
                return Binop(op, left_expr, right_expr)
            except Exception:
                pass
        except Exception:
            pass
    else:
        raise Exception(f"Failed to parse binop {tokens}.")


def parse_parens(tokens):
    assert type(tokens) == list
    assert len(tokens) >= 3
    assert tokens[0] == LEFT_PAREN
    assert tokens[-1] == RIGHT_PAREN

    return parse(tokens[1:-1])


def parse_unop(op, tokens):
    assert type(tokens) == list
    assert len(tokens) >= 2
    assert op in UNOPS
    assert tokens[0] == op

    result = parse(tokens[1:])
    return Unop(op, result)


def parse_const(tokens):
    assert type(tokens) == list
    assert len(tokens) == 1
    assert type(tokens[0]) == str
    assert tokens[0] in CONSTANTS

    return Const(tokens[0])


def parse_function(tokens):
    assert type(tokens) == list
    assert len(tokens) >= 2
    assert tokens[0] in FUNCTIONS

    result = parse(tokens[1:])
    return Function(tokens[0], result)


def parse(tokens):
    assert type(tokens) == list

    try:
        return parse_float(tokens)
    except Exception:
        try:
            return parse_const(tokens)
        except Exception:
            try:
                return parse_var(tokens)
            except Exception:
                try:
                    return parse_parens(tokens)
                except Exception:
                    try:
                        return parse_function(tokens)
                    except Exception:
                        try:
                            for op in UNOPS:
                                try:
                                    parse_unop(op, tokens)
                                except Exception:
                                    pass
                            raise Exception()
                        except Exception:
                            try:
                                for op in BINOPS:
                                    try:
                                        return parse_binop(op, tokens)
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


def parse_main(tokens):
    assert type(tokens) == list

    expr = parse(tokens)
    if check_single_var(expr):
        return expr
    raise RuntimeError(f"More than 1 variable: {expr}.")


def test():
    tokens = [LN, LEFT_PAREN, 4., ADD, 3., RIGHT_PAREN, SUB, LEFT_PAREN,
              2., ADD, 5., ADD, 3., ADD, 3., MUL, 2., RIGHT_PAREN]
    print(parse(tokens))


if __name__ == "__main__":
    test()
