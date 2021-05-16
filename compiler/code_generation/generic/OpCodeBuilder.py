from __future__ import annotations
from typing import List, Dict

from compiler.analysis.typing import Env, TypeInferrable
from compiler.analysis.unification import InferenceType
import compiler.code_generation.generic.op_codes as codes
import compiler.code_generation.generic.generator_utils as gen_utils
from compiler.code_generation.generic.GeneratorContext import GeneratorContext


class OpCodeBuilder:
    def __init__(self, context: GeneratorContext, env: Env):
        self.ops: List[codes.GenericOpCode] = []
        self.label_counter = 0
        self.local_counter = 0
        self.locals: Dict[int, gen_utils.Local] = {}
        self.env = env
        self.context = context

    def get_local(self, id: int):
        l = self.locals.get(id)
        if not l:
            l = self.add_local(id, len(self.locals))
        return l

    def add_local(self, id: int, index: int):
        l = gen_utils.Local(index)
        self.locals[id] = l
        return l

    def is_global(self, id: int):
        return id in self.context.globals

    def get_global(self, id: int):
        return self.context.get_global(id)

    def get_type(self, ast_node: TypeInferrable):
        sigma = self.env.fresh_type_var()
        subst = ast_node.infer_type(self.env, sigma)
        return sigma.substitute(subst)

    def fresh_label(self):
        self.label_counter += 1
        return gen_utils.Label(self.label_counter)

    def add_print_str(self, s: str):
        for c in s:
            self.ops.append(codes.PushConst(ord(c)))
            self.ops.append(codes.PrintChar())

    def add(self, op_code: codes.GenericOpCode):
        self.ops.append(op_code)

    def mark(self, label: gen_utils.Label):
        self.ops.append(codes.MarkLabel(label))

    def get_fun_instance(self, name: str, arg_types: List[InferenceType]):
        return gen_utils.FunctionInstance(name, arg_types=arg_types)

    def add_call(self, fun_name: str, arg_types: List[InferenceType], hide=False):
        fun_instance = gen_utils.FunctionInstance(fun_name, arg_types=arg_types, hide_from_user=hide)
        self.context.require_fun_instance(fun_instance)
        self.add(codes.Call(
            gen_utils.Function(fun_instance.create_identifier(),
                               len(fun_instance.arg_types))
        ))

    def ends_with_return(self):
        if len(self.ops) == 0:
            return False
        return isinstance(self.ops[-1], codes.Ret) or isinstance(self.ops[-1], codes.RetNoValue)

