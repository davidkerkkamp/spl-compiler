from enum import Enum, auto
from typing import Dict, List

import compiler.AST.base as base
from compiler.AST.base import Expr, Field
from compiler.analysis.binding import Context
from compiler.analysis.typing import Env
from compiler.analysis.unification import InferenceType, Subst, InferenceInt, InferenceBool, InferenceList, \
    InferenceChar, InferenceTuple
import compiler.code_generation.generic.op_codes as codes
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.code_generation.generic.generator_utils import FunctionInstance
from compiler.errors import UnknownFunctionError, FunCallArgsMismatch, NoFunctionInstanceError, NumberUnderflowError, \
    NumberOverflowError


# ************************** Operators **************************

class BinaryOpType(Enum):
    Add = auto()  # +
    Sub = auto()  # -
    Mul = auto()  # *
    Div = auto()  # /
    Eq = auto()  # ==
    Neq = auto()  # !=
    Lt = auto()  # <
    Leq = auto()  # <=
    Geq = auto()  # >=
    Gt = auto()  # >
    And = auto()  # &&
    Or = auto()  # ||
    Cons = auto()  # :
    Mod = auto()  # %


class UnaryOpType(Enum):
    Min = auto()  # -
    Neg = auto()  # !


# ************************** Expressions **************************

class Op(Expr):
    def __init__(self, expr1: Expr, op_type: BinaryOpType, expr2: Expr):
        super().__init__()
        self.expr1 = expr1
        self.op_type = op_type
        self.expr2 = expr2

    def pretty_print(self, i=0):
        op = {
            BinaryOpType.Add: '+',
            BinaryOpType.Sub: '-',
            BinaryOpType.Mul: '*',
            BinaryOpType.Div: '/',
            BinaryOpType.Eq: '==',
            BinaryOpType.Neq: '!=',
            BinaryOpType.Lt: '<',
            BinaryOpType.Leq: '<=',
            BinaryOpType.Geq: '>=',
            BinaryOpType.Gt: '>',
            BinaryOpType.And: '&&',
            BinaryOpType.Or: '||',
            BinaryOpType.Cons: ':',
            BinaryOpType.Mod: '%'
        }.get(self.op_type)
        return f'({self.expr1.pretty_print(i)} {op} {self.expr2.pretty_print(i)})'

    def infer_type(self, env: Env, sigma: InferenceType):
        e1_type, e2_type, result_type = None, None, None
        if self.op_type in [BinaryOpType.Sub, BinaryOpType.Mul, BinaryOpType.Div, BinaryOpType.Mod]:
            e1_type, e2_type, result_type = InferenceInt(), InferenceInt(), InferenceInt()
        elif self.op_type in [BinaryOpType.Eq, BinaryOpType.Neq, BinaryOpType.Geq, BinaryOpType.Leq, BinaryOpType.Lt,
                              BinaryOpType.Gt]:
            tv = env.fresh_type_var()
            e1_type, e2_type, result_type = tv, tv, InferenceBool()
        elif self.op_type in [BinaryOpType.Add]:  # Add is overloaded for int, char and list
            tv = env.fresh_type_var()
            e1_type, e2_type, result_type = tv, tv, tv
        elif self.op_type in [BinaryOpType.And, BinaryOpType.Or]:
            e1_type, e2_type, result_type = InferenceBool(), InferenceBool(), InferenceBool()
        elif self.op_type == BinaryOpType.Cons:
            tv = env.fresh_type_var()
            e1_type, e2_type, result_type = tv, InferenceList(tv), InferenceList(tv)

        star1 = self.expr1.infer_type(env, e1_type)
        env.substitute(star1)
        star2 = self.expr2.infer_type(env, e2_type.substitute(star1)).compose(star1)
        return sigma.substitute(star2).unify_or_type_error(result_type.substitute(star2), self.code_range).compose(
            star2)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.expr1.binding_analysis(context, feedback)
        self.expr2.binding_analysis(context, feedback)

    def generate_code(self, code_builder: OpCodeBuilder):
        self.expr1.generate_code(code_builder)
        self.expr2.generate_code(code_builder)

        if self.op_type is BinaryOpType.Eq or self.op_type is BinaryOpType.Neq or self.op_type is BinaryOpType.Add:
            t1, t2 = code_builder.get_type(self.expr1), code_builder.get_type(self.expr2)

            subst = t1.unify(t2)  # To handle cases with empty list
            t1, t2 = t1.substitute(subst), t2.substitute(subst)

            if self.op_type is BinaryOpType.Eq:
                code = codes.Eq()
                name = '__refeq'
            elif self.op_type is BinaryOpType.Neq:
                code = codes.Ne()
                name = '__neq'  # TODO
            elif self.op_type is BinaryOpType.Add:
                if isinstance(t1, InferenceBool) or isinstance(t1, InferenceTuple):
                    raise NoFunctionInstanceError('__add', [t1, t2])
                code = codes.Add()
                name = '__add'

            if t1.is_scalar() and t2.is_scalar():  # If scalar, compare directly with appropriate instruction
                code_builder.add(code)
            else:  # Else call custom equality testing function
                code_builder.add_call(
                    fun_name=name,
                    arg_types=[t1, t2],
                    hide=True
                )
        else:
            code = {
                BinaryOpType.Add: codes.Add(),
                BinaryOpType.Sub: codes.Sub(),
                BinaryOpType.Mul: codes.Mul(),
                BinaryOpType.Div: codes.Div(),
                BinaryOpType.Lt: codes.Lt(),
                BinaryOpType.Leq: codes.Le(),
                BinaryOpType.Geq: codes.Ge(),
                BinaryOpType.Gt: codes.Gt(),
                BinaryOpType.Mod: codes.Mod(),
                BinaryOpType.And: codes.And(),
                BinaryOpType.Or: codes.Or(),
                BinaryOpType.Cons: codes.CreateListCons(),
            }.get(self.op_type)
            assert code is not None, 'Unknown binary operator'
            code_builder.add(code)


