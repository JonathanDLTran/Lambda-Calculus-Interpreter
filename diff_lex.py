ADD = "+"
SUB = "-"
MUL = "*"
DIV = "\\"
POW = "^"
BINOPS = [
    ADD, SUB, MUL, DIV, POW
]

LEFT_PAREN = "("
RIGHT_PAREN = ")"
SEPARATORS = [
    LEFT_PAREN, RIGHT_PAREN
]

LN = "ln"
SIN = "sin"
COS = "cos"
FUNCTIONS = [
    LN, SIN, COS
]

PI = "pi"
EXP = "e"

CONSTANTS = [
    PI, EXP
]

KEYWORDS = sorted([
    *BINOPS, *SEPARATORS, *FUNCTIONS, *CONSTANTS
])

DOT = "."
SPACES = " \n\t\r"


def lex(string):
    """
    Lexes string into list of tokens,.
    """
    assert type(string) == str

    if string == "":
        return []

    l_string = len(string)
    for kw in KEYWORDS:
        l = len(kw)
        if l < l_string and string[:l] == kw:
            return [kw] +


def main():
    pass


def test():
    pass


if __name__ == "__main__":
    test()
