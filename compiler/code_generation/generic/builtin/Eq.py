from typing import List

import compiler.analysis.unification as uni
from compiler.AST.fields import FieldType
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod
import compiler.code_generation.generic.generator_utils as gen_utils
import compiler.code_generation.generic.op_codes as codes


class Eq(BuiltInMethod):
    def __init__(self):
        super().__init__()
        self.name = 'equals'
        self.num_args = 2
        self.num_quants = 2
        self.return_type = uni.InferenceBool()

    def generate_code(self, arg_types: List[uni.InferenceType], code_builder: OpCodeBuilder):
        assert len(arg_types) == 2, \
            f'Error during code generation of \'{self.name}\': ' \
            f'expected {self.num_args} arguments but found {len(arg_types)}'
        t1 = arg_types[0]
        t2 = arg_types[1]
        assert t1.is_equal(t2) or \
               (isinstance(t1, uni.InferenceList) and isinstance(t1.t, uni.InferenceTypeVar)
                and isinstance(t2, uni.InferenceList) and isinstance(t2.t, uni.InferenceTypeVar)), \
            f'Error during code generation: {self.name} expects both arguments to be of the same type'
        assert not isinstance(t1, uni.InferenceVoid), \
            f'Error during code generation: could not generate {self.name} code for type {t1}'
        arg1 = gen_utils.Local(-1)
        arg2 = gen_utils.Local(-2)

        if isinstance(t1, uni.InferenceInt) or isinstance(t1, uni.InferenceBool) or isinstance(t1, uni.InferenceChar):
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.Eq())
            code_builder.add(codes.Ret())
        elif isinstance(t1, uni.InferenceList):
            null_label = code_builder.fresh_label()
            false_label = code_builder.fresh_label()
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.BrFalse(null_label))
            if isinstance(t1.t, uni.InferenceTypeVar):
                code_builder.add_print_str('Error: type var list has contents')
                code_builder.add(codes.Halt())
            else:
                code_builder.add(codes.LdLoc(arg1))
                code_builder.add(codes.LdFld(FieldType.Hd))
                code_builder.add(codes.LdLoc(arg2))
                code_builder.add(codes.LdFld(FieldType.Hd))
                code_builder.add_call(self.name, [t1.t, t1.t])
                code_builder.add(codes.BrFalse(false_label))

            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdFld(FieldType.Tl))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.LdFld(FieldType.Tl))
            tail = uni.InferenceList(t1.t)
            code_builder.add_call(self.name, [tail, tail])
            code_builder.add(codes.Ret())

            code_builder.mark(null_label)
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.Eq())
            code_builder.add(codes.Ret())

            code_builder.mark(false_label)
            code_builder.add(codes.PushConst(0))
            code_builder.add(codes.Ret())
        elif isinstance(t1, uni.InferenceTuple):
            false_label = code_builder.fresh_label()
            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdFld(FieldType.Fst))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.LdFld(FieldType.Fst))
            code_builder.add_call(self.name, [t1.t1, t1.t1])
            code_builder.add(codes.BrFalse(false_label))

            code_builder.add(codes.LdLoc(arg1))
            code_builder.add(codes.LdFld(FieldType.Snd))
            code_builder.add(codes.LdLoc(arg2))
            code_builder.add(codes.LdFld(FieldType.Snd))
            code_builder.add_call(self.name, [t1.t2, t1.t2])
            code_builder.add(codes.Ret())

            code_builder.mark(false_label)
            code_builder.add(codes.PushConst(0))
            code_builder.add(codes.Ret())