class UnaryOp(Expr):
    def __init__(self, op_type: UnaryOpType, expr: Expr):
        super().__init__()
        self.op_type = op_type
        self.expr = expr

    def pretty_print(self, i=0):
        op = {UnaryOpType.Min: '-', UnaryOpType.Neg: '!'}.get(self.op_type)
        return f'({op}{self.expr.pretty_print(i)})'

    def infer_type(self, env: Env, sigma: InferenceType):
        e_type, result_type = None, None
        if self.op_type == UnaryOpType.Neg:
            e_type, result_type = InferenceBool(), InferenceBool()
        elif self.op_type == UnaryOpType.Min:
            e_type, result_type = InferenceInt(), InferenceInt()
            if isinstance(self.expr, ConstNumber):
                self.expr.minus = True

        star = self.expr.infer_type(env, e_type)
        return sigma.substitute(star).unify_or_type_error(result_type.substitute(star), self.code_range).compose(star)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.expr.binding_analysis(context, feedback)

    def generate_code(self, code_builder: OpCodeBuilder):
        self.expr.generate_code(code_builder)
        code = {
            UnaryOpType.Min: codes.Neg(),
            UnaryOpType.Neg: codes.Not(),
        }.get(self.op_type)
        assert code is not None, 'Unknown unary operator'
        code_builder.add(code)


class ConstNumber(Expr):
    def __init__(self, value: int):
        super().__init__()
        self.value = value
        self.minus = False

    def pretty_print(self, i=0):
        return str(self.value)

    def infer_type(self, env: Env, sigma: InferenceType):
        if not self.minus and self.value > 0x7fffffff:  # Check for int overflow
            raise NumberOverflowError(self.value, self.code_range)
        elif self.minus and self.value > 0x80000000:  # Check for int underflow
            raise NumberUnderflowError(self.value, self.code_range)
        return sigma.unify_or_type_error(InferenceInt(), self.code_range)

    def generate_code(self, code_builder: OpCodeBuilder):
        code_builder.add(codes.PushConst(self.value))


class ConstString(Expr):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def pretty_print(self, i=0):
        return self.value

    def generate_code(self, code_builder: OpCodeBuilder):
        for c in self.value:
            code_builder.add(codes.PushConst(ord(c)))
        code_builder.add(codes.CreateListNil())
        for c in self.value:
            code_builder.add(codes.CreateListCons())


