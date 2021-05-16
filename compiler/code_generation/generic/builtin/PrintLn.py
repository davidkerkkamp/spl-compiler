from typing import List

from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod
import compiler.analysis.unification as uni
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
import compiler.code_generation.generic.generator_utils as gen_utils
import compiler.code_generation.generic.op_codes as codes


class PrintLn(BuiltInMethod):
    def __init__(self):
        super().__init__()
        self.name = 'println'
        self.num_args = 1
        self.num_quants = 1
        self.return_type = uni.InferenceVoid()

    def generate_code(self, arg_types: List[uni.InferenceType], code_builder: OpCodeBuilder):
        arg = gen_utils.Local(-1)
        assert len(arg_types) == 1, \
            f'Error during code generation of \'{self.name}\': ' \
            f'expected {self.num_args} argument but found {len(arg_types)}'
        arg_type = arg_types[0]
        assert not isinstance(arg_type, uni.InferenceTypeVar) or isinstance(arg_type, uni.InferenceVoid), \
            f'Error during code generation: could not generate {self.name} code for type {arg_type}'
        code_builder.add(codes.LdLoc(arg))
        code_builder.add_call('print', [arg_type])
        code_builder.add(codes.PushConst(ord('\n')))
        code_builder.add(codes.PrintChar())
