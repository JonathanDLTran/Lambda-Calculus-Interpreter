ADD = "+"
SUB = "-"
MUL = "*"
DIV = "\\"
POW = "^"
# reverse ordered by precedence to allow grouping more tightly those
# terms with higher precedence
# e.g. ADD has lowest, POW has highest
BINOPS = [
    ADD, SUB, MUL, DIV, POW
]
UNOPS = [
    SUB
]
OPS = {
    *UNOPS, *BINOPS
}


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
