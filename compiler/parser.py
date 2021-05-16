from collections import deque

from compiler.AST.base import Error, Text, Expr, Statement
from compiler.AST.spl_file import SPLFile
from compiler.AST.declarations import FunArgNames, VarDecl, FunDecl
from compiler.AST.expressions import BinaryOpType, UnaryOpType, Op, UnaryOp, ConstNumber, ConstChar, ConstBool, \
    FieldExpr, EmptyList, Tuple, FunctionCall
from compiler.AST.fields import Variable, Accessor, FieldType
from compiler.AST.statements import Block, If, While, Assign, Return, BlockStatement, DeclWrapper, \
    ExprWrapper
from compiler.AST.types import IntType, BoolType, CharType, TypeVarType, ListType, ValueReturn, VoidReturn, FunArgs, \
    FunctionType
from typing import Callable, List
from compiler.errors import *
from compiler.logging import Logger
from compiler.tokens import Token, TokenType


class ParseError(Exception):
    pass


class TokenReader:
    def __init__(self, tokens: List[Token]):
        self.tokens: deque[Token] = deque(tokens)
        self.current = None
        self.pop_next()
        self.block_depth: int = 0

    def pop_next(self):
        try:
            self.current = self.tokens.popleft()
        except IndexError:
            raise Exception('No tokens to pop from queue')

    def current_token_type(self):
        return self.current.token_type

    def current_token_val(self):
        return self.current.value

    def current_code_range(self):
        return self.current.code_range

    def read_if(self, f: Callable[[Token], bool]):
        current = self.current
        if f(current):
            self.pop_next()
            self.check_block_depth(current)
            return current
        else:
            return None

    def read_if_keyword(self, keyword: str):
        return self.read_if(lambda t: t.token_type == TokenType.KEYWORD and t.value == keyword)

    def read(self):
        return self.read_if(lambda t: True)

    def require(self, f: Callable[[Token], bool]):
        token = self.read_if(f)
        if token is None:
            raise ParseError('Unexpected token')
        return token

    def require_type(self, token_type: TokenType):
        return self.require(lambda t: t.token_type == token_type)

    def require_keyword(self, keyword: str):
        return self.require(lambda t: t.token_type == TokenType.KEYWORD and t.value == keyword)

    def check_block_depth(self, current: Token):
        if current.token_type == TokenType.CURLY_OPEN:
            self.block_depth += 1
        elif current.token_type == TokenType.CURLY_CLOSE:
            self.block_depth -= 1

    def move_context_up(self, depth = 1):
        current_depth = self.block_depth
        while self.block_depth > current_depth - depth:
            self.read()

    def skip_to(self, token: Token, including_last=False):
        while (self.current_token_type() != token.token_type or self.current_token_val() != token.value) \
                and self.current_token_type() != TokenType.EOF:
            self.read()
        if including_last:
            self.read()

    def skip_to_semicolon(self):
        self.skip_to(Token(TokenType.SEMICOLON, ';'), False)


