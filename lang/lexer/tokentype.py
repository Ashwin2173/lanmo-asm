from enum import Enum

class TokenType(Enum):
    COMMENT = "COMMENT"
    IDENTIFIER = "IDENTIFIER"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"
    NEWLINE = "NEWLINE"

    OPEN_BRACE = "OPEN_BRACE"
    CLOSE_BRACE = "CLOSE_BRACE"

    K_PUSH = "PUSH"
    K_POP = "POP"
    K_ADD = "ADD"
    K_PEEK = "PEEK"
    K_HALT = "HALT"
    K_EOF = "EOF"
    K_RET = "RET"