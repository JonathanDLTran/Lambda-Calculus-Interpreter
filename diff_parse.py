from token_constants import *


class Expr(object):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()


class Float(Expr):
    def __init__(self, float):
        super().__init__()
        self.float = float

    def __repr__(self):
        return f"{self.float}"

    def __str__(self):
        return self.__repr__()


class Var(Expr):
    def __init__(self, var):
        super().__init__()
        self.var = var

    def __repr__(self):
        return f"{self.var}"

    def __str__(self):
        return self.__repr__()


class Binop(Expr):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left}) {self.op} ({self.right})"

    def __str__(self):
        return self.__repr__()


class Unop(Expr):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"{self.op} {self.expr}"

    def __str__(self):
        return self.__repr__()


class Function(Expr):
    def __init__(self, f, expr):
        super().__init__()
        self.f = f
        self.expr = expr

    def __repr__(self):
        return f"{self.f}({self.expr})"

    def __str__(self):
        return self.__repr__()


class Const(Expr):
    def __init__(self, const):
        super().__init__()
        self.const = const

    def __repr__(self):
        return f"{self.const}"

    def __str__(self):
        return self.__repr__()


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

    return Float(tokens[0])


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


def main():
    pass


def test():
    tokens = [4., ADD, 3., SUB, 2., ADD, 5., ADD, 3., ADD, 3., MUL, 2.]
    print(parse(tokens))


if __name__ == "__main__":
    test()
