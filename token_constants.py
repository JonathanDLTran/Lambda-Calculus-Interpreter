ADD = "+"
SUB = "-"
MUL = "*"
DIV = "\\"
POW = "^"
BINOPS = [
    ADD, SUB, MUL, DIV, POW
]
UNOPS = [
    SUB
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
