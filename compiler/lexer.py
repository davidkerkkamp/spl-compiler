from compiler.errors import UnexpectedCharError
from compiler.tokens import *
from compiler.utils import CodePosition, CodeRange, InputHandler
import re


class Lexer:
    def __init__(self, max_errors=5):
        self.input_text = InputHandler.input_text
        self.tokens = []
        self.lex_position = CodePosition(1, 1)
        self.lex_errors = []
        self.lex_index = 0
        self.keywords = ['True', 'False', 'if', 'else', 'while', 'return', 'var', 'Int', 'Bool', 'Char', 'Void']
        self.brackets = {
            '(': TokenType.PAREN_OPEN, ')': TokenType.PAREN_CLOSE,
            '{': TokenType.CURLY_OPEN, '}': TokenType.CURLY_CLOSE,
            '[': TokenType.BLOCK_OPEN, ']': TokenType.BLOCK_CLOSE
        }
        self.max_errors = max_errors
        self.token_match_rules = [  # (Token or lambda, regex)
            (TokenType.INT, r'([1-9][0-9]*)|0+'),  # Integers
            (lambda match: TokenType.KEYWORD  # Identifiers and keywords
                if match in self.keywords else TokenType.IDENTIFIER, r'[_]*[a-zA-Z][a-zA-Z0-9_]*'),
            (lambda match: self.brackets.get(match), r'[(){}\[\]]'),  # Brackets
            (TokenType.SEMICOLON, r';'),  # Semicolon
            (TokenType.COMMA, r','),  # Comma
            (TokenType.DOT, r'\.'),  # Dot
            (TokenType.DOUBLECOLON, r'::'),  # Doublecolon
            (TokenType.ARROW, r'->'),  # Arrow
            (TokenType.OPERATOR, r'==|<=|>=|!=|&&|[|][|]|(:(?!:))|(-(?!>))|[+*%<>=!/]'),  # Operators
            (TokenType.CHAR, r'[\'](.|([\\][n]))[\']'),  # Characters
            (TokenType.STRING, r'["]((?!["])(.|[\n]))*["]')  # String
        ]

    def skip_whitespaces_comments(self):
        remaining_input = self.get_remaining_input()
        if len(remaining_input) == 0:
            return
        if m := re.match(r'[ \t]+', remaining_input):  # Skip whitespaces and tabs
            self.increase_lex_index(m.end())
            return self.skip_whitespaces_comments()
        elif m := re.match(r'([\n]|(//(.*)[\n]?))', remaining_input):  # Match single line comment and newlines
            self.increase_lex_index(m.end())
            self.move_code_position()
            return self.skip_whitespaces_comments()
        elif m := re.match(r'[/][*]((?![*]/)(.|\n))*([*]/)?', remaining_input):  # Match multiline comments
            newlines = [n.start() for n in re.finditer('\n', m.group())]
            self.increase_lex_index(m.end())
            self.move_code_position(line_incr=len(newlines), set_column=m.end() - (newlines[-1] if newlines else 0))
            return self.skip_whitespaces_comments()

    def lex_input(self):
        while True:
            token: Token = self.lex_next()
            self.tokens.append(token)
            if token.token_type == TokenType.EOF:
                break
            elif token.token_type == TokenType.UNEXPECTED:
                self.lex_errors.append(UnexpectedCharError(token.code_range, token.value))
                if len(self.lex_errors) >= self.max_errors:
                    break
        return self.tokens

    def lex_next(self):
        self.skip_whitespaces_comments()
        start_position = CodePosition.from_code_position(self.lex_position)
        remaining_input = self.get_remaining_input()
        if len(remaining_input) == 0:  # Done lexing
            end_pos = CodePosition.from_code_position(self.lex_position)
            end_pos.column+=1
            return self.create_token(TokenType.EOF, '',
                                     CodeRange(start_position, end_pos))

        for i, (t, r) in enumerate(self.token_match_rules):
            assert isinstance(t, TokenType) or callable(t)
            if m := re.match(r, remaining_input):
                self.increase_lex_index(m.end())
                code_range = CodeRange(start_position, CodePosition.from_code_position(self.lex_position))

                if callable(t):  # If t is a lambda, call it with the matched string, else return t as token type
                    return self.create_token(t(m.group()), m.group(), code_range)
                return self.create_token(t, m.group(), code_range)

        # If nothing matched, return unexpected token
        self.increase_lex_index(1)
        return self.create_token(TokenType.UNEXPECTED, remaining_input[0],
                                 CodeRange(start_position, CodePosition.from_code_position(self.lex_position)))

    @staticmethod
    def create_token(token_type: TokenType, value: str, code_range: CodeRange):
        return Token(token_type, re.sub("['\"]", "", value), code_range)  # Strip single/double quotes (char)

    def increase_lex_index(self, n):
        self.lex_index += n
        self.lex_position.increment_column(n)

    def get_remaining_input(self):
        return self.input_text[self.lex_index:] if self.lex_index < len(self.input_text) else ''

    def move_code_position(self, line_incr=1, set_column=1):
        self.lex_position.increment_line(line_incr)
        self.lex_position.set_column(set_column)