class ConstChar(Expr):
    def __init__(self, value: str):
        super().__init__()
        if len(value) > 1 and value[0] == '\\' and value[1] == 'n':
            self.value = '\n'
            x = 5
        else:
            self.value = value[0]

    def pretty_print(self, i=0):
        return f'\'{self.value}\''

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceChar(), self.code_range)

    def generate_code(self, code_builder: OpCodeBuilder):
        code_builder.add(codes.PushConst(ord(self.value)))

class ConstBool(Expr):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def pretty_print(self, i=0):
        return str(self.value)

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceBool(), self.code_range)

    def generate_code(self, code_builder: OpCodeBuilder):
        if self.value:
            code_builder.add(codes.PushConst(-1))  # True is encoded as -1
        else:
            code_builder.add(codes.PushConst(0))  # False is encoded as 0


class FieldExpr(Expr):
    def __init__(self, field: Field):
        super().__init__()
        self.field = field

    def pretty_print(self, i=0):
        return self.field.pretty_print(i)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.field.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        return self.field.infer_type(env, sigma)

    def generate_code(self, code_builder: OpCodeBuilder):
        self.field.generate_code(code_builder)


class EmptyList(Expr):
    def __init__(self):
        super().__init__()

    def pretty_print(self, i=0):
        return '[]'

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceList(env.fresh_type_var()), self.code_range)

    def generate_code(self, code_builder: OpCodeBuilder):
        code_builder.add(codes.CreateListNil())


class Tuple(Expr):
    def __init__(self, fst: Expr, snd: Expr):
        super().__init__()
        self.fst = fst
        self.snd = snd

    def pretty_print(self, i=0):
        return f'({self.fst.pretty_print(i)}, {self.snd.pretty_print(i)})'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.fst.binding_analysis(context, feedback)
        self.snd.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        a1, a2 = env.fresh_type_var(), env.fresh_type_var()
        star1 = self.fst.infer_type(env, a1)
        env.substitute(star1)
        star2 = self.snd.infer_type(env, a2).compose(star1)
        return sigma.substitute(star2).unify_or_type_error(InferenceTuple(a1, a2).substitute(star2), self.code_range) \
            .compose(star2)

    def generate_code(self, code_builder: OpCodeBuilder):
        self.fst.generate_code(code_builder)
        self.snd.generate_code(code_builder)
        code_builder.add(codes.CreateTuple())


class FunctionCall(Expr):
    def __init__(self, function_name: base.Text, expressions: List[Expr]):
        super().__init__()
        self.function_name = function_name
        self.expressions = expressions

    def pretty_print(self, i=0):
        args = '(' + ''.join([x.pretty_print(i) + (', ' if index + 1 < len(self.expressions) else '')
                              for index, x in enumerate(self.expressions)]) + ')'
        return f'{self.function_name.pretty_print(i)}{args}'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        if self.function_name.value not in context.functions:
            feedback['errors'] = [] if feedback.get('errors') is None else feedback['errors']
            feedback['errors'].append(UnknownFunctionError(self.code_range, self.function_name.value))
        for arg in self.expressions:
            arg.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        f = env.functions.get(self.function_name.value)
        if f is not None:
            f = f.instantiate(env)
            args_len = len(self.expressions)
            tv_len = len(f.usage.arg_types)
            if args_len != tv_len:
                raise FunCallArgsMismatch(self.code_range, self.function_name.value, args_len, tv_len)

            subst = Subst.empty()
            for exp, tv in zip(self.expressions, f.usage.arg_types):
                subst = exp.infer_type(env, tv.substitute(subst)).compose(subst)
                env.substitute(subst)
            return sigma.unify_or_type_error(f.usage.return_type.substitute(subst), self.code_range).compose(subst)
        else:  # Function was not yet declared
            type_vars = []
            subst = Subst.empty()
            for arg in self.expressions:
                tv = env.fresh_type_var()
                type_vars.append(tv)
                subst = arg.infer_type(env, tv).compose(subst)
                env.substitute(subst)
            env.add_fun_usage(self.function_name.value, type_vars, sigma, self.code_range)
            return subst

    def generate_code(self, code_builder: OpCodeBuilder):
        arg_types = [code_builder.get_type(e) for e in self.expressions]
        for e in self.expressions:
            e.generate_code(code_builder)
        code_builder.add_call(self.function_name.value, arg_types)
