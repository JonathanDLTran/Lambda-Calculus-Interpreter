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

    def get_var(self):
        return self.var

    def __str__(self):
        return self.var


class Int(Message):
    def __init__(self, i):
        super().__init__()
        assert type(i) == int
        self.i = i

    def get_int(self):
        return self.i

    def __str__(self):
        return str(self.i)


class Bool(Message):
    def __init__(self):
        super().__init__()
        assert type(b) == bool
        self.b = b

    def get_bool(self):
        return self.b

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

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

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
    def __init__(self, channel, var, var_type, proc):
        assert isinstance(proc, Process)
        assert type(channel) == Var
        assert type(var) == Var
        assert isinstance(var_type, Type)
        self.channel = channel
        self.var = var
        self.proc = proc
        self.var_type = var_type

    def get_proc(self):
        return self.proc

    def get_var(self):
        return self.var

    def get_channel(self):
        return self.channel

    def get_var_type(self):
        return self.var_type

    def __str__(self):
        return f"@{self.channel}({self.var} : {self.var_type}).{self.proc}"


class Send(Process):
    def __init__(self, channel, message, proc):
        assert isinstance(proc, Process)
        assert type(channel) == Var
        assert isinstance(message, Message)
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
    def __init__(self, var, channel_type, proc):
        assert type(var) == Var
        assert isinstance(proc, Process)
        assert isinstance(channel_type, Type)
        super().__init__()
        self.var = var
        self.proc = proc
        self.channel_type = channel_type

    def get_var(self):
        return self.var

    def get_proc(self):
        return self.proc

    def get_channel_type(self):
        return self.channel_type

    def __str__(self):
        return f"(\\{self.var} : {self.channel_type}).{self.proc}"


class TupMatch(Process):
    def __init__(self, z, x, y, x_type, y_type, proc):
        assert type(z) == Var
        assert type(x) == Var
        assert type(y) == Var
        assert isinstance(x_type, Type)
        assert isinstance(y_type, Type)
        assert isinstance(proc, Process)
        self.z = z
        self.x = x
        self.y = y
        self.x_type = x_type
        self.y_type = y_type
        self.proc = proc

    def get_z(self):
        return self.z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_x_type(self):
        return self.x_type

    def get_y_type(self):
        return self.y_type

    def get_proc(self):
        return self.proc

    def __str__(self):
        return f"match {self.z} with ({self.x} : {self.x_type}, {self.y} : {self.y_type}) in {self.proc}"

# ------------ TYPE CHCKER CODE ------------


def check_message(ctx, msg):
    """
    Check Message ctx, msg is the raw type of msg
    """
    assert isinstance(msg, Message)
    if type(msg) == Int:
        return TInt
    elif type(msg) == Bool:
        return TBool
    elif type(msg) == Unit:
        return TUnit
    elif type(msg) == Pair:
        left = check_message(msg.get_left())
        right = check_message(msg.get_right())
        return TPair(left, right)
    elif type(msg) == Var:
        return ctx[msg]
    else:
        raise TypeError(f"Message {msg} is not well typed under {ctx}")


def check_process(ctx, proc):
    assert isinstance(proc, Process)
    if type(proc) == Zero:
        return True
    elif type(proc) == Or:
        left = check_process(ctx, proc.get_left())
        right = check_process(ctx, proc.get_right())
        return left and right
    elif type(proc) == New:
        var = proc.get_var()
        var_type = proc.get_channel_type()
        sub_proc = proc.get_proc()
        new_ctx = deepcopy(ctx)
        new_ctx[var.get_var()] = TChannel(var_type)
        return check_process(new_ctx, sub_proc)
    elif type(proc) == Receive:
        channel = proc.get_channel()
        chan = channel.get_var()
        if chan not in ctx:
            raise TypeError(
                f"Type Error: Receive: {proc} error, {chan} not bound in {ctx}")
        bound_type = ctx[chan]
        if type(bound_type) != TChannel:
            raise TypeError(
                f"Type Error: Receive: {proc} error, {chan} not of type TChannel, it is {bound_type}")
        var = proc.get_var()
        var_type = proc.get_var_type()
        sub_proc = proc.get_proc()
        new_ctx = deepcopy(ctx)
        new_ctx[var.get_var()] = var_type
        return check_process(new_ctx, sub_proc)
    elif type(proc) == Send:
        channel = proc.get_channel()
        chan = channel.get_var()
        if chan not in ctx:
            raise TypeError(
                f"Type Error: Send: {proc} error, {chan} not bound in {ctx}")
        bound_type = ctx[chan]
        if type(bound_type) != TChannel:
            raise TypeError(
                f"Type Error: Send: {proc} error, {chan} not of type TChannel, it is {bound_type}")
        msg = proc.get_message()
        msg_type = check_message(ctx, msg)
        chan_type = ctx[chan]
        if TChannel(msg_type) is chan_type:
            raise TypeError(
                f"Type Error: Send: {proc} error, message type {msg_type} not equal to the channel type {chan_type}")
        sub_proc = proc.get_proc()
        return check_process(ctx, sub_proc)
    elif type(proc) == TupMatch:
        z = proc.get_z()
        x = proc.get_x()
        y = proc.get_y()
        x_typ = proc.get_x_type()
        y_typ = proc.get_y_type()
        sub_proc = proc.get_proc()
        z_type = ctx[z.get_var()]
        if z_type != TPair(x_typ, y_typ):
            raise TypeError(
                f"Type Error: Match: {proc} error, z type {z_type}, expect Pair Type {TPair(x_typ, y_typ)}")
        new_ctx = deepcopy(ctx)
        new_ctx[x] = x_typ
        new_ctx[y] = y_typ
        return check_process(new_ctx, sub_proc)
    elif type(proc) == Respawn:
        sub_proc = proc.get_proc()
        return check_process(ctx, sub_proc)
    else:
        raise TypeError(f"Process {proc} is not well typed under {ctx}")


def check_main(proc):
    assert isinstance(proc, Process)
    ctx = {}
    return check_process(ctx, proc)


# ------------ INTERPRETER CODE ------------
NEW_VAR_PREFIX_STRING = "__X__"
NEW_VAR_NUM = 1


def gen_var():
    global NEW_VAR_NUM
    new_var = Var(NEW_VAR_PREFIX_STRING + str(NEW_VAR_NUM))
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


# ------------ MAIN RUNNER ------------

def main():
    process = New(Var("x"), TInt(), Or(
        Send(Var("x"), Int(3), Zero()),
        Receive(Var("x"), Var("y"), TInt(), Zero()
                )))
    check_main(process)
    return interpret_main(process)


if __name__ == "__main__":
    main()
