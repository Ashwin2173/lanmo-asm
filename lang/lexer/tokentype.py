from enum import Enum

class TokenType(Enum):
    COMMENT = "COMMENT"
    IDENTIFIER = "IDENTIFIER"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    DOT_OPERATOR = "DOT_OPERATOR"
    NEWLINE = "NEWLINE"

    K_PUSH = "PUSH"