import os
import sys

from lang.lexer.tokenizer import tokenize

def read_program_file(args: list[str]) -> str:
    program_file = None
    for arg in args:
        if arg.endswith(".lm"):
            program_file = open(arg, 'r')
            break
    return None if program_file is None else program_file.read()

def main(args: list[str]) -> None:
    program = read_program_file(args)
    if program is None:
        print("[ERROR] Required a .lm for running")
        sys.exit(1)
    tokens = tokenize(program)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main(sys.argv)