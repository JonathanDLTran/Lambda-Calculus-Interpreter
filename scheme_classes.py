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
        assert len(args) >= 0  # 0 arg function allowed for defines
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


class Values():
    def __init__(self, values):
        assert type(values) == list
        assert len(values) >= 0
        self.values = values

    def get_values(self):
        return deepcopy(self.values)

    def get_num_values(self):
        return len(self.values)


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
