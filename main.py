import sys

from lang.lexer.tokenizer import tokenize
from lang.parser.compiler import compile
from exceptions import LanmoSyntaxError

def read_program_file(args: list[str]) -> tuple[str, str]:
    for arg in args:
        if arg.endswith(".lm"):
            return open(arg, 'r').read(), arg
    return None, None

def get_error_token_format(e: LanmoSyntaxError, program: str) -> str:
    line = e.token.get_line() - 1
    raw = e.token.get_raw()
    program_lines = program.splitlines()
    raw_line = program_lines[line]
    size = len(e.token.get_raw())
    previous_line = "" if line <= 0 else program_lines[line - 1]
    prefix = f"  > {line + 1}: "
    previous_line = f"    {line}: " + previous_line if len(previous_line) != 0 else ""
    return f"{previous_line}\n{prefix}{raw_line}\n{' ' * (len(prefix) + raw_line.find(raw))}{'^' * size}"

def main(args: list[str]) -> None:
    program, path = read_program_file(args)
    if program is None:
        print("[ERROR] Required a .lm for running")
        sys.exit(1)
    tokens = tokenize(program)
    byte_code_file = f"{path[:-3]}.lbc"
    with open(byte_code_file, 'wb') as byte_code_file:
        try:
            byte_code_file.write(compile(tokens))
        except LanmoSyntaxError as e:
            print(f"file: {path}")
            if e.token is not None:
                print(get_error_token_format(e, program))
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main(sys.argv)