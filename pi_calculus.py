"""
Pi Calculus is an interpreter for the pi calculus

Some of the work is based from
https://cs.pomona.edu/~michael/courses/csci131f16/lec/Lec25.html
including the Operational Semantics
"""

# ------------ IMPORTS ------------
import threading
import random


# ------------ AST CLASSES ------------


class Process(object):
    def __init__(self):
        pass

    def __str__(self):
        return "Process Abstract Class"

    def __repr__(self):
        return self.__str__()


class Zero(Process):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "0"


class Respawn(Process):
    def __init__(self, proc):
        assert isinstance(proc, Process)
        super().__init__()
        self.proc = proc

    def get_proc(self):
        return self.proc

    def __str__(self):
        return f"!{self.proc}"


class Receive(Process):
    def __init__(self, channel, var, proc):
        assert isinstance(proc, Process)
        assert type(channel) == str
        assert type(var) == str
        self.channel = channel
        self.var = var
        self.proc = proc

    def get_proc(self):
        return self.proc

    def get_var(self):
        return self.var

    def get_channel(self):
        return self.channel

    def __str__(self):
        return f"{self.channel}({self.var}).{self.proc}"


class Send(Process):
    def __init__(self, channel, message, proc):
        assert isinstance(proc, Process)
        assert type(channel) == str
        assert type(message) == str
        self.channel = channel
        self.message = message
        self.proc = proc

    def get_proc(self):
        return self.proc

    def get_message(self):
        return self.message

    def get_channel(self):
        return self.channel

    def __str__(self):
        return f"_{self.channel}_<{self.message}>.{self.proc}"


class Or(Process):
    def __init__(self, left, right):
        assert isinstance(left, Process)
        assert isinstance(right, Process)
        super().__init__()
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def __str__(self):
        return f"{self.left} | {self.right}"


class New(Process):
    def __init__(self, var, proc):
        assert type(var) == str
        assert isinstance(proc, Process)
        super().__init__()
        self.var = var
        self.proc = proc

    def get_var(self):
        return self.var

    def get_proc(self):
        return self.proc

    def __str__(self):
        return f"\\{self.var}.{self.proc}"


# ------------ INTERPRETER CODE ------------
NEW_VAR = "__X__"
NEW_VAR_NUM = 1


def gen_var():
    global NEW_VAR_NUM
    new_var = NEW_VAR + str(NEW_VAR_NUM)
    NEW_VAR_NUM += 1
    return new_var


def subst(p, c, x):
    pass


def interpret(state):
    assert type(state) == tuple
    assert len(state) == 2
    (C, R) = state
    has_zero = False
    has_or = False
    has_respawn = False
    has_new = False
    for proc in R:
        if type(proc) == Zero:
            has_zero = True
        elif type(proc) == Or:
            has_or = True
        elif type(proc) == New:
            has_new = True
        elif type(proc) == Respawn:
            has_respawn = True
    if has_zero:
        new_R = list(filter(lambda proc: type(proc) != Zero, R))
        new_state = (C, new_R)
        return interpret(new_state)
    elif has_or:
        new_R = []
        for proc in R:
            if type(proc) == Or:
                new_R.append(proc.get_left())
                new_R.append(proc.get_right())
            else:
                new_R.append(proc)
        new_state = (C, new_R)
        return interpret(new_state)
    elif has_new:
        for i in range(len(R)):
            proc = R[i]
            if type(proc) == New:
                p = proc.get_proc()
                x = proc.get_var()
                c = gen_var()
                new_C = C.add(c)
                new_R = R[:i] + R[i + 1:]
                new_R.append(subst(p, c, x))
                new_state = (new_C, new_R)
                return interpret(new_state)
    # make last because respawn could just go forever
    elif has_respawn:
        new_R = []
        for proc in R:
            if type(proc) == Respawn:
                new_R.append(proc)
                new_R.append(proc.get_proc())
            else:
                new_R.append(proc)
        new_state = (C, new_R)
        return interpret(new_state)
    return 1


def interpret_main(process):
    assert isinstance(process, Process)
    channels = set()
    running_processes = [process]
    state = (channels, running_processes)
    return interpret(state)


# ------------ MAIN RUNNEr ------------

def main():
    process = Or(Zero(), Zero())
    return interpret_main(process)


if __name__ == "__main__":
    main()
