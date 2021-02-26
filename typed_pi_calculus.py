"""
Pi Calculus is an interpreter for the pi calculus

Some of the work is based from
https://cs.pomona.edu/~michael/courses/csci131f16/lec/Lec25.html
including the Operational Semantics

Typed idea comes from
https://fzn.fr/teaching/mpri/2006/pitypes.pdf
"""

# ------------ IMPORTS ------------
import threading
from random import shuffle
from copy import deepcopy


# ----------- CLASSES FOR TYPES --------
class Type(object):
    def __init__(self):
        pass

    def __str__(self):
        return "Type Abstract Class"

    def __repr__(self):
        return self.__str__()


class TUnit(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "unit"


class TInt(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "int"


class TBool(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "bool"


class TPair(Type):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def __str__(self):
        return f"({self.left} * {self.right})"


class TChannel(Type):
    def __init__(self, typ):
        super().__init__()
        self.typ = typ

    def get_type(self):
        return self.typ

    def __str__(self):
        return f"[{self.typ} channel]"

# ------------ MESSAGE CLASSES ------------


class Message(object):
    def __init__(self):
        pass

    def __str__(self):
        return f"Abstract Message Class"

    def __repr__(self):
        return self.__str__()


class Var(Message):
    def __init__(self, var):
        super().__init__()
        assert type(var) == str
        self.var = var

    def __str__(self):
        return self.var


class Int(Message):
    def __init__(self, i):
        super().__init__()
        assert type(i) == int
        self.i = i

    def __str__(self):
        return str(self.i)


class Bool(Message):
    def __init__(self):
        super().__init__()
        assert type(b) == bool
        self.b = b

    def __str__(self):
        return str(self.b)


class Unit(Message):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "()"


class Pair(Message):
    def __init__(self, left, right):
        super().__init__()
        assert isinstance(left, Message)
        assert isinstance(right, Message)
        self.left = left
        self.right = right

    def __str__(self):
        return f"({str(self.left)}, {str(self.right)})"


# ------------ PROCESS CLASSES ------------


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
        return f"@{self.channel}({self.var}).{self.proc}"


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
        return f"->{self.channel}<{self.message}>.{self.proc}"


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

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

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

# ------------ TYPE CHCKER CODE ------------


# ------------ INTERPRETER CODE ------------
NEW_VAR = "__X__"
NEW_VAR_NUM = 1


def gen_var():
    global NEW_VAR_NUM
    new_var = NEW_VAR + str(NEW_VAR_NUM)
    NEW_VAR_NUM += 1
    return new_var


def fv(proc):
    assert isinstance(proc) == Process
    if type(proc) == Zero:
        return []
    elif type(proc) == Send:
        return [proc.get_channel(), proc.get_message()] + fv(proc.get_proc())
    elif type(proc) == Receive:
        return [proc.get_channel()] + list(filter(lambda v: v != proc.get_var(), fv(proc.get_proc())))
    elif type(proc) == Or:
        return fv(proc.get_left()) + fv(proc.get_right())
    elif type(proc) == New:
        return list(filter(lambda v: v != proc.get_var(), fv(proc.get_proc())))
    elif type(proc) == Respawn:
        return fv(proc.get_proc())
    else:
        raise RuntimeError(f"No Matching Case in FV: {proc}")


def subst(proc, c, x, bound):
    """
    subst c for x in proc
    """
    assert isinstance(proc, Process)

    if type(proc) == Zero:
        return proc
    elif type(proc) == Send:
        channel = proc.get_channel()
        msg = proc.get_message()
        sub_proc = proc.get_proc()
        new_channel = c if x == channel and channel not in bound else channel
        new_msg = c if x == msg and msg not in bound else msg
        new_sub_proc = subst(sub_proc, c, x, deepcopy(bound))
        new_proc = Send(new_channel, new_msg, new_sub_proc)
        return new_proc
    elif type(proc) == Receive:
        channel = proc.get_channel()
        var = proc.get_var()
        sub_proc = proc.get_proc()
        new_channel = c if x == channel and channel not in bound else channel
        bound.add(var)
        new_sub_proc = subst(sub_proc, c, x, deepcopy(bound))
        new_proc = Send(new_channel, var, new_sub_proc)
        return new_proc
    elif type(proc) == Or:
        new_left = subst(proc.get_left(), c, x, deepcopy(bound))
        new_right = subst(proc.get_right(), c, x, deepcopy(bound))
        new_proc = Or(new_left, new_right)
        return new_proc
    elif type(proc) == New:
        var = proc.get_var()
        sub_proc = proc.get_proc()
        bound.add(var)
        new_sub_proc = subst(sub_proc, c, x, deepcopy(bound))
        new_proc = New(var, new_sub_proc)
        return new_proc
    elif type(proc) == Respawn:
        new_body = subst(proc.get_proc(), c, x, deepcopy(bound))
        new_proc = Respawn(new_body)
        return new_proc
    else:
        raise RuntimeError(f"No Matching Case in Subst: {proc}")


def interpret(state):
    print(state)
    assert type(state) == tuple
    assert len(state) == 2
    (C, R) = state
    shuffle(R)
    has_zero = -1
    has_or = -1
    has_respawn = -1
    has_new = -1
    has_send = -1
    has_receive = -1
    for i in range(len(R)):
        proc = R[i]
        if type(proc) == Zero:
            has_zero = i
        elif type(proc) == Or:
            has_or = i
        elif type(proc) == New:
            has_new = i
        elif type(proc) == Respawn:
            has_respawn = i
        elif type(proc) == Send:
            has_send = i
        elif type(proc) == Receive:
            has_receive = i
    if has_zero >= 0:
        new_R = R[:has_zero] + R[has_zero + 1:]
        new_state = (C, new_R)
        return interpret(new_state)
    elif has_or >= 0:
        proc = R[has_or]
        new_R = R[:has_or] + [proc.get_left(), proc.get_right()] + \
            R[has_or + 1:]
        new_state = (C, new_R)
        return interpret(new_state)
    elif has_new >= 0:
        proc = R[has_new]
        p = proc.get_proc()
        x = proc.get_var()
        c = gen_var()
        C.add(c)
        new_R = R[:has_new] + R[has_new + 1:]
        new_R.append(subst(p, c, x, set()))
        new_state = (C, new_R)
        return interpret(new_state)
    elif has_send >= 0 and has_receive >= 0:
        q = R[has_send]
        p = R[has_receive]
        q_proc = q.get_proc()
        q_msg = q.get_message()
        q_chan = q.get_channel()
        p_proc = p.get_proc()
        p_var = p.get_var()
        p_chan = p.get_channel()
        if p_chan != q_chan:
            return interpret(state)
        new_R = R[:min(has_receive, has_send)] + \
            R[min(has_receive, has_send): max(has_receive, has_send)] + \
            R[max(has_receive, has_send)] + \
            [q_proc] + \
            [subst(p_proc, q_msg, p_var, set())]
        new_state = (C, new_R)
        return interpret(new_state)
    # make last because respawn could just go forever
    elif has_respawn >= 0:
        new_R = R[:has_respawn] + [proc, proc.get_proc()] + R[has_respawn + 1:]
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
    process = Or(Or(Send("x", "y", Zero()), New(
        "x", Receive("x", "x", Zero()))), Zero())
    return interpret_main(process)


if __name__ == "__main__":
    main()
