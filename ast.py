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


class Boolean(Constant):
    def __init__(self, v):
        assert type(v) == bool
        super().__init__(v)

    def __str__(self):
        return f"{'#t' if self.value else '#f'}"


class Integer(Constant):
    def __init__(self, v):
        assert type(v) == int
        super().__init__(v)

    def __str__(self):
        return f"{self.value}"


class String(Constant):
    def __init__(self, v):
        assert type(v) == str
        super().__init__(v)

    def __str__(self):
        return f'"{self.value}"'


class Var(Expr):
    def __init__(self, var):
        assert type(var) == str
        super().__init__()
        self.var = var

    def get_var(self):
        return self.var

    def __str__(self):
        return f"{self.var}"


class Quote(Expr):
    def __init__(self, datum):
        super().__init__()
        self.datum = datum

    def get_datum(self):
        return self.datum

    def __str__(self):
        return f"(quote {self.datum})"


class Unquote(Expr):
    def __init__(self, expr):
        assert isinstance(expr, Expr)
        super().__init__()
        self.expr = expr

    def get_expr(self):
        return self.expr

    def __str__(self):
        return f"(unquote {self.expr})"


class Quasiquote(Expr):
    def __init__(self, expr):
        assert isinstance(expr, Expr)
        super().__init__()
        self.expr = expr

    def get_expr(self):
        return self.expr

    def __str__(self):
        return f"(quasiquote {self.expr})"


class If(Expr):
    def __init__(self, guard, expr):
        assert isinstance(guard, Expr)
        assert isinstance(expr, Expr)
        super().__init__()
        self.guard = guard
        self.expr = expr

    def get_guard(self):
        return self.guard

    def get_expr(self):
        return self.expr

    def set_guard(self, guard):
        assert isinstance(guard, Expr)
        self.guard = guard

    def set_expr(self, expr):
        assert isinstance(expr, Expr)
        self.expr = expr

    def __str__(self):
        return f"(if {self.guard} {self.expr})"


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

    def set_guard(self, guard):
        assert isinstance(guard, Expr)
        self.guard = guard

    def get_fst(self):
        return self.fst

    def set_fst(self, expr):
        assert isinstance(expr, Expr)
        self.fst = expr

    def get_snd(self):
        return self.snd

    def set_snd(self, expr):
        assert isinstance(expr, Expr)
        self.snd = expr

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

    def set_var(self, var):
        assert type(var) == str
        self.var = var

    def get_expr(self):
        return self.expr

    def set_expr(self, expr):
        assert isinstance(expr, Expr)
        self.expr = expr

    def __str__(self):
        return f"(set! {self.var} {self.expr})"


class App(Expr):
    def __init__(self, expr_list):
        assert type(expr_list) == list
        assert len(expr_list) >= 2
        for expr in expr_list:
            assert isinstance(expr, Expr)
        super().__init__()
        self.fun = expr_list[0]
        self.args = expr_list[1:]

    def get_args(self):
        return self.args

    def set_args(self, args):
        assert type(args) == list
        for arg in args:
            assert type(arg) == str
        self.args = args

    def get_fun(self):
        return self.fun

    def set_fun(self, fun):
        assert isinstance(fun, Expr)
        self.fun = fun

    def __str__(self):
        args_str = ""
        for i, arg in enumerate(self.args):
            args_str += str(arg)
            if i != len(self.args) - 1:
                args_str += " "
        return f"({self.fun} {args_str})"


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

    def set_args(self, args):
        assert type(args) == list
        for arg in args:
            assert type(arg) == str
        self.args = args

    def set_body(self, body):
        assert isinstance(body, Expr)
        self.body = body

    def __str__(self):
        args_str = ""
        for i, arg in enumerate(self.args):
            args_str += str(arg)
            if i != len(self.args) - 1:
                args_str += " "
        return f"(lambda [{args_str}] {self.body})"


class Let(Expr):
    def __init__(self, bindings, bodies):
        assert type(bodies) == list
        assert len(bodies) > 0
        for body in bodies:
            assert isinstance(body, Expr)
        assert type(bindings) == list
        for binding in bindings:
            assert type(binding) == tuple
            assert len(binding) == 2
            name, expr = binding
            assert type(name) == str
            assert isinstance(expr, Expr)
        super().__init__()
        self.bindings = bindings
        self.bodies = bodies

    def get_bindings(self):
        return self.bindings

    def get_bodies(self):
        return self.bodies

    def set_bindings(self, bindings):
        assert type(bindings) == list
        for binding in bindings:
            assert type(binding) == tuple
            assert len(binding) == 2
            name, expr = binding
            assert type(name) == str
            assert isinstance(expr, Expr)
        self.bindings = bindings

    def set_bodies(self, bodies):
        assert type(bodies) == list
        assert len(bodies) > 0
        for body in bodies:
            assert isinstance(body, Expr)
        self.bodies = bodies

    def __str__(self):
        bindings_str = ""
        for i, (name, expr) in enumerate(self.bindings):
            bindings_str += f"({name} {expr})"
            if i != len(self.bindings) - 1:
                bindings_str += " "
        bodies_str = ""
        for i, body in enumerate(self.bodies):
            bodies_str += str(body)
            if i != len(self.bodies) - 1:
                bodies_str += " "
        return f"(let [{bindings_str}] {bodies_str})"
