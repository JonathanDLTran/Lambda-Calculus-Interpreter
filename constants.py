OPEN_PAREN = "("
CLOSE_PAREN = ")"
OPEN_BRACKET = "["
CLOSE_BRACKET = "]"
BRACES = [
    OPEN_PAREN,
    CLOSE_PAREN,
]
QUOTATION_MARK = '\"'
TICK = "'"
BACKTICK = "`"
AT = "@"
COMMA = ","

INFIX_MARKER = "$"

DOT = "."

COMMENT = ";"
NEWLINE = "\n"
CARRIAGE_RETURN = "\r\n"
NEWLINE_CHARS = "\r\n"

SPACE = " "
TRUE = "#t"
FALSE = "#f"
ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"
EXP = "**"
CONCAT = "^"
PRINTLN = "println"
SET = "set!"
EQ = "eq?"
QUOTE = "quote"
UNQUOTE = "unquote"
QUASIQUOTE = "quasiquote"
UNQUOTE_SPLICING = "unquote-splicing"
LIST = "list"
IF = "if"
LET = "let"
LETSTAR = "let*"
AND = "and"
OR = "or"
NOT = "not"
BEGIN = "begin"
CONS = "cons"
CAR = "car"
CDR = "cdr"
DEFINE = "define"
LAMBDA = "lambda"
FOR = "for"
FORLIST = "for/list"
DEFINE_MACRO = "define-macro"
APPLY = "apply"
MAP = "map"
LT = "lt?"
GT = "gt?"
LTE = "lte?"
GTE = "gte?"
NEQ = "neq?"
COND = "cond"
ELSE = "else"
DELAY = "delay"
FORCE = "force"
CONS_STREAM = "cons-stream"
CDR_STREAM = "cdr-stream"
VARIADIC = "variadic"
APPEND = "append"
NIL = "nil"
MATCH = "match"  # very basic match
UNDERSCORE = "_"

PREPARSE_SYMBOLS_MAP = {
    TICK: QUOTE,
    BACKTICK: QUASIQUOTE,
    AT: UNQUOTE_SPLICING,
    COMMA: UNQUOTE
}
