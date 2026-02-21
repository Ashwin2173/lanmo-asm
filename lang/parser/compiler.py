import struct

from lang.lexer.word import Word
from lang.lexer.tokentype import TokenType
from lang.parser.opcodetype import OpCodeType
from exceptions import LanmoSyntaxError

MAGIC = 2273
MAJOR_VERSION = 1
MINOR_VERSION = 1

def compile(tokens: list[Word]) -> bytearray:
    symbol_table = bytearray()
    program_code = bytearray()
    tokens = tokens_iter(tokens)
    try:
        for token in tokens:
            token_type = token.get_type()
            if token_type == TokenType.K_PUSH:
                value: Word = next(tokens)
                expect_token(value, TokenType.INTEGER)
                index = len(symbol_table)
                symbol_table += struct.pack("<i", int(value.get_raw()))
                program_code += struct.pack("<BH", get_opcode(token), index)
            else:
                raise LanmoSyntaxError(token, "Unknown token or Unhandled opCode")
    except StopIteration:
        raise LanmoSyntaxError(None, "Missing <EOF>")
    return pack_byte_code(symbol_table, program_code)

def get_opcode(token: Word) -> int:
    return OpCodeType[token.get_raw()].value

def expect_token(token: Word, token_type: TokenType) -> None:
    if token.get_type() != token_type:
        raise LanmoSyntaxError(token, f"Expected {token_type}, but got {token.get_type()}")

def tokens_iter(tokens: list[Word]):
    for token in tokens:
        yield token

def pack_byte_code(symbol_table: bytearray, program_code: bytearray) -> bytearray:
    final_byte_code = bytearray()
    final_byte_code += get_header()
    final_byte_code += struct.pack("<I", len(symbol_table))
    final_byte_code += symbol_table
    final_byte_code += struct.pack("<I", len(program_code))
    final_byte_code += program_code
    return final_byte_code

def get_header() -> bytearray:
    return struct.pack("<IHH", MAGIC, MAJOR_VERSION, MINOR_VERSION)
