from abc import ABC, abstractmethod
from typing import List, Dict, Union

from compiler.compiler_warnings import CompilerWarning
from compiler.errors import BindingError


class Context:
    def __init__(self):
        self.variables: List[Dict[str, int]] = []
        self.functions = {}
        self.types: List[Dict[str, int]] = []
        self.counter = 0

    def get_variable(self, var: str):
        for scope in reversed(self.variables):
            v = scope.get(var)
            if v is not None:
                return v
        return None

    def get_variable_current_scope(self, var: str):
        return self.variables[-1].get(var)

    def add_variable(self, var: str):
        if self.variables[-1].get(var):
            raise Exception(f'Variable {var} is already defined in current scope')
        new_tv = self.counter
        self.variables[-1][var] = new_tv
        self.counter += 1
        return new_tv

    def get_or_add_type(self, name: str):
        for scope in reversed(self.types):
            v = scope.get(name)
            if v is not None:
                return v
        # Doesn't exist, add new
        new_tv = self.counter
        self.types[-1][name] = new_tv
        self.counter += 1
        return new_tv

    def has_type(self, name: str):
        for scope in reversed(self.types):
            if name in scope:
                return True
        return False

    def collect_variables(self):
        return [v for scope in self.variables for v in scope]

    def collect_functions(self):
        return list(self.functions)

    def add_function(self, name: str):
        self.functions[name] = 0

    def has_function(self, name: str):
        return self.functions.get(name) is not None

    def push_scope(self):
        self.variables.append({})
        self.types.append({})

    def pop_scope(self):
        del self.variables[-1]
        del self.types[-1]


class BindingAnalyzable(ABC):
    @abstractmethod
    def binding_analysis(self, context: Context, feedback: Dict[str, Union[List[BindingError], List[CompilerWarning]]]):
        pass
