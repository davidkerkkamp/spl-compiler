from __future__ import annotations

import compiler.analysis.unification as uni
from compiler.tokens import Token
from compiler.utils import CodeRange, Colors


class CompilerError(Exception):
    def __init__(self, code_range: CodeRange):
        self.code_range = code_range

    def print_error(self, class_name, message: str):
        return f'{Colors.FAIL}{class_name}: {message} at: \n{self.code_range}{Colors.ENDC}'


class ParserError(CompilerError):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)


class SyntaxError(ParserError):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)


class TypeError(CompilerError):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)


class BindingError(CompilerError):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)


class CodeGenError(Exception):
    def __init__(self):
        pass

class ReturnValueError(CompilerError):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)


class UnexpectedCharError(SyntaxError):
    def __init__(self, code_range: CodeRange, token_str: str):
        super().__init__(code_range)
        self.token_str = token_str

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Unexpected character \'{self.token_str}\'')


class UnexpectedTokenError(SyntaxError):
    def __init__(self, token: Token, code_range: CodeRange):
        super().__init__(code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Unexpected token \'{self.token_str}\'')


class ExpectedSymbolError(SyntaxError):
    def __init__(self, symbol: str, token: Token):
        super().__init__(token.code_range)
        self.symbol = symbol
        self.token = token

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Expected \'{self.symbol}\' '
                                                                  f'but found \'{self.token.value}\'')


class ExpectedTermError(SyntaxError):
    def __init__(self, token: Token):
        super().__init__(token.code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Term expected but found \'{self.token_str}\'')


class ExpectedExprError(SyntaxError):
    def __init__(self, token: Token):
        super().__init__(token.code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Expression expected but found \'{self.token_str}\'')


class ExpectedIdentError(SyntaxError):
    def __init__(self, token: Token):
        super().__init__(token.code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Identifier expected but found \'{self.token_str}\'')


class ExpectedStatementError(SyntaxError):
    def __init__(self, token: Token):
        super().__init__(token.code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Statement expected but found \'{self.token_str}\'')


class ExpectedTypeError(SyntaxError):
    def __init__(self, token: Token):
        super().__init__(token.code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Type expected but found \'{self.token_str}\'')


class UnbalancedBracketsError(SyntaxError):
    def __init__(self, start: Token, end: Token, range_start: CodeRange, range_end: CodeRange):
        super().__init__(range_start)
        self.range_start = range_start
        self.range_end = range_end
        self.start = start
        self.end = end

    def __str__(self):
        return f'{Colors.FAIL}{self.__class__.__base__.__name__}: Unbalanced brackets \'{self.start.value}\' ' \
               f'and \'{self.end.value}\' between:\n{self.range_start}\n    and\n{self.range_end}{Colors.ENDC}'


class MissingSemicolonError(SyntaxError):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, 'Missing semicolon \';\'')


class UnknownFieldError(SyntaxError):
    def __init__(self, field: str, code_range: CodeRange):
        super().__init__(code_range)
        self.field = field

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Unknown field \'{self.field}\', valid fields are: '
                                                                  f'fst, snd, hd, tl')


class TooManyBracketsError(ParserError):
    def __init__(self, token: Token):
        super().__init__(token.code_range)
        self.token_str = token.value

    def __str__(self):
        return self.print_error(self.__class__.__name__, f'Too many brackets \'{self.token_str}\'')


class EmptyFunctionBodyError(ParserError):
    def __init__(self, function_name: str, code_range: CodeRange):
        super().__init__(code_range)
        self.function_name = function_name

    def __str__(self):
        return self.print_error(self.__class__.__name__, f'Function \'{self.function_name}\' has an empty body')


class NumberOverflowError(TypeError):
    def __init__(self, num: int, code_range: CodeRange):
        super().__init__(code_range)
        self.token_str = num

    def __str__(self):
        return self.print_error(self.__class__.__name__,
                                f'Number \'{self.token_str}\' is too large for target integer type')


class NumberUnderflowError(TypeError):
    def __init__(self, num: int, code_range: CodeRange):
        super().__init__(code_range)
        self.token_str = num

    def __str__(self):
        return self.print_error(self.__class__.__name__,
                                f'Number \'{self.token_str}\' is too small for target integer type')


class TypeMismatch(TypeError):
    def __init__(self, code_range: CodeRange, t1, t2):  # t1, t2: InferenceType
        super().__init__(code_range)
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Type mismatch! Expected type {self.t1} but found {self.t2}')


class InvalidTypeError(TypeError):
    def __init__(self, code_range: CodeRange, tv: int, other):  # other: InferenceType
        super().__init__(code_range)
        self.tv = tv
        self.other = other

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__, f'Invalid type {self.other} contains v{self.tv}, '
                                                                  f'but types cannot be recursive')


class UnknownVarTypeError(TypeError):
    def __init__(self, code_range: CodeRange, tv: int, name: str):  # other: InferenceType
        super().__init__(code_range)
        self.tv = tv
        self.name = name

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Type {self.tv} of variable \'{self.name}\' could not be determined')


class FunArgsTypesMismatch(TypeError):
    def __init__(self, code_range: CodeRange, name: str, args_len: int, types_len: int):
        super().__init__(code_range)
        self.name = name
        self.args_len = args_len
        self.types_len = types_len

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Function \'{self.name}\' is declared with {self.args_len} arguments, '
                                f'but has {self.types_len} argument types')


class FunCallArgsMismatch(TypeError):
    def __init__(self, code_range: CodeRange, name: str, args_len: int, types_len: int):
        super().__init__(code_range)
        self.name = name
        self.args_len = args_len
        self.types_len = types_len

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Function \'{self.name}\' is called with {self.args_len} arguments, '
                                f'but is declared with {self.types_len} argument types')


class DuplicateIdentifierError(BindingError):
    def __init__(self, code_range: CodeRange, ident: str):
        super().__init__(code_range)
        self.ident = ident

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Already defined identifier \'{self.ident}\' is re-defined')


class DuplicateFunctionError(BindingError):
    def __init__(self, code_range: CodeRange, ident: str):
        super().__init__(code_range)
        self.ident = ident

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Already defined function \'{self.ident}\' is re-defined')


class UnknownFunctionError(BindingError):
    def __init__(self, code_range: CodeRange, fun: str):
        super().__init__(code_range)
        self.fun = fun

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Function with name \'{self.fun}\' is not defined')


class UnknownVariableError(BindingError):
    def __init__(self, code_range: CodeRange, var: str):
        super().__init__(code_range)
        self.var = var

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Variable with name \'{self.var}\' is not defined')


class NotAllPathsReturnError(ReturnValueError):
    def __init__(self, code_range: CodeRange, fun: str):
        super().__init__(code_range)
        self.fun = fun

    def __str__(self):
        return self.print_error(self.__class__.__base__.__name__,
                                f'Not all paths in function \'{self.fun}\' return,')


class NoFunctionInstanceError(CodeGenError):
    def __init__(self, fun_name: str, arg_types: [uni.InferenceType]):
        super().__init__()
        self.fun_name = fun_name
        self.arg_types = arg_types

    def __str__(self):
        arg_str = ', '.join([str(a) for a in self.arg_types])
        return f'{Colors.FAIL}{self.__class__.__base__.__name__}: ' \
               f'No instance of function \'{self.fun_name}\' is available for argument types: {arg_str}{Colors.ENDC}'
