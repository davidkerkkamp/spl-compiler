from __future__ import annotations
from typing import Dict
import compiler.code_generation.generic.generator_utils as gen_utils


class GeneratorContext:
    def __init__(self):
        self.needed_fun_instances: Dict[str, gen_utils.FunctionInstance] = {}
        self.globals: Dict[int, int] = {}

    def require_fun_instance(self, fun_instance: gen_utils.FunctionInstance):
        fun_str = f'{fun_instance.name}_{"_".join([str(arg) for arg in fun_instance.arg_types])}'
        if fun_str not in self.needed_fun_instances:
            self.needed_fun_instances[fun_str] = fun_instance

    def get_global(self, id: int):
        g = self.globals.get(id)
        if g is None:
            g = len(self.globals)
            self.globals[id] = g
        return gen_utils.Global(g)

