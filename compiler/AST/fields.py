from __future__ import annotations

from enum import Enum, auto
from typing import Dict

import compiler.AST.base as base
from compiler.analysis.binding import Context
from compiler.analysis.typing import Env
from compiler.analysis.unification import InferenceType, InferenceTuple, InferenceList
import compiler.code_generation.generic.op_codes as codes
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.errors import UnknownVariableError


# ************************** Fields **************************

class FieldType(Enum):
    Fst = auto()
    Snd = auto()
    Hd = auto()
    Tl = auto()


class Variable(base.Field):
    def __init__(self, name: str, id_number: int = None):
        super().__init__()
        self.name = name
        self.id_number = id_number

    def pretty_print(self, i=0):
        id_str = '' if self.id_number is None else f'[ {self.id_number} ]'
        return self.name + id_str

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        if (v := context.get_variable(self.name)) is not None:
            self.id_number = v
        else:
            feedback['errors'] = [] if feedback.get('errors') is None else feedback['errors']
            feedback['errors'].append(UnknownVariableError(self.code_range, self.name))

    def infer_type(self, env: Env, sigma: InferenceType):
        type_var = env.get_var(self.id_number)
        result = sigma.unify_or_type_error(type_var, self.code_range)
        env.substitute(result)
        return result

    def generate_code(self, code_builder: OpCodeBuilder):
        if code_builder.is_global(self.id_number):
            glob = code_builder.get_global(self.id_number)
            code_builder.add(codes.LdGlob(glob))
        else:
            loc = code_builder.get_local(self.id_number)
            code_builder.add(codes.LdLoc(loc))

    def generate_storage_code(self, code_builder: OpCodeBuilder):
        if code_builder.is_global(self.id_number):
            glob = code_builder.get_global(self.id_number)
            code_builder.add(codes.StGlob(glob))
        else:
            loc = code_builder.get_local(self.id_number)
            code_builder.add(codes.StLoc(loc))


class Accessor(base.Field):
    def __init__(self, field_type: FieldType, field: base.Field):
        super().__init__()
        self.field_type = field_type
        self.field = field

    def pretty_print(self, i=0):
        accessor = {
            FieldType.Fst: 'fst',
            FieldType.Snd: 'snd',
            FieldType.Hd: 'hd',
            FieldType.Tl: 'tl'
        }.get(self.field_type)
        return f'{self.field.pretty_print(i)}.{accessor}'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.field.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        if self.field_type == FieldType.Fst:
            tup = InferenceTuple(sigma, env.fresh_type_var())
            return self.field.infer_type(env, tup)
        elif self.field_type == FieldType.Snd:
            tup = InferenceTuple(env.fresh_type_var(), sigma)
            return self.field.infer_type(env, tup)
        elif self.field_type == FieldType.Hd:
            lst = InferenceList(sigma)
            return self.field.infer_type(env, lst)
        elif self.field_type == FieldType.Tl:
            lst = InferenceList(env.fresh_type_var())
            star = sigma.unify_or_type_error(lst, self.code_range)
            env.substitute(star)
            return self.field.infer_type(env, sigma.substitute(star)).compose(star)
        else:
            raise Exception('Unknown field accessor')

    def generate_code(self, code_builder: OpCodeBuilder):
        self.field.generate_code(code_builder)
        code_builder.add(codes.LdFld(self.field_type))

    def generate_storage_code(self, code_builder: OpCodeBuilder):
        self.field.generate_code(code_builder)
        code_builder.add(codes.Swp())
        code_builder.add(codes.StFld(self.field_type))
