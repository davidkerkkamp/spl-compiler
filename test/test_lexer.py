import unittest
from compiler.lexer import Lexer, TokenType, Token


# TODO More tests
class LexerTests(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def expected_token_len(self, tokens, num):
        self.assertEqual(len(tokens), num, f'Token list should contain {num} token(s)')

    def expected_token(self, token: Token, token_type: TokenType, token_value: str):
        self.assertEqual(token.token_type, token_type, f'Token should be type {token_type}')
        self.assertEqual(token.value, token_value, f'Token should have value "{token_value}"')

    def test_lex_empty(self):
        self.lexer.input_text = ''
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 1)
        self.assertEqual(tokens[0].token_type, TokenType.EOF, 'Only token should be EOF token')

    def test_lex_whitespaces(self):
        self.lexer.input_text = '  \t     5          60 '
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 3)
        self.expected_token(tokens[0], TokenType.INT, '5')
        self.expected_token(tokens[1], TokenType.INT, '60')

    def test_lex_comments(self):
        self.lexer.input_text = '// Single line comment \n 1 /* multi line \n still comment \t  ccccc \n */ 2 /* to end'
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 3)
        self.expected_token(tokens[0], TokenType.INT, '1')
        self.expected_token(tokens[1], TokenType.INT, '2')

    def test_lex_brackets(self):
        self.lexer.input_text = '[]{}()'
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 7)
        self.expected_token(tokens[0], TokenType.BLOCK_OPEN, '[')
        self.expected_token(tokens[1], TokenType.BLOCK_CLOSE, ']')
        self.expected_token(tokens[2], TokenType.CURLY_OPEN, '{')
        self.expected_token(tokens[3], TokenType.CURLY_CLOSE, '}')
        self.expected_token(tokens[4], TokenType.PAREN_OPEN, '(')
        self.expected_token(tokens[5], TokenType.PAREN_CLOSE, ')')

    def test_lex_punctuation(self):
        self.lexer.input_text = '.,;'
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 4)
        self.expected_token(tokens[0], TokenType.DOT, '.')
        self.expected_token(tokens[1], TokenType.COMMA, ',')
        self.expected_token(tokens[2], TokenType.SEMICOLON, ';')

    def test_lex_fun_decl(self):
        self.lexer.input_text = '::   ->'
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 3)
        self.expected_token(tokens[0], TokenType.DOUBLECOLON, '::')
        self.expected_token(tokens[1], TokenType.ARROW, '->')

    def test_lex_operators(self):
        self.lexer.input_text = ': : - > <+*/==<=!>= > = != ! = &&||%'
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 21)
        self.expected_token(tokens[0], TokenType.OPERATOR, ':')
        self.expected_token(tokens[1], TokenType.OPERATOR, ':')
        self.expected_token(tokens[2], TokenType.OPERATOR, '-')
        self.expected_token(tokens[3], TokenType.OPERATOR, '>')
        self.expected_token(tokens[4], TokenType.OPERATOR, '<')
        self.expected_token(tokens[5], TokenType.OPERATOR, '+')
        self.expected_token(tokens[6], TokenType.OPERATOR, '*')
        self.expected_token(tokens[7], TokenType.OPERATOR, '/')
        self.expected_token(tokens[8], TokenType.OPERATOR, '==')
        self.expected_token(tokens[9], TokenType.OPERATOR, '<=')
        self.expected_token(tokens[10], TokenType.OPERATOR, '!')
        self.expected_token(tokens[11], TokenType.OPERATOR, '>=')
        self.expected_token(tokens[12], TokenType.OPERATOR, '>')
        self.expected_token(tokens[13], TokenType.OPERATOR, '=')
        self.expected_token(tokens[14], TokenType.OPERATOR, '!=')
        self.expected_token(tokens[15], TokenType.OPERATOR, '!')
        self.expected_token(tokens[16], TokenType.OPERATOR, '=')
        self.expected_token(tokens[17], TokenType.OPERATOR, '&&')
        self.expected_token(tokens[18], TokenType.OPERATOR, '||')
        self.expected_token(tokens[19], TokenType.OPERATOR, '%')

    def test_lex_char(self):
        self.lexer.input_text = "a'b'c '\n' '\t'"
        tokens = self.lexer.lex_input()
        self.expected_token_len(tokens, 6)
        self.expected_token(tokens[0], TokenType.IDENTIFIER, 'a')
        self.expected_token(tokens[1], TokenType.CHAR, 'b')
        self.expected_token(tokens[2], TokenType.IDENTIFIER, 'c')
        self.expected_token(tokens[3], TokenType.CHAR, '\n')
        self.expected_token(tokens[4], TokenType.CHAR, '\t')

if __name__ == '__main__':
    unittest.main()
