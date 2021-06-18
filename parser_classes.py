class Expr(object):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()


class Float(Expr):
    def __init__(self, f):
        super().__init__()
        self.float = f

    def get_f(self):
        return self.float

    def __repr__(self):
        return f"{self.float}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value):
        if type(value) != Float:
            return False
        return value.float == self.float


class Var(Expr):
    def __init__(self, var):
        super().__init__()
        self.var = var

    def get_var(self):
        return self.var

    def __repr__(self):
        return f"{self.var}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value):
        if type(value) != Var:
            return False
        return value.var == self.var


class Binop(Expr):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

    def get_op(self):
        return self.op

    def get_l(self):
        return self.left

    def get_r(self):
        return self.right

    def __repr__(self):
        return f"({self.left}) {self.op} ({self.right})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value):
        if type(value) != Binop:
            return False
        return value.op == self.op and value.left == self.left and value.right == self.right


class Unop(Expr):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

    def get_op(self):
        return self.op

    def get_e(self):
        return self.expr

    def __repr__(self):
        return f"{self.op} {self.expr}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value):
        if type(value) != Unop:
            return False
        return value.op == self.op and value.expr == self.expr


class Function(Expr):
    def __init__(self, f, expr):
        super().__init__()
        self.f = f
        self.expr = expr

    def get_f(self):
        return self.f

    def get_e(self):
        return self.expr

    def __repr__(self):
        return f"{self.f}({self.expr})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value):
        if type(value) != Function:
            return False
        return value.expr == self.expr and value.f == self.f


class Const(Expr):
    def __init__(self, const):
        super().__init__()
        self.const = const

    def __repr__(self):
        return f"{self.const}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value):
        if type(value) != Const:
            return False
        return value.const == self.const
