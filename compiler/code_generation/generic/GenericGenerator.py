import copy
from typing import Set, Dict, List

from compiler.AST.declarations import VarDecl, FunDecl
from compiler.AST.spl_file import SPLFile
from compiler.analysis.typing import Env
import compiler.code_generation.generic.generator_utils as gen_utils
from compiler.analysis.unification import Subst
from compiler.code_generation.generic.GeneratorContext import GeneratorContext
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
import compiler.code_generation.generic.op_codes as codes
from compiler.code_generation.generic.builtin.BuiltInMethod import BuiltInMethod


class GenericGenerator:
    def __init__(self, spl_file: SPLFile, env: Env, builtins: List[BuiltInMethod]):
        self.spl_file = spl_file
        self.env = env
        self.builtins = builtins
        self.context = GeneratorContext()
        self.functions = []
        self.processed_instances: Set[str] = set()
        self.function_asts: Dict[str, FunDecl] = {}

    def get_function_asts(self):
        for decl in self.spl_file.declarations:
            if isinstance(decl, FunDecl):
                self.function_asts[decl.name.value] = decl

    def initialize(self):
        code_builder = OpCodeBuilder(self.context, self.env)
        main = gen_utils.FunctionInstance('main', [])
        self.initialize_globals(code_builder)
        code_builder.add_call(main.name, main.arg_types)
        code_builder.add(codes.Halt())
        init = gen_utils.FunctionInstance('init', [], hide_from_user=True, entry_point=True)
        self.functions.append((init, gen_utils.FunctionImpl(code_builder.ops)))
        self.context.require_fun_instance(main)

    def initialize_globals(self, code_builder: OpCodeBuilder):
        for decl in self.spl_file.declarations:  # Extra iteration over decls to add globals to context
            if isinstance(decl, VarDecl):
                code_builder.get_global(decl.id_number)
        for decl in self.spl_file.declarations:
            if isinstance(decl, VarDecl):
                assert decl.id_number is not None, 'Var declaration ID should be set during binding analysis'
                decl.expression.generate_code(code_builder)
                glob = code_builder.get_global(decl.id_number)
                code_builder.add(codes.StGlob(glob))

    def generate_function_impls(self):
        while len(self.context.needed_fun_instances) > 0:
            fun_key, fun_inst = self.context.needed_fun_instances.popitem()
            if fun_key in self.processed_instances:
                continue  # Already generated code
            code_builder = OpCodeBuilder(self.context, copy.deepcopy(self.env))  # Deep copy env for polymorphic funcs
            if (fun_decl := self.function_asts.get(fun_inst.name, None)) is not None:
                # Check argument types
                subst = Subst.empty()
                for arg_id, arg_type in zip(fun_decl.arg_ids, fun_inst.arg_types):
                    current = code_builder.env.get_var(arg_id)
                    subst = current.substitute(subst).unify(arg_type).compose(subst)
                code_builder.env.substitute(subst)
                # Initialize args as local vars
                num_args = len(fun_decl.arg_ids)
                for i, arg_id in enumerate(fun_decl.arg_ids):
                    code_builder.add_local(arg_id, -num_args + i)
                fun_decl.block.generate_code(code_builder)
            else:
                # Check builtins
                builtin = None
                for b in self.builtins:
                    if b.name == fun_inst.name:
                        builtin = b
                if builtin is not None:
                    builtin.generate_code(fun_inst.arg_types, code_builder)
                else:
                    raise Exception(f'Unknown function \'{fun_inst.name}\' encountered while generating code')
            if not code_builder.ends_with_return():
                code_builder.add(codes.RetNoValue())  # Add return if function doesn't end with return stmt
            self.functions.append((fun_inst, gen_utils.FunctionImpl(code_builder.ops)))
            self.processed_instances.add(fun_key)

    def generate(self):
        self.get_function_asts()
        self.initialize()
        self.generate_function_impls()
        return self.functions  # , len(self.context.globals)


