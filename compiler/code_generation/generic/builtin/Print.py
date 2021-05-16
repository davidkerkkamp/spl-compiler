from typing import List

import compiler.analysis.unification as uni
from compiler.AST.fields import FieldType
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod
import compiler.code_generation.generic.generator_utils as gen_utils
import compiler.code_generation.generic.op_codes as codes


class Print(BuiltInMethod):
    def __init__(self):
        super().__init__()
        self.name = 'print'
        self.num_args = 1
        self.num_quants = 1
        self.return_type = uni.InferenceVoid()

    def generate_code(self, arg_types: List[uni.InferenceType], code_builder: OpCodeBuilder):
        arg = gen_utils.Local(-1)
        assert len(arg_types) == 1, \
            f'Error during code generation of \'{self.name}\': ' \
            f'expected {self.num_args} argument but found {len(arg_types)}'
        arg_type = arg_types[0]
        assert not isinstance(arg_type, uni.InferenceTypeVar) and not isinstance(arg_type, uni.InferenceVoid), \
            f'Error during code generation: could not generate {self.name} code for type {arg_type}'
        if isinstance(arg_type, uni.InferenceInt):
            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.PrintInt())
        if isinstance(arg_type, uni.InferenceBool):
            false_label = code_builder.fresh_label()
            end_label = code_builder.fresh_label()

            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.BrFalse(false_label))
            code_builder.add_print_str('True')
            code_builder.add(codes.Br(end_label))
            code_builder.mark(false_label)
            code_builder.add_print_str('False')
            code_builder.mark(end_label)
        if isinstance(arg_type, uni.InferenceChar):
            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.PrintChar())
        if isinstance(arg_type, uni.InferenceList):
            null_label = code_builder.fresh_label()
            end_label = code_builder.fresh_label()

            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.BrFalse(null_label))
            if isinstance(arg_type.t, uni.InferenceTypeVar):
                code_builder.add_print_str('Error: type var list has contents')
                code_builder.add(codes.Halt())
            else:
                code_builder.add(codes.LdLoc(arg))
                code_builder.add(codes.LdFld(FieldType.Hd))
                code_builder.add_call(self.name, [arg_type.t])
                code_builder.add(codes.Pop())
            # If not a str (list of char), then print cons operator in between
            if not isinstance(arg_type.t, uni.InferenceChar):
                code_builder.add_print_str(' : ')

            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.LdFld(FieldType.Tl))
            code_builder.add_call(self.name, [uni.InferenceList(arg_type.t)])
            code_builder.add(codes.Pop())
            code_builder.add(codes.Br(end_label))
            code_builder.mark(null_label)
            # End with empty list [] if not str
            if not isinstance(arg_type.t, uni.InferenceChar):
                code_builder.add_print_str('[]')
            code_builder.mark(end_label)
        if isinstance(arg_type, uni.InferenceTuple):
            code_builder.add_print_str('(')
            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.LdFld(FieldType.Fst))
            code_builder.add_call(self.name, [arg_type.t1])
            code_builder.add(codes.Pop())
            code_builder.add_print_str(', ')
            code_builder.add(codes.LdLoc(arg))
            code_builder.add(codes.LdFld(FieldType.Snd))
            code_builder.add_call(self.name, [arg_type.t2])
            code_builder.add(codes.Pop())
            code_builder.add_print_str(')')
