from typing import Dict, List

from compiler.AST.base import SPL
from compiler.analysis.binding import BindingAnalyzable, Context
from compiler.analysis.typing import TypeInferrable, Env
from compiler.analysis.unification import InferenceType, Subst, InferenceInt, InferenceBool, InferenceChar, \
    InferenceTuple, InferenceList, InferenceVoid


# ************************** Type **************************

class Type(SPL, TypeInferrable, BindingAnalyzable):
    def __init__(self):
        super().__init__()

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        pass

    def infer_type(self, env: Env, sigma: InferenceType):
        return Subst.empty()


class BasicType(Type):
    pass


class IntType(BasicType):
    def __init__(self):
        super().__init__()

    def pretty_print(self, i=0):
        return 'Int'

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceInt(), self.code_range)


class BoolType(BasicType):
    def __init__(self):
        super().__init__()

    def pretty_print(self, i=0):
        return 'Bool'

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceBool(), self.code_range)


class CharType(BasicType):
    def __init__(self):
        super().__init__()

    def pretty_print(self, i=0):
        return 'Char'

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceChar(), self.code_range)


class TypeVarType(BasicType):
    def __init__(self, var_name: str, id_number: int):
        super().__init__()
        self.var_name = var_name
        self.id_number = id_number

    def pretty_print(self, i=0):
        return self.var_name + ('' if self.id_number is None else f'[ {self.id_number} ]')

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.id_number = context.get_or_add_type(self.var_name)

    def infer_type(self, env: Env, sigma: InferenceType):
        assert self.id_number is not None, 'Binding analysis must be done before typing'
        return sigma.unify_or_type_error(env.get_var(self.id_number), self.code_range)


class TupleType(Type):
    def __init__(self, fst_type: Type, snd_type: Type):
        super().__init__()
        self.fst_type = fst_type
        self.snd_type = snd_type

    def pretty_print(self, i=0):
        return f'({self.fst_type.pretty_print(i)}, {self.snd_type.pretty_print(i)})'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.fst_type.binding_analysis(context, feedback)
        self.snd_type.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        a1, a2 = env.fresh_type_var(), env.fresh_type_var()
        star1 = self.fst_type.infer_type(env, a1)
        env.substitute(star1)
        star2 = self.snd_type.infer_type(env, a2).compose(star1)
        return sigma.unify_or_type_error(InferenceTuple(a1, a2).substitute(star2), self.code_range).compose(star2)


class ListType(Type):
    def __init__(self, list_type: Type):
        super().__init__()
        self.list_type = list_type

    def pretty_print(self, i=0):
        return f'[{self.list_type.pretty_print(i)}]'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.list_type.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        a = env.fresh_type_var()
        star = self.list_type.infer_type(env, a)
        env.substitute(star)
        return sigma.unify_or_type_error(InferenceList(a).substitute(star), self.code_range).compose(star)


# ************************** Return type **************************

class ReturnType(SPL, TypeInferrable, BindingAnalyzable):
    def __init__(self):
        super().__init__()

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        pass

    def infer_type(self, env: Env, sigma: InferenceType):
        return Subst.empty()


class ValueReturn(ReturnType):
    def __init__(self, return_type: Type):
        super().__init__()
        self.return_type = return_type

    def pretty_print(self, i=0):
        return self.return_type.pretty_print(i)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.return_type.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        return self.return_type.infer_type(env, sigma)


class VoidReturn(ReturnType):
    def __init__(self):
        super().__init__()

    def pretty_print(self, i=0):
        return 'Void'

    def infer_type(self, env: Env, sigma: InferenceType):
        return sigma.unify_or_type_error(InferenceVoid(), self.code_range)


# ************************** Function type **************************

class FunArgs(SPL):
    def __init__(self, args: List[Type]):
        super().__init__()
        self.args = args

    def pretty_print(self, i=0):
        return ''.join([x.pretty_print(i) + ' ' for i, x in enumerate(self.args)])


class FunctionType(SPL, BindingAnalyzable):
    def __init__(self, args: FunArgs, return_type: ReturnType):
        super().__init__()
        self.args = args
        self.return_type = return_type

    def pretty_print(self, i=0):
        return f'{self.args.pretty_print(i)}-> {self.return_type.pretty_print(i)}'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        for arg in self.args.args:
            arg.binding_analysis(context, feedback)
        self.return_type.binding_analysis(context, feedback)
