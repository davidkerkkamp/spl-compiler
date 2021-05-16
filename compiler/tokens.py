from enum import Enum, auto
from compiler.utils import CodeRange


class TokenType(Enum):
    OPERATOR = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    PAREN_OPEN = auto()  # (
    PAREN_CLOSE = auto()  # )
    CURLY_OPEN = auto()  # {
    CURLY_CLOSE = auto()  # }
    BLOCK_OPEN = auto()  # [
    BLOCK_CLOSE = auto()  # ]
    INT = auto()
    CHAR = auto()
    STRING = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    DOUBLECOLON = auto()
    ARROW = auto()
    EOF = auto()
    UNEXPECTED = auto()


class Token:
    def __init__(self, token_type: TokenType, value: str, code_range: CodeRange = None):
        self.token_type = token_type
        self.value = value
        self.code_range = code_range