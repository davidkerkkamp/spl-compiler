from typing import Dict, List

import compiler.AST.base as base
from compiler.AST.base import Decl, Expr
from compiler.analysis.binding import Context
from compiler.analysis.typing import Env
from compiler.analysis.unification import InferenceType, Subst
from compiler.AST.statements import Block
from compiler.AST.types import Type, FunctionType
from compiler.errors import FunArgsTypesMismatch, FunCallArgsMismatch

# ************************** Declarations **************************
from compiler.logging import Logger


class VarDecl(Decl):
    def __init__(self, var_type: Type, name: base.Text, expression: Expr, id_number: int = None):
        super().__init__()
        self.var_type = var_type
        self.name = name
        self.expression = expression
        self.id_number = id_number

    def pretty_print(self, i=0):
        type_str = 'var' if self.var_type is None else self.var_type.pretty_print(i)
        id_str = '' if self.id_number is None else f'[ {self.id_number} ]'
        return f'{type_str} {self.name.pretty_print(i)}{id_str} = {self.expression.pretty_print(i)};'

    def infer_type(self, env: Env, sigma: InferenceType):
        t = env.get_var(self.id_number)
        if self.var_type:
            star = self.var_type.infer_type(env, t)
        else:
            star = Subst.empty()
        env.substitute(star)
        return self.expression.infer_type(env, t.substitute(star)).compose(star)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        num = context.get_variable_current_scope(self.name.value)
        if num is None:
            raise Exception(f'Variable "{self.name.value}" is unknown in current context')
        self.id_number = num
        if self.var_type:
            self.var_type.binding_analysis(context, feedback)
        self.expression.binding_analysis(context, feedback)


class FunArgNames(base.SPL):
    def __init__(self, arg_names: List[base.Text]):
        super().__init__()
        self.arg_names = arg_names

    def pretty_print(self, i=0, arg_ids=None):
        if arg_ids is None or len(arg_ids) < len(self.arg_names):
            arg_ids = ['' for _ in self.arg_names]
        else:
            arg_ids = [f'[ {x} ]' for x in arg_ids]
        return '(' + ', '.join([f'{x.pretty_print()}{arg_ids[index]}' for index, x in enumerate(self.arg_names)]) + ')'


class FunDecl(Decl):
    def __init__(self, name: base.Text, arg_names: FunArgNames, fun_type: FunctionType, block: Block,
                 arg_ids: List[int] = None):
        super().__init__()
        self.name = name
        self.arg_names = arg_names
        self.fun_type = fun_type
        self.block = block
        self.arg_ids = arg_ids

    def pretty_print(self, i=0):
        fun_type = f' :: {self.fun_type.pretty_print(i)}' if self.fun_type is not None else ''
        return f'{self.name.pretty_print(i)}{self.arg_names.pretty_print(i, self.arg_ids)}{fun_type}\n' \
               f'{self.block.indented_print(i)}\n '

    def infer_type(self, env: Env, sigma: InferenceType):
        Logger.debug(f'* Start typing function {self.name.value}')
        assert isinstance(self.arg_ids, list), 'Binding analysis must be done before type inference'
        if self.name.value == 'main':
            assert len(self.arg_ids) == 0, \
                f"Function 'main' cannot take arguments, but is defined with {len(self.arg_ids)}"
        env.add_fun(self.name.value, self.arg_ids)
        name = self.name.value
        f = env.functions.get(name)
        env.update_fun_quants(name, [])

        star = Subst.empty()
        if self.fun_type is not None:
            args_len = len(f.usage.arg_types)
            types_len = len(self.fun_type.args.args)
            if args_len != types_len:
                raise FunArgsTypesMismatch(self.code_range, name, args_len, types_len)

            for arg_tv, arg_type_def in zip(f.usage.arg_types, self.fun_type.args.args):
                star = arg_type_def.infer_type(env, arg_tv).compose(star)
                env.substitute(star)
            star = self.fun_type.return_type.infer_type(env, f.usage.return_type).compose(star)
            env.substitute(star)

        star = self.block.infer_type(env, f.usage.return_type.substitute(star)).compose(star)
        f = env.functions.get(name)
        # Update the quantifiers
        type_vars = []
        for arg_tv in f.usage.arg_types:
            type_vars = arg_tv.substitute(star).collect_type_vars(type_vars)
        Logger.debug(f'TVs in resulting function type before removing free TVs= {f.usage}: {type_vars}')

        # Remove free variables in env from the TVs we're going to quantify over
        free_env_type_vars = env.free_type_vars(
            lambda fun_name: fun_name != name
        )
        Logger.debug(f'Free TVs in env: {free_env_type_vars}')
        type_vars = [x for x in type_vars if x not in free_env_type_vars]
        Logger.debug(f'TVs after removing free TVs: {type_vars}')
        env.update_fun_quants(name, type_vars)

        f = env.functions.get(name)
        postponed = env.postponed_functions.pop(name, None)
        if postponed is not None:
            for (instance_type, inst_code_range) in postponed:
                ft = f.instantiate(env)
                args_len = len(instance_type.arg_types)
                tv_len = len(ft.usage.arg_types)
                if tv_len != args_len:
                    raise FunCallArgsMismatch(self.code_range, self.name.value, args_len, tv_len)
                for actual, instance in zip(ft.usage.arg_types, instance_type.arg_types):
                    Logger.debug(f'Postponed function signature check: {actual} <-> {instance}')
                    star = actual.unify_or_type_error(instance.substitute(star), inst_code_range).compose(star)
                    env.substitute(star)
                star = instance_type.return_type.substitute(star)\
                    .unify_or_type_error(ft.usage.return_type.substitute(star), inst_code_range)
                env.substitute(star)
        Logger.debug(f'- Finished typing function {name}\n')
        return star

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        context.push_scope()
        arg_ids = []
        for arg in self.arg_names.arg_names:  # Add fun arg names to current scope context
            arg_ids.append(context.add_variable(arg.value))
        self.arg_ids = arg_ids
        if self.fun_type:
            self.fun_type.binding_analysis(context, feedback)
        self.block.binding_analysis(context, feedback)
        context.pop_scope()
