from token_constants import *


def lex(string):
    """
    Lexes string into list of tokens,.
    """
    string = string.strip()
    parens_str = string.replace(LEFT_PAREN, f" {LEFT_PAREN} ")
    parens_str = parens_str.replace(RIGHT_PAREN, f" {RIGHT_PAREN} ")
    for op in BINOPS:
        parens_str = parens_str.replace(op, f" {op} ")
    split_str = parens_str.split()
    final_lst = []
    for s in split_str:
        s = s.strip()
        try:
            f = float(s)
            final_lst.append(f)
        except Exception:
            final_lst.append(str(s))
    return final_lst


def test():
    s = "3+4"
    l = lex(s)
    print(l)


if __name__ == "__main__":
    test()
