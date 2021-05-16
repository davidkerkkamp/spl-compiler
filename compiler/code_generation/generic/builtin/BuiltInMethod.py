from __future__ import annotations
from typing import List

from compiler.analysis.binding import Context
from compiler.analysis.typing import Env
from compiler.analysis.unification import InferenceType, InferenceVoid
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder


class BuiltInMethod:
    def __init__(self):
        self.name = 'undefined'
        self.num_args = 0
        self.num_quants = 0
        self.return_type = InferenceVoid()

    def add_to_context(self, context: Context):
        context.add_function(self.name)

    def add_to_env(self, env: Env):
        tv = env.fresh_type_var()
        args = [tv for _ in range(self.num_args)]
        quants = [tv for _ in range(self.num_quants)]
        env.add_builtin(self.name, quants, args, self.return_type)

    def generate_code(self, arg_types: List[InferenceType], code_builder: OpCodeBuilder):
        pass


