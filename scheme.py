
from eval import eval_expr, frontend, expr_to_str


import sys
import os.path


def file_evaluator(file_name):
    fp = open(file_name, "r")
    s = fp.read()
    fp.close()

    context = {}
    try:
        eval_expr(frontend(s), context, False)
    except:
        print("Error")
        exit(1)
    exit(0)


def interpreter():
    context = {}
    try:
        while(True):
            expr_string = input("> ")
            expr_string = expr_string.strip()
            if expr_string.lower() == "quit":
                print("\tExiting Interpreter...")
                return
            elif expr_string.lower() == "reset-context":
                print("\tResetting Interpreter Context...")
                print("\n")
                context = {}
                continue
            try:
                value = expr_to_str(
                    eval_expr(frontend(expr_string), context, False))
                print(value)
                print("\n")
            except:
                print("Error")
                print("\n")
    except KeyboardInterrupt:
        print("\tExiting Interpreter...")
        return


def main():
    args = sys.argv[1:]
    if args == []:
        print("\t----- Scheme Interpreter -----")
        interpreter()
        exit(0)
    elif args[0] == "--help":
        print("\tUsage: python3 scheme.py [file.scm]")
        exit(0)
    elif len(args) == 1:
        file_name = args[0]
        if not os.path.exists(file_name):
            print(f"\tNo Path to File {file_name}.")
            exit(0)
        file_evaluator(file_name)
        exit(0)
    else:
        print(f"\tToo Many Arguments: {args}")
        exit(0)


if __name__ == "__main__":
    main()
