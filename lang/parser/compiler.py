import struct

from lang.lexer.word import Word
from lang.lexer.tokentype import TokenType
from lang.parser.opcodetype import OpCodeType
from lang.parser.datatype import DataType
from exceptions import LanmoSyntaxError

MAGIC = 2273
MAJOR_VERSION = 1
MINOR_VERSION = 0

SINGLE_OPCODES = {
    TokenType.K_ADD,
    TokenType.K_PEEK,
    TokenType.K_POP,
    TokenType.K_HALT,
    TokenType.K_RET
}

class Compiler:
    def __init__(self, tokens: list[Word]):
        self.tokens = tokens_iter(tokens)
        self.constant_table = bytearray()
        self.function_table = bytearray()
        self.constant_lookup = dict()

    def compile(self) -> bytearray:
        try:
            for token in self.tokens:
                if token.get_type() == TokenType.K_EOF:
                    break
                elif token.get_type() == TokenType.IDENTIFIER:
                    self.__parse_function(token)
                else:
                    raise LanmoSyntaxError(token, "Unknown token out of function")
        except StopIteration:
            raise LanmoSyntaxError(None, "Missing <EOF>")
        return self.__pack_byte_code()

    def __parse_function(self, token: Word) -> None:
        name_index = self.__add_constant(token)
        function_code = bytearray()
        max_stack_size = 255
        expect_token(next(self.tokens), TokenType.OPEN_BRACE)
        for token in self.tokens:
            token_type = token.get_type()
            if token_type == TokenType.CLOSE_BRACE: 
                break
            elif token_type == TokenType.K_PUSH:
                self.__parse_push(token, function_code)
            elif token_type in SINGLE_OPCODES:
                function_code += struct.pack("<B", get_opcode(token))
            else:
                raise LanmoSyntaxError(token, "Unknown token or Unhandled opCode")
        function = bytearray()
        function += struct.pack("<I", name_index)
        function += struct.pack("<I", 0)     # args count
        function += struct.pack("<I", 0)     # local count 
        function += struct.pack("<I", max_stack_size)
        function += struct.pack("<I", len(function_code))
        function += function_code
        self.function_table += struct.pack("<I", len(function))
    
    def __parse_push(self, token: Word, execution_code: bytearray) -> None:
        value: Word = next(self.tokens)
        index = self.__add_constant(value)
        execution_code += struct.pack("<BH", get_opcode(token), index)

    def __add_constant(self, token: Word) -> int:
        raw_value = token.get_raw()
        index = self.constant_lookup.get(raw_value, len(self.constant_table))
        if index == len(self.constant_table):
            if token.get_type() == TokenType.INTEGER:
                self.constant_table += struct.pack("<Bi", DataType.INTEGER.value, int(raw_value))
            elif token.get_type() == TokenType.IDENTIFIER:
                word = token.get_raw()
                self.constant_table += struct.pack("<B", DataType.STRING.value)
                self.constant_table += struct.pack(f"<I{len(word)}s", len(word), word.encode('utf-8'))
            elif token.get_type() == TokenType.STRING:
                string_value = token.get_raw()[1:-1]
                self.constant_table += struct.pack("<B", DataType.STRING.value)
                self.constant_table += struct.pack(f"<I{len(string_value)}s", len(string_value), string_value.encode('utf-8'))
            else:
                raise LanmoSyntaxError(token, f"Expected CONSTANT; got {token.get_type().value}")
        return index

    def __pack_byte_code(self) -> bytearray:
        final_byte_code = bytearray()
        final_byte_code += get_header()
        final_byte_code += struct.pack("<I", len(self.constant_table))
        final_byte_code += self.constant_table
        final_byte_code += struct.pack("<I", len(self.function_table))
        final_byte_code += self.function_table
        return final_byte_code

def get_opcode(token: Word) -> int:
    return OpCodeType[token.get_raw()].value

def expect_token(token: Word, token_type: TokenType) -> None:
    if token.get_type() != token_type:
        raise LanmoSyntaxError(token, f"Expected {token_type}, but got {token.get_type().value}")

def tokens_iter(tokens: list[Word]):
    for token in tokens:
        yield token

def get_header() -> bytearray:
    return struct.pack("<IHH", MAGIC, MAJOR_VERSION, MINOR_VERSION)
