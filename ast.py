class AST:
    """
    AST is an abstract syntax tree
    """

    def __init__(self):
        self.sentences = []

    def is_empty(self):
        return self.sentences == []


class Expr(object):
    """
    Expr respresents an expression
    ABSTRACT CLASS for all instantiated expression classes
    """

    def __init__(self):
        pass

    def __repr__(self):
        return "This is a abstract expression"


class IntValue(Expr):
    """
    IntValue represents an Int Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(IntValue: " + str(self.value) + ")"


class BoolValue(Expr):
    """
    BoolValue represents an Bool Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(BoolValue: " + str(self.value) + ")"


class FloatValue(Expr):
    """
    FloatValue represents an float Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(FloatValue: " + str(self.value) + ")"


class StrValue(Expr):
    """
    StrValue represents an String
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(StrValue: " + str(self.value) + ")"


class VarValue(Expr):
    """
    IntValue represents an Variable Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(VarValue: " + str(self.value) + ")"


class Tuple(Expr):
    """
    Tuple represents an Tuple
    """

    def __init__(self, exprs_list):
        super().__init__()
        self.exprs = exprs_list
        self.length = len(exprs_list)

    def get_exprs(self):
        return self.exprs

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Tuple: (" + ", ".join(list(map(lambda e: str(e), self.exprs))) + "))"


class List(Expr):
    """
    List represents an list
    """

    def __init__(self, exprs_list):
        super().__init__()
        self.exprs = exprs_list
        self.length = len(exprs_list)

    def get_exprs(self):
        return self.exprs

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(List: [" + ", ".join(list(map(lambda e: str(e), self.exprs))) + "])"


class Dict(Expr):
    """
    Dict represents an dictionary
    """

    def __init__(self, keys_list, values_list):
        super().__init__()
        assert len(keys_list) == len(values_list)
        self.keys = keys_list
        self.values = values_list
        self.length = len(values_list)

    def get_keys(self):
        return self.keys

    def get_vals(self):
        return self.values

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Dict: {" + ", ".join(list(map(lambda k, v: str(k) + " : " + str(v), self.keys, self.values))) + "})"


class Struct(Expr):
    """
    Struct represents an struct
    """

    def __init__(self, keys_list, values_list):
        super().__init__()
        assert len(keys_list) == len(values_list)
        self.keys = keys_list
        self.values = values_list
        self.length = len(values_list)

    def get_keys(self):
        return self.keys

    def get_vals(self):
        return self.values

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Struct: {|" + ", ".join(list(map(lambda k, v: str(k) + " : " + str(v), self.keys, self.values))) + "|})"


class Bop(Expr):
    """
    Bop represents e1 bop e2
    """

    def __init__(self, bop, left=None, right=None):
        super().__init__()
        self.bop = bop
        self.left = left
        self.right = right

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def get_bop(self):
        return self.bop

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def __repr__(self):
        return "(BOP: " + str(self.left) + str(self.bop) + str(self.right) + ")"


class Unop(Expr):
    """
    Unop represents unop e
    """

    def __init__(self, unop, expr=None):
        super().__init__()
        self.unop = unop
        self.expr = expr

    def set_expr(self, expr):
        self.expr = expr

    def get_unop(self):
        return self.unop

    def get_expr(self):
        return self.expr

    def __repr__(self):
        return "(UNOP: " + str(self.unop) + str(self.expr) + ")"


class Assign(Expr):
    """
    assign represents var assign expre
    """

    def __init__(self, var, expr=None):
        super().__init__()
        self.var = var
        self.expr = expr

    def set_expr(self, expr):
        self.expr = expr

    def set_var(self, var):
        self.var = var

    def get_expr(self):
        return self.expr

    def get_var(self):
        return self.var

    def __repr__(self):
        return "(Assign: " + str(self.var) + " := " + str(self.expr) + ")"


class While(Expr):
    """
    While represents
    while guard_expr dowhile
        phrases
    endwhile
    """

    def __init__(self, guard=None, body_list=None):
        super().__init__()
        self.guard = guard
        self.body = body_list

    def set_guard(self, guard):
        self.guard = guard

    def set_body(self, body_list):
        self.body = body_list

    def get_guard(self):
        return self.guard

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(while " + str(self.guard) + " dowhile\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendwhile)"


class For(Expr):
    """
    For represents
    For var from int to int by int dofor
        phrases
    endfor
    """

    def __init__(self, index, from_int, end_int, by, body_list):
        super().__init__()
        self.index = index
        self.from_int = from_int
        self.end_int = end_int
        self.by = by
        self.body = body_list

    def get_index(self):
        return self.index

    def get_from(self):
        return self.from_int

    def get_end(self):
        return self.end_int

    def get_by(self):
        return self.by

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(for " + str(self.index) + " from " + str(self.from_int) + " to " + str(self.end_int) + " by " + str(self.by) + " dofor\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendfor)"


class Function(Expr):
    """
    Function represents
    fun f a b c ->
        body
    endfun
    """

    def __init__(self, name, args_list, body_list):
        super().__init__()
        self.name = name
        self.args = args_list
        self.body = body_list

    def get_name(self):
        return self.name

    def get_args(self):
        return self.args

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(fun " + str(self.name) + " " + " ".join(list(map(lambda arg: str(arg), self.args))) + " ->\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendfun)"


class IfThenElse(Expr):
    """
    IFThenElse represents an if then else erpression
    """

    def __init__(self, if_guard, if_body, elif_guards=[], elif_bodies=[], else_body=None):
        super().__init__()
        self.if_pair = (if_guard, if_body)
        self.elif_list = (elif_guards, elif_bodies)
        self.else_body = else_body

    def get_if_pair(self):
        return self.if_pair

    def get_elif_pair_list(self):
        return self.elif_list

    def get_else(self):
        return self.else_body

    def __repr__(self):
        (if_guard, if_body) = self.if_pair
        elif_guards, elif_bodies = self.elif_list
        else_body = self.else_body
        return ("(if " + str(if_guard) + " then\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), if_body))) + "\nendif\n"
                + ("" if elif_guards == [] else "\n".join(list(map(lambda g, b: "elif " + str(g) + " then\n\t" +
                                                                   "\n\t".join(list(map(lambda phrase: str(phrase), b))) + "\nendelif\n", elif_guards, elif_bodies))))
                + ("" if else_body == None else "else\n\t" +
                   "\n\t".join(list(map(lambda phrase: str(phrase), else_body))) + "\nendelse\n")
                + ")"
                )


class Extern(Expr):
    """
    Extern represents fun extern (arg1 arg2...) with possibly no args as in
    extern () , with only open and close brackets.
    """

    def __init__(self, fun, args_list=[]):
        super().__init__()
        self.fun = fun
        self.args_list = args_list

    def set_args(self, args_list):
        self.args_list = args_list

    def get_fun(self):
        return self.fun

    def get_args(self):
        return self.args_list

    def __repr__(self):
        return "(Extern: " + str(self.fun) + "(" + (" ".join(list(map(lambda a: str(a), self.args_list)))) + ")" + ")"


class Apply(Expr):
    """
    Apply represents fun (arg1 arg2...) with possibly no args as in
    fun () , with only open and close brackets.
    """

    def __init__(self, fun, args_list=[]):
        super().__init__()
        self.fun = fun
        self.args_list = args_list

    def set_args(self, args_list):
        self.args_list = args_list

    def get_fun(self):
        return self.fun

    def get_args(self):
        return self.args_list

    def __repr__(self):
        return "(Apply: " + str(self.fun) + "(" + (" ".join(list(map(lambda a: str(a), self.args_list)))) + ")" + ")"


class Return(Expr):
    """
    return represents
    return expr;
    """

    def __init__(self, body):
        super().__init__()
        self.body = body

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(Return: " + str(self.body) + ";)"


class Ignore(Expr):
    """
    ignore represents
    expr;
    """

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def get_expr(self):
        return self.expr

    def __repr__(self):
        return "(Ignore: " + str(self.expr) + ";)"


class Program(Expr):
    """
    Program represents a syntacucally valid program
    """

    def __init__(self, phrase_list=[]):
        super().__init__()
        self.phrases = phrase_list

    def get_phrases(self):
        return self.phrases

    def __repr__(self):
        return "(Program:\n" + "\n".join(list(map(lambda phrase: str(phrase), self.phrases))) + "\n)"
