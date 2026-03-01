import sys

from lang.asm.asmbler import Asmbler
from lang.dis.disasm import Disasm

program_args = set()

def read_program_file(args: list[str]) -> tuple[str, str]:
    ret_value = None, None
    for arg in args:
        if arg.endswith(".lm"):
            ret_value = open(arg, 'r').read(), arg
        elif arg.endswith(".lmc"):
            ret_value = open(arg, 'rb').read(), arg
        elif arg.startswith("--"):
            program_args.add(arg)
    return ret_value

def main(args: list[str]) -> None:
    program, path = read_program_file(args)
    if "--version" in program_args:
        print("LANMO 1.0 written in python")
        sys.exit(0)
    elif program is None or "--help" in program_args:
        print("USAGE:")
        print("    lasm [OPTIONS] [PROGRAM_PATH]")
        print("OPTIONS:") 
        print("    --dis       Disasmble bytecode to program")
        print("    --help      Prints this usage")
        print("    --version   prints the version")
        sys.exit(0)
    elif "--dis" in program_args:
        if not path.endswith("lmc"):
            print("[ERROR] Required .lmc file for disasmbling")
            sys.exit(1)
        disasmbler = Disasm(program)
        print(disasmbler.disasmble())
        sys.exit(0)
    else:
        if not path.endswith("lm"):
            print("[ERROR] Required .lm file for compiling")
            exit(1)
        asmbler = Asmbler(program, path)
        asmbler.asmble()
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)