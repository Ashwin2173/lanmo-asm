from enum import Enum, auto

class OpCodeType(Enum):
    PUSH = auto()
    POP = auto()
    ADD = auto()
    PEEK = auto()
    CALL = auto()
    HALT = auto()
    RET = auto()