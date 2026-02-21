from enum import Enum 

class OpCodeType(Enum):
    PUSH = 1
    POP = 2
    ADD = 3
    PEEK = 4
    HALT = 5