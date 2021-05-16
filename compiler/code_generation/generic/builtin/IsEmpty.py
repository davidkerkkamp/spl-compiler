from typing import List

import compiler.analysis.unification as uni
from compiler.AST.fields import FieldType
from compiler.analysis.typing import Env
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod
import compiler.code_generation.generic.generator_utils as gen_utils
import compiler.code_generation.generic.op_codes as codes

class IsEmpty(BuiltInMethod):
    def __init__(self):
        super().__init__()
        self.name = 'isEmpty'
        self.num_args = 1
        self.num_quants = 1
        self.return_type = uni.InferenceBool()

    def add_to_env(self, env: Env):
        tv = env.fresh_type_var()
        quants = [tv for _ in range(self.num_quants)]
        env.add_builtin(self.name, quants, [uni.InferenceList(tv)], self.return_type)

    def generate_code(self, arg_types: List[uni.InferenceType], code_builder: OpCodeBuilder):
        assert len(arg_types) == 1, f'len function needs 1 argument, {len(arg_types)} where given'
        t = arg_types[0]
        assert isinstance(t, uni.InferenceList), f'Error during code generation of {self.name}: ' \
                                                 f'expects argument of type list, but type {t} was given'

        arg = gen_utils.Local(-1)
        code_builder.add(codes.LdLoc(arg))
        code_builder.add(codes.PushConst(0))
        code_builder.add(codes.Eq())
        code_builder.add(codes.Ret())
