from typing import Dict, List

import compiler.code_generation.generic.generator_utils as gen_utils
from compiler.analysis.ReturnValueAnalyzable import ReturnValueAnalyzable
from compiler.analysis.binding import BindingAnalyzable, Context
from compiler.analysis.typing import TypeInferrable, Env
from compiler.analysis.unification import InferenceType, Subst
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.compiler_warnings import CompilerWarning
from compiler.utils import CodeRange


def get_indent(i):
    return ''.join(['    ' for _ in range(i)])


# Base class
class SPL:
    def __init__(self):
        self.code_range = None

    def with_code_range(self, code_range: CodeRange):
        self.code_range: CodeRange = code_range
        return self

    def indented_print(self, indent=0):
        return get_indent(indent) + self.pretty_print(indent)

    def pretty_print(self, i=0):
        return self.__str__()


class Text(SPL):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def pretty_print(self, i=0):
        return self.value


# In case of an error during parsing, this node is used as placeholder
class Error(SPL):
    def __init__(self):
        super().__init__()

    def pretty_print(self, i=0):
        return '{Error!}'


# Decl base class
class Decl(SPL, TypeInferrable, BindingAnalyzable):
    def __init__(self):
        super().__init__()

    def infer_type(self, env: Env, sigma: InferenceType):
        return Subst.empty()

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        pass


# Expr base class
class Expr(SPL, TypeInferrable, BindingAnalyzable, gen_utils.CodeGenerator):
    def __init__(self):
        super().__init__()

    def infer_type(self, env: Env, sigma: InferenceType):
        return Subst.empty()

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        pass

    def generate_code(self, code_builder: OpCodeBuilder):
        pass


# Statement base class
class Statement(SPL, TypeInferrable, BindingAnalyzable, ReturnValueAnalyzable, gen_utils.CodeGenerator):
    def __init__(self):
        super().__init__()

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        pass

    def infer_type(self, env: Env, sigma: InferenceType):
        return Subst.empty()

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return False, False

    def generate_code(self, code_builder: OpCodeBuilder):
        pass


# Field base class
class Field(SPL, TypeInferrable, BindingAnalyzable, gen_utils.CodeGenerator, gen_utils.StorageCodeGenerator):
    def __init__(self):
        super().__init__()

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        pass

    def infer_type(self, env: Env, sigma: InferenceType):
        return Subst.empty()

    def generate_code(self, code_builder: OpCodeBuilder):
        pass

    def generate_storage_code(self, code_builder: OpCodeBuilder):
        pass