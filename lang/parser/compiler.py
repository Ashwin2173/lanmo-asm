import struct

from lang.lexer.word import Word
from lang.lexer.tokentype import TokenType
from lang.parser.opcodetype import OpCodeType
from exceptions import LanmoSyntaxError

MAGIC = 2273
MAJOR_VERSION = 1
MINOR_VERSION = 0

SINGLE_OPCODES = {
    TokenType.K_ADD,
    TokenType.K_PEEK,
    TokenType.K_POP,
    TokenType.K_HALT
}

class Compiler:
    def __init__(self, tokens: list[Word]):
        self.tokens = tokens_iter(tokens)
        self.constant_table = bytearray()
        self.execution_code = bytearray()
        self.constant_lookup = dict()

    def compile(self) -> bytearray:
        try:
            for token in self.tokens:
                token_type = token.get_type()
                if token_type == TokenType.K_EOF: 
                    break
                elif token_type == TokenType.K_PUSH:
                    self.__parse_push(token)
                elif token_type in SINGLE_OPCODES:
                    self.execution_code += struct.pack("<B", get_opcode(token))
                else:
                    raise LanmoSyntaxError(token, "Unknown token or Unhandled opCode")
        except StopIteration:
            raise LanmoSyntaxError(None, "Missing <EOF>")
        return self.__pack_byte_code()
    
    def __parse_push(self, token: Word) -> None:
        value: Word = next(self.tokens)
        expect_token(value, TokenType.INTEGER)
        raw_value = value.get_raw()
        index = self.constant_lookup.get(raw_value, len(self.constant_table))
        if index == len(self.constant_table):
            self.constant_table += struct.pack("<i", int(raw_value))
            self.constant_lookup[raw_value] = index
        self.execution_code += struct.pack("<BH", get_opcode(token), index)

    def __pack_byte_code(self) -> bytearray:
        final_byte_code = bytearray()
        final_byte_code += get_header()
        final_byte_code += struct.pack("<I", len(self.constant_table))
        final_byte_code += self.constant_table
        final_byte_code += struct.pack("<I", len(self.execution_code))
        final_byte_code += self.execution_code
        return final_byte_code

def get_opcode(token: Word) -> int:
    return OpCodeType[token.get_raw()].value

def expect_token(token: Word, token_type: TokenType) -> None:
    if token.get_type() != token_type:
        raise LanmoSyntaxError(token, f"Expected {token_type}, but got {token.get_type()}")

def tokens_iter(tokens: list[Word]):
    for token in tokens:
        yield token

def get_header() -> bytearray:
    return struct.pack("<IHH", MAGIC, MAJOR_VERSION, MINOR_VERSION)
