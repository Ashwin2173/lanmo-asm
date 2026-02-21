from lang.lexer.tokentype import TokenType

class Word:
    def __init__(self, w_raw: str, w_type: TokenType, w_line: int, w_span: tuple[int, int]):
        self.w_raw = w_raw
        self.w_type = w_type
        self.w_line = w_line
        self.w_span = w_span

    def get_raw(self) -> str:
        return self.w_raw
    
    def get_type(self) -> str:
        return self.w_type

    def get_line(self) -> int:
        return self.w_line
    
    def get_span(self) -> tuple[int, int]:
        return self.w_span
    
    def __str__(self):
        return f"{self.w_type} '{self.w_raw}' at line: {self.w_line}"
