PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
OPERATORS = [
    PLUS,
    MINUS,
    TIMES,
    DIV,
]

LPAREN = "("
RPAREN = ")"
LBRACKET = "["
RBRACKET = "]"
DELIMITERS = [
    LPAREN,
    RPAREN,
    LBRACKET,
    RBRACKET,
]

DEFINE = "define"
IF = "if"
COND = "cond"
AND = "and"
OR = "or"
LET = "let"
BEGIN = "begin"
LAMBDA = "lambda"
MU = "mu"
QUOTE = "quote"
QUASIQUOTE = "quasiquote"
UNQUOTE = "unquote"
DELAY = "delay"
CONS_STREAM = "cons-stream"
SET = "set!"
UNQUOTE_SPLICING = "unquote-splicing"
DEFINE_MACRO = "define-macro"

KEYWORDS = [
    DEFINE,
    IF,
    COND,
    AND,
    OR,
    LET,
    BEGIN,
    LAMBDA,
    MU,
    QUOTE,
    QUASIQUOTE,
    UNQUOTE,
    DELAY,
    CONS_STREAM,
    SET,
    UNQUOTE_SPLICING,
    DEFINE_MACRO]

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "".join([c.upper() for c in LOWERCASE])
LETTERS = LETTERS + UPPERCASE
DIGIT = "0123456789"
IDENTIFIER = "!@#$%^&*~`"


SYMBOLS = [
    *KEYWORDS,
    *OPERATORS,
    *DELIMITERS,
]

SYMBOLS = sorted(SYMBOLS)

EMPTY = ""
SPACE = " "
TAB = "\t"
RETURN = "\r"
NEWLINE = "\n"
CARRIAGE_RETURN = "\r\n"
SPACES = [SPACE, TAB, RETURN, NEWLINE, CARRIAGE_RETURN]


def lex(string):
    assert type(string) == str
    symbols = []
    for c in string:
        if c in SPACES:
            continue
