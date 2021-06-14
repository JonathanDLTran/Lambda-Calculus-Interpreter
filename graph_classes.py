class Node:
    def __init__(self, num, stmts, final=False):
        assert type(num) == int
        assert type(final) == bool
        super().__init__()
        self.num = num
        self.stmts = stmts
        self.final = final

    def get_num(self):
        return self.num

    def get_stmts(self):
        return self.stmts

    def get_final(self):
        return self.final

    def set_num(self, num):
        assert type(num) == int
        self.num = num

    def set_stmts(self, stmts):
        assert type(stmts) == list
        self.stmts = stmts

    def set_final(self, final):
        assert type(final) == bool
        self.final = final

    def __repr__(self):
        node_body = None
        if self.stmts == None:
            node_body = ""
        else:
            node_body = '\n'.join(list(map(lambda s: str(s), self.stmts)))
        return f"{node_body}"

    def __str__(self):
        return self.__repr__()


class Edge:
    def __init__(self, start, end, conds):
        assert type(conds) == list
        super().__init__()
        self.start = start
        self.end = end
        self.conds = conds

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_conds(self):
        return self.conds

    def set_start(self, start):
        assert type(start) == int
        assert start >= 1
        self.start = start

    def set_end(self, end):
        assert type(end) == int
        assert end >= 1
        self.end = end

    def set_conds(self, conds):
        assert type(conds) == list
        self.conds = conds

    def __repr__(self):
        edge_body = None
        if self.conds == None:
            edge_body = ""
        else:
            edge_body = '\n'.join(list(map(lambda s: str(s), self.conds)))
        return f"{edge_body}"

    def __str__(self):
        return self.__repr__()
