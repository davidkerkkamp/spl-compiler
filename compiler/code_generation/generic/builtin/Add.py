from typing import List

import compiler.analysis.unification as uni
from compiler.AST.fields import FieldType
from compiler.analysis.typing import Env
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod
import compiler.code_generation.generic.generator_utils as gen_utils
import compiler.code_generation.generic.op_codes as codes
from compiler.errors import NoFunctionInstanceError


class Add(BuiltInMethod):
    def __init__(self):
        super().__init__()
        self.name = '__add'
        self.num_args = 2
        self.num_quants = 1

    def add_to_env(self, env: Env):
        tv = env.fresh_type_var()
        quants = [tv for _ in range(self.num_quants)]
        env.add_builtin(self.name, quants, [tv, tv], tv)

    def generate_code(self, arg_types: List[uni.InferenceType], code_builder: OpCodeBuilder):
        assert len(arg_types) == 2, \
            f'Error during code generation of \'{self.name}\': ' \
            f'expected {self.num_args} arguments but found {len(arg_types)}'
        t1, t2 = arg_types[0], arg_types[1]
        assert t1.is_equal(t2) or \
               (isinstance(t1, uni.InferenceList) and isinstance(t1.t, uni.InferenceTypeVar)
                and isinstance(t2, uni.InferenceList) and isinstance(t2.t, uni.InferenceTypeVar)), \
            f'Error during code generation: {self.name} expects both arguments to be of the same type'
        assert not isinstance(t1, uni.InferenceVoid), \
            f'Error during code generation: could not generate {self.name} code for type {t1}'

        arg1 = gen_utils.Local(-2)
        arg2 = gen_utils.Local(-1)

        if isinstance(t1, uni.InferenceInt) or isinstance(t1, uni.InferenceChar):
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.Add())
            code_builder.add(codes.Ret())
        elif isinstance(t1, uni.InferenceList):
            null_label_1 = code_builder.fresh_label()
            null_label_2 = code_builder.fresh_label()
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.BrFalse(null_label_1))
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdFld(FieldType.Hd))
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdFld(FieldType.Tl))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add_call(self.name, [t1, t1], hide=True)
            code_builder.add(codes.CreateListCons())
            code_builder.add(codes.Ret())

            code_builder.mark(null_label_1)
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.BrFalse(null_label_2))
            if isinstance(t2.t, uni.InferenceTypeVar):
                code_builder.add_print_str('Error: type var list has contents')
                code_builder.add(codes.Halt())
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.LdFld(FieldType.Hd))
            code_builder.add(codes.PushConst(0))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.LdFld(FieldType.Tl))
            code_builder.add_call(self.name, [t1, t1], hide=True)
            code_builder.add(codes.CreateListCons())
            code_builder.add(codes.Ret())

            code_builder.mark(null_label_2)
            code_builder.add(codes.CreateListNil())
            code_builder.add(codes.Ret())
        elif isinstance(t1, uni.InferenceBool) or isinstance(t1, uni.InferenceTuple):
            raise NoFunctionInstanceError(self.name, arg_types)
