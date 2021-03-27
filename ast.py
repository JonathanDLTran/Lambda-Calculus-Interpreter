class Expr:
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Scheme Expr Abstract Class"

    def __repr__(self):
        return self.__str__()


class Constant(Expr):
    def __init__(self, v):
        super().__init__()
        self.value = v

    def get_value(self):
        return self.value

    def __str__(self):
        return f"{self.value}"


class Var(Expr):
    def __init__(self, var):
        assert type(var) == str
        super().__init__()
        self.var = var

    def get_var(self):
        return self.var

    def __str__(self):
        return f"{self.value}"


class Quote(Expr):
    def __init__(self, datum):
        super().__init__()
        self.datum = datum

    def get_datum(self):
        return self.datum

    def __str__(self):
        return f"(quote {self.datum})"


class If(Expr):
    def __init__(self, guard, body):
        super().__init__()
        self.guard = guard
        self.body = body

    def get_guard(self):
        return self.guard

    def get_body(self):
        return self.body

    def __str__(self):
        return f"(if {self.guard} {self.body})"


class IfElse(Expr):
    def __init__(self, guard, e1, e2):
        assert isinstance(guard, Expr)
        assert isinstance(e1, Expr)
        assert isinstance(e2, Expr)
        super().__init__()
        self.guard = guard
        self.fst = e1
        self.snd = e2

    def get_guard(self):
        return self.guard

    def get_fst(self):
        return self.fsg

    def get_snd(self):
        return self.snd

    def __str__(self):
        return f"(if {self.guard} {self.fst} {self.snd})"


class Set(Expr):
    def __init__(self, var, expr):
        assert type(var) == str
        assert isinstance(expr, Expr)
        super().__init__()
        self.var = var
        self.expr = expr

    def get_var(self):
        return self.var

    def get_expr(self):
        return self.expr

    def __str__(self):
        return f"(set! {self.var} {self.expr})"


class App(Expr):
    pass


class Lambda(Expr):
    def __init__(self, args_list, body):
        assert type(args_list) == list
        for arg in args_list:
            assert type(arg) == str
        assert isinstance(body, Expr)
        super().__init__()
        self.args = args_list
        self.body = body

    def get_args(self):
        return self.args

    def get_body(self):
        return self.body

    def __str__(self):
        args_str = ""
        for i, arg in enumerate(self.args):
            args_str += arg
            if i != len(self.args):
                args_str += " "
        return f"(lambda {args_str} {self.body})"
