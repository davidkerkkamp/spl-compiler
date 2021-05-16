from typing import List, Dict, Callable
from abc import ABC, abstractmethod
from compiler.analysis.unification import Subst, InferenceType, InferenceTypeVar
from compiler.utils import CodeRange


class BasicFunctionType:
    def __init__(self, arg_types=None, return_type=None):
        self.arg_types: List[InferenceType] = [] if arg_types is None else arg_types
        self.return_type: InferenceType = return_type

    def substitute(self, subst: Subst):
        return BasicFunctionType(
            [v.substitute(subst) for i, v in enumerate(self.arg_types)],
            self.return_type.substitute(subst)
        )

    def __str__(self):
        arg_strings = ', '.join([x.__str__() for x in self.arg_types])
        return f'arg_types: [{arg_strings}], return_type: {self.return_type}'


class FunctionInferenceType:
    def __init__(self, quantified_type_vars=None, usage=None):
        self.quantified_type_vars: List[int] = [] if quantified_type_vars is None else quantified_type_vars
        self.usage: BasicFunctionType = usage

    def substitute(self, subst: Subst):
        return FunctionInferenceType(
            self.quantified_type_vars,
            self.usage.substitute(subst)
        )

    def instantiate(self, env):
        subst = Subst({k: env.fresh_type_var() for i, k in enumerate(self.quantified_type_vars)})
        return self.substitute(subst)

    def collect_type_vars(self, result: List[int]):  # Append to given list and return result
        tmp = []
        for i, t in enumerate(self.usage.arg_types):
            tmp = t.collect_type_vars(tmp)
        tmp = self.usage.return_type.collect_type_vars(tmp)
        return result + [x for i, x in enumerate(tmp) if x not in self.quantified_type_vars]


class Env:
    def __init__(self):
        self.n = 0
        self.variables: Dict[int, InferenceType] = dict()
        self.functions: Dict[str, FunctionInferenceType] = dict()
        self.global_var_ids: List[int] = []
        self.postponed_functions: Dict[str, List[(BasicFunctionType, CodeRange)]] = dict()

    def substitute(self, subst: Subst):
        self.variables = {k: v.substitute(subst) for k, v in self.variables.items()}
        self.functions = {k: v.substitute(subst) for k, v in self.functions.items()}
        self.postponed_functions = {k: [(t.substitute(subst), c) for (t, c) in v] for k, v in self.postponed_functions.items()}

    def get_var(self, num: int, crash=False):
        try:
            return self.variables[num]
        except Exception as e:
            if crash:
                raise e
            tv = self.fresh_type_var()
            self.variables[num] = tv
            return tv

    def update_fun_quants(self, name: str, quants: List[int]):
        fun = self.functions.get(name)
        self.functions[name] = FunctionInferenceType(quants, fun.usage)

    def add_fun_usage(self, name: str, arg_types: List[InferenceType], return_type: InferenceType, code_range: CodeRange):
        if name not in self.postponed_functions:
            self.postponed_functions[name] = []
        lst = self.postponed_functions[name]
        lst.append((BasicFunctionType(arg_types, return_type), code_range))

    def add_fun(self, name: str, arg_ids: List[int]):
        args = [self.get_var(a) for a in arg_ids]
        ret = self.fresh_type_var()
        try:
            quant_type_vars = [a.num for a in args]  # a.num fails if a is not InferenceTypeVar
        except:
            raise Exception('All arguments should be type variables')
        ft = FunctionInferenceType(quant_type_vars, BasicFunctionType(args, ret))
        self.functions[name] = ft

    def free_type_vars(self, filter_fun: Callable[[str], bool]):
        res = []  # Uses reference to this list instead of return values of called functions below
        for name, f in self.functions.items():
            if filter_fun(name):
                res = f.collect_type_vars(res)
        for gv in self.global_var_ids:
            if (tv := self.variables.get(gv)) is not None:
                res = tv.collect_type_vars(res)
        return res

    def add_builtin(self, name: str, quants: List[InferenceTypeVar], arg_types: List[InferenceType],
                    ret_type: InferenceType):
        try:
            quant_type_vars = [a.num for i, a in enumerate(quants)]  # a.num fails if a is not InferenceTypeVar
        except:
            raise Exception('quants should all be type variables')
        ft = FunctionInferenceType(quant_type_vars, BasicFunctionType(arg_types, ret_type))
        self.functions[name] = ft

    def fresh_type_var(self):
        tv = InferenceTypeVar(self.n)
        self.n += 1
        return tv

    def get_globals_with_tv(self):
        tv_globals = []
        for g in self.global_var_ids:
            t = self.variables[g]
            # if isinstance(t, InferenceTypeVar):
            if t.contains_typevar(None):
                tv_globals.append((g, t))
        return tv_globals


class TypeInferrable(ABC):
    @abstractmethod
    def infer_type(self, env: Env, sigma: InferenceType) -> Subst:
        return Subst.empty()
