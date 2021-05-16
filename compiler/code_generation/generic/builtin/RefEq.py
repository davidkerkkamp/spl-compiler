from typing import List

import compiler.analysis.unification as uni
import compiler.code_generation.generic.generator_utils as gen_utils
import compiler.code_generation.generic.op_codes as codes
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod


class RefEq(BuiltInMethod):
    def __init__(self):
        super().__init__()
        self.name = '__refeq'
        self.num_args = 2
        self.num_quants = 1
        self.return_type = uni.InferenceBool()

    def generate_code(self, arg_types: List[uni.InferenceType], code_builder: OpCodeBuilder):
        code_builder.add(codes.LdLoc(gen_utils.Local(-1)))
        code_builder.add(codes.LdLoc(gen_utils.Local(-2)))
        code_builder.add(codes.Eq())
        code_builder.add(codes.Ret())