class Parser:
    def __init__(self, token_reader: TokenReader):
        self.errors: List[ParserError] = []
        self.tr: TokenReader = token_reader

    def parse_spl(self):
        decls = []
        while self.tr.current_token_type() is not TokenType.EOF:
            if len(self.errors) > 5:
                print('Abort parsing: too many errors')
                break
            try:
                decl = self.parse_decl()
                decls.append(decl)
            except:
                print(f'### Error at\n{self.tr.current_code_range()}')
                break
        return SPLFile(decls)

    def parse_semicolon(self):
        try:
            self.tr.require_type(TokenType.SEMICOLON)
        except:  # Assume semicolon is missing, continue parsing
            self.errors.append(MissingSemicolonError(self.tr.current_code_range()))

    # ****************************** DECLARATIONS ******************************

    def parse_decl(self):
        if self.tr.current_token_type() == TokenType.IDENTIFIER:
            return self.parse_fun_decl()
        else:
            return self.parse_var_decl()

    def parse_fun_decl(self):
        try:
            token = self.tr.require_type(TokenType.IDENTIFIER)
        except:
            self.errors.append(ExpectedIdentError(self.tr.current))
            raise ParseError()
        name = Text(token.value).with_code_range(token.code_range)

        def parse_args():
            args = []
            while self.tr.current_token_type() != TokenType.PAREN_CLOSE:
                if len(args) > 0:
                    try:
                        self.tr.require_type(TokenType.COMMA)
                    except:
                        self.errors.append(ExpectedSymbolError(',', self.tr.current))
                        raise ParseError()
                try:
                    t = self.tr.require_type(TokenType.IDENTIFIER)
                except:
                    self.errors.append(ExpectedIdentError(self.tr.current))
                    raise ParseError()
                args.append(Text(t.value).with_code_range(t.code_range))
            return FunArgNames(args)

        args = self.parse_balanced_brackets(
            Token(TokenType.PAREN_OPEN, '('), parse_args, Token(TokenType.PAREN_CLOSE, ')'))
        if self.tr.current_token_type() == TokenType.DOUBLECOLON:
            self.tr.read()
            fun_type = self.parse_fun_type()
        else:
            fun_type = None
        block = self.parse_block()
        try:
            assert isinstance(block, Error) or len(block.statements) > 0
        except:
            self.errors.append(EmptyFunctionBodyError(name.value, name.code_range))
        return FunDecl(name, args, fun_type, block, None).with_code_range(name.code_range)

    def parse_var_decl(self, id_token: Token = None):
        start = self.tr.current_code_range().start if id_token is None else id_token.code_range
        if id_token is None and (self.tr.read_if_keyword('var')) is not None:
            var_type = None
        else:
            var_type = self.parse_type(id_token)
        try:
            id_token = self.tr.require_type(TokenType.IDENTIFIER)
            ident = Text(id_token.value).with_code_range(id_token.code_range)
        except:
            self.errors.append(ExpectedIdentError(self.tr.current))
            raise ParseError()
        try:
            self.tr.require(lambda t: t.token_type == TokenType.OPERATOR and t.value == '=')
        except:
            self.errors.append(ExpectedSymbolError('=', self.tr.current))
            raise ParseError()
        expr = self.parse_expr()
        code_range = CodeRange(start, expr.code_range.end)
        self.parse_semicolon()
        return VarDecl(var_type, ident, expr).with_code_range(code_range)

    # ****************************** TYPES ******************************

    def parse_type(self, type_token: Token = None):
        current = self.tr.current if type_token is None else type_token
        if current.token_type == TokenType.BLOCK_OPEN:  # List type
            return ListType(self.parse_balanced_brackets(current, self.parse_type, Token(TokenType.BLOCK_CLOSE, ']')))\
                .with_code_range(current.code_range)
        elif current.token_type == TokenType.PAREN_OPEN:  # Tuple type
            def f():
                try:
                    t1 = self.parse_type()
                except:
                    self.tr.skip_to(Token(TokenType.COMMA, ','))  # Skip to comma for error recovery
                    t1 = Error()
                self.tr.require_type(TokenType.COMMA)
                t2 = self.parse_type()
                code_range = CodeRange(t1.code_range.start, t2.code_range.end)
                return Tuple(t1, t2).with_code_range(code_range)

            return self.parse_balanced_brackets(current, f, Token(TokenType.PAREN_CLOSE, ')'))
        elif current.token_type == TokenType.IDENTIFIER:  # Type var
            if type_token is None:
                self.tr.read()
            return TypeVarType(current.value, None).with_code_range(current.code_range)
        else:
            if type_token is None:
                self.tr.read()
            return self.parse_basic_type(current)

    def parse_basic_type(self, type_token: Token = None):
        current = self.tr.read() if type_token is None else type_token
        if current.token_type == TokenType.KEYWORD:
            t = {'Int': IntType(),
                 'Bool': BoolType(),
                 'Char': CharType()}.get(current.value)
            if t is not None:
                return t.with_code_range(current.code_range)
        self.errors.append(ExpectedTypeError(current))
        raise ParseError()

    def parse_fun_type(self):
        start = self.tr.current_code_range().start
        args = []
        try:
            while self.tr.current_token_type() != TokenType.ARROW:
                args.append(self.parse_type())
        except:
            args.append(Error())
            current = self.tr.current
            self.tr.skip_to(Token(TokenType.ARROW, '->'))  # when error, try skipping to arrow and continue parse
        try:
            self.tr.require_type(TokenType.ARROW)
        except:
            self.errors.append(ExpectedSymbolError('->', current))
            raise ParseError()
        return_type = self.parse_return_type()
        code_range = CodeRange(start, self.tr.current_code_range().end)
        return FunctionType(FunArgs(args), return_type).with_code_range(code_range)

    def parse_return_type(self):
        current = self.tr.current
        if current.token_type == TokenType.KEYWORD and current.value == 'Void':
            self.tr.read()
            return VoidReturn().with_code_range(current.code_range)
        else:
            try:
                t = self.parse_type()
            except:
                t = Error()
                self.tr.skip_to(Token(TokenType.CURLY_OPEN, '{'))  # try skipping to { and continue parsing
            return ValueReturn(t).with_code_range(CodeRange(current.code_range.start, self.tr.current_code_range().end))

    # ****************************** STATEMENTS ******************************

    def parse_statement(self) -> Statement:
        current = self.tr.current
        if current.token_type == TokenType.KEYWORD:
            if current.value == 'return':
                return self.parse_return()
            elif current.value == 'if':
                return self.parse_if()
            elif current.value == 'while':
                return self.parse_while()
            elif current.value in ['var', 'Bool', 'Int', 'Char']:
                var_decl = self.parse_var_decl()
                return DeclWrapper(var_decl).with_code_range(var_decl.code_range)
        if current.token_type in [TokenType.BLOCK_OPEN, TokenType.PAREN_OPEN]:
            var_decl = self.parse_var_decl()
            return DeclWrapper(var_decl).with_code_range(var_decl.code_range)
        elif current.token_type == TokenType.IDENTIFIER:
            return self.parse_identifier_statement()
        elif current.token_type == TokenType.CURLY_OPEN:
            block = self.parse_block()
            code_range = CodeRange(current.code_range.start, self.tr.current_code_range().end)
            return BlockStatement(block).with_code_range(code_range)
        else:
            self.errors.append(ExpectedStatementError(current))
            raise ParseError()

    def parse_return(self):
        t = self.tr.require_keyword('return')
        expr = None
        if self.tr.current_token_type() != TokenType.SEMICOLON:
            try:
                expr = self.parse_expr()
            except:
                expr = Error()
                self.tr.skip_to_semicolon()  # Skip to ; for error recovery and continue parsing
        code_range = CodeRange(t.code_range.start, self.tr.current_code_range().end)
        self.parse_semicolon()
        return Return(expr).with_code_range(code_range)

    def parse_if(self):
        t = self.tr.require_keyword('if')
        condition = self.parse_bracketed_expr(allow_tuple=False)  # Error is handled in parse_bracketed_expr
        then_block = self.parse_block()  # Error is handled in parse_block
        else_block = None
        if self.tr.read_if_keyword('else') is not None:
            else_block = self.parse_block()
        code_range = CodeRange(t.code_range.start, self.tr.current_code_range().end)
        return If(condition, then_block, else_block).with_code_range(code_range)

    def parse_while(self):
        t = self.tr.require_keyword('while')
        condition = self.parse_bracketed_expr(allow_tuple=False)
        body = self.parse_block()
        code_range = CodeRange(t.code_range.start, self.tr.current_code_range().end)
        return While(condition, body).with_code_range(code_range)

    def parse_identifier_statement(self):
        id_token = self.tr.require_type(TokenType.IDENTIFIER)
        if self.tr.current_token_type() == TokenType.PAREN_OPEN:  # Functional call
            call = self.parse_function_call(id_token)
            self.parse_semicolon()
            return ExprWrapper(call).with_code_range(call.code_range)
        elif self.tr.current_token_type() in [TokenType.DOT, TokenType.OPERATOR]:  # Assignment
            base_field = Variable(id_token.value).with_code_range(id_token.code_range)
            field = self.parse_field_accessor(base_field)
            try:
                op = self.tr.require(lambda t: t.token_type == TokenType.OPERATOR and t.value == '=')
            except:
                self.errors.append(ExpectedSymbolError('=', self.tr.current))
                raise ParseError()
            expr = self.parse_expr()
            self.parse_semicolon()
            code_range = CodeRange(id_token.code_range.start, self.tr.current_code_range().end)
            return Assign(field, expr).with_code_range(code_range)
        else:  # Var declaration with type var
            return DeclWrapper(self.parse_var_decl(id_token)).with_code_range(id_token.code_range)

    def parse_block(self):  # TODO order of var decls and stmts
        def f():
            start_range = self.tr.current_code_range()
            statements = []
            while self.tr.current_token_type() != TokenType.CURLY_CLOSE:
                stmt = self.parse_statement()
                statements.append(stmt)
            code_range = CodeRange(start_range.start, self.tr.current_code_range().end)
            return Block(statements).with_code_range(code_range)

        return self.parse_balanced_brackets(Token(TokenType.CURLY_OPEN, '{'), f, Token(TokenType.CURLY_CLOSE, '}'))

    # ****************************** EXPRESSIONS ******************************
    def parse_bin_op_expr(self, get_op: Callable, parse_next: Callable):
        result = parse_next()
        while self.tr.current_token_type() == TokenType.OPERATOR and \
                isinstance(op := get_op(self.tr.current_token_val()), BinaryOpType):
            self.tr.read()
            rhs = parse_next()
            code_range = CodeRange(result.code_range.start, rhs.code_range.end)
            result = Op(result, op, rhs).with_code_range(code_range)
        return result

    def parse_expr(self):
        return self.parse_bool_expr()

    def parse_bool_expr(self):
        return self.parse_bin_op_expr(
            lambda sym: {'&&': BinaryOpType.And, '||': BinaryOpType.Or}.get(sym, None),
            self.parse_comp_expr
        )

    def parse_comp_expr(self):
        return self.parse_bin_op_expr(
            lambda sym: {
                '==': BinaryOpType.Eq,
                '<': BinaryOpType.Lt,
                '>': BinaryOpType.Gt,
                '<=': BinaryOpType.Leq,
                '>=': BinaryOpType.Geq,
                '!=': BinaryOpType.Neq,
            }.get(sym, None),
            self.parse_list_expr
        )

    def parse_list_expr(self):
        lhs = self.parse_mod_expr()
        if self.tr.read_if(lambda t: t.token_type == TokenType.OPERATOR and t.value == ':') is not None:
            rhs = self.parse_list_expr()
            code_range = CodeRange(lhs.code_range.start, rhs.code_range.end)
            return Op(lhs, BinaryOpType.Cons, rhs).with_code_range(code_range)
        return lhs

    def parse_mod_expr(self):
        return self.parse_bin_op_expr(
            lambda sym: {'%': BinaryOpType.Mod}.get(sym, None),
            self.parse_sum
        )

    def parse_sum(self):
        return self.parse_bin_op_expr(
            lambda sym: {'+': BinaryOpType.Add, '-': BinaryOpType.Sub}.get(sym, None),
            self.parse_product
        )

    def parse_product(self):
        return self.parse_bin_op_expr(
            lambda sym: {'*': BinaryOpType.Mul, '/': BinaryOpType.Div}.get(sym, None),
            self.parse_unary_op
        )

    def parse_unary_op(self):
        ops = {'!': UnaryOpType.Neg, '-': UnaryOpType.Min}
        if isinstance(op := ops.get(self.tr.current_token_val(), None), UnaryOpType):
            start = self.tr.current.code_range.start
            self.tr.read()
            rhs = self.parse_unary_op()
            code_range = CodeRange(start, rhs.code_range.end)
            return UnaryOp(op, rhs).with_code_range(code_range)
        return self.parse_term()

    # PARSE TERMS

    def parse_identifier_expr(self):
        token = self.tr.require_type(TokenType.IDENTIFIER)
        if self.tr.current_token_type() == TokenType.PAREN_OPEN:
            return self.parse_function_call(token)
        base_field = Variable(token.value).with_code_range(token.code_range)
        field = self.parse_field_accessor(base_field)
        code_range = CodeRange(token.code_range.start, field.code_range.end)
        return FieldExpr(field).with_code_range(code_range)

    def parse_field_accessor(self, base_field: Variable):
        field = base_field
        while self.tr.current_token_type() == TokenType.DOT:
            dot = self.tr.require_type(TokenType.DOT)
            try:
                id = self.tr.require_type(TokenType.IDENTIFIER)
            except:
                self.errors.append(ExpectedIdentError(self.tr.current))
                raise ParseError()
            if id.value == 'fst':
                kind = FieldType.Fst
            elif id.value == 'snd':
                kind = FieldType.Snd
            elif id.value == 'hd':
                kind = FieldType.Hd
            elif id.value == 'tl':
                kind = FieldType.Tl
            else:
                self.errors.append(UnknownFieldError(id.value, id.code_range))
                raise ParseError()
            field = Accessor(kind, field).with_code_range(id.code_range)
        return field

    def parse_function_call(self, id_token: Token):
        def f():
            fargs = []
            while self.tr.current_token_type() != TokenType.PAREN_CLOSE:
                if len(fargs) > 0:
                    try:
                        self.tr.require_type(TokenType.COMMA)
                    except Exception as e:
                        self.errors.append(ExpectedSymbolError(',', self.tr.current))
                        raise e
                fargs.append(self.parse_expr())
            return FunctionCall(Text(id_token.value), fargs).with_code_range(id_token.code_range)

        return self.parse_balanced_brackets(
            Token(TokenType.PAREN_OPEN, '('), f, Token(TokenType.PAREN_CLOSE, ')'))

    def parse_number(self):
        token = self.tr.require_type(TokenType.INT)
        num = int(token.value)
        return ConstNumber(num).with_code_range(token.code_range)

        # if num <= 0x7FFFFFFF:  # Handle max 32-bit int
        #     return ConstNumber(num).with_code_range(token.code_range)
        # else:
        #     self.errors.append(NumberOverflowError(token))
        #     raise ParseError()

    def parse_bracketed_expr(self, allow_tuple: bool = True):
        def f():
            expr = self.parse_expr()
            if allow_tuple and self.tr.read_if(lambda t: t.token_type == TokenType.COMMA):
                expr2 = self.parse_expr()
                code_range = CodeRange(expr.code_range.start, expr2.code_range.end)
                return Tuple(expr, expr2).with_code_range(code_range)
            return expr

        return self.parse_balanced_brackets(
            Token(TokenType.PAREN_OPEN, '('), f, Token(TokenType.PAREN_CLOSE, ')'))

    def parse_string(self, string: str, code_range: CodeRange):
        # return Op(lhs, BinaryOpType.Cons, rhs).with_code_range(code_range)
        if len(string) == 0:
            return EmptyList().with_code_range(code_range)
        else:
            return Op(ConstChar(string[0]), BinaryOpType.Cons, self.parse_string(string[1:], code_range))\
                .with_code_range(code_range)

    def parse_term(self) -> Expr:
        tr = self.tr
        current = tr.current
        if current.token_type == TokenType.IDENTIFIER:
            return self.parse_identifier_expr()
        elif current.token_type == TokenType.INT:
            return self.parse_number()
        elif current.token_type == TokenType.CHAR:
            tr.read()
            return ConstChar(current.value).with_code_range(current.code_range)  # Char
        elif current.token_type == TokenType.STRING:
            tr.read()
            string = str.encode(current.value).decode('unicode_escape')
            return self.parse_string(string, current.code_range)
        elif current.token_type == TokenType.KEYWORD and (current.value == 'True' or current.value == 'False'):
            tr.read()
            b = True if current.value == 'True' else False
            return ConstBool(b).with_code_range(current.code_range)  # Boolean
        elif current.token_type == TokenType.PAREN_OPEN:  # Bracketed expression
            return self.parse_bracketed_expr()
        elif current.token_type == TokenType.BLOCK_OPEN:  # Empty list
            tr.read()
            try:
                close = tr.require_type(TokenType.BLOCK_CLOSE)
            except:
                close = tr.current
                self.errors.append(ExpectedSymbolError(']', close))
                raise ParseError()
            code_range = CodeRange(current.code_range.start, close.code_range.end)
            return EmptyList().with_code_range(code_range)
        else:
            self.errors.append(ExpectedTermError(current))
            raise ParseError()

    def parse_balanced_brackets(self, start: Token, f: Callable, end: Token):
        try:
            t1 = self.tr.require_type(start.token_type)
        except:
            self.errors.append(ExpectedSymbolError(start.value, self.tr.current))
            raise ParseError()
        try:
            result = f()
        except RecursionError:
            Logger.debug(f"Recursion error caught parsing from {start.value} to {end.value}")
            result = Error()
            self.errors.append(TooManyBracketsError(t1))
            self.tr.skip_to(end)
        except Exception as e:  # if it's a block, try moving one context up, otherwise try to find closing bracket
            Logger.debug(f"Exception caught parsing from {start.value} to {end.value}, skipping to closing bracket: {e}")
            result = Error()
            if end.token_type == TokenType.CURLY_CLOSE:
                self.tr.move_context_up()
                return result.with_code_range(CodeRange(t1.code_range.start, self.tr.current_code_range()))
            else:
                self.tr.skip_to(end)
        try:
            t2 = self.tr.require_type(end.token_type)
            # code_range = CodeRange(t1.code_range.start, t2.code_range.end)
            return result
        except:
            self.errors.append(UnbalancedBracketsError(start, end, t1.code_range, self.tr.current_code_range()))
            raise ParseError()
