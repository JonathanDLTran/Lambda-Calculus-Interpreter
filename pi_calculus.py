"""
Pi Calculus is an interpreter for the pi calculus
"""

# ------------ IMPORTS ------------
import threading


# ------------ AST CLASSES ------------


class Process(Object):
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
        return f"->{self.channel}[{self.var}].{self.proc}"


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
        return f"<-{self.channel}({self.message}).{self.proc}"


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
        return f"\'{self.var}.{self.proc}"


# ------------ INTERPRETER CODE ------------


def interpret(process):
    assert isinstance(process, Process)


# ------------ MAIN RUNNEr ------------

def main():
    pass


if __name__ == "__main__":
    main()
