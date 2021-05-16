from typing import List, Dict

from compiler.AST.base import SPL, Decl
from compiler.AST.declarations import VarDecl, FunDecl
from compiler.analysis.binding import BindingAnalyzable, Context
from compiler.analysis.typing import TypeInferrable, Env
from compiler.analysis.unification import InferenceType, Subst

# SPLFile - top node
from compiler.errors import DuplicateFunctionError, DuplicateIdentifierError, UnknownVarTypeError


class SPLFile(SPL, TypeInferrable, BindingAnalyzable):
    def __init__(self, declarations: List[Decl]):
        super().__init__()
        self.declarations = declarations

    def pretty_print(self, i=0):
        return ''.join([x.indented_print(i) + '\n' for index, x in enumerate(self.declarations)])

    def infer_type(self, env: Env, sigma: InferenceType):
        env.global_var_ids = [x.id_number for x in self.declarations if isinstance(x, VarDecl)]
        subst = Subst.empty()
        for d in self.declarations:
            subst = subst.compose(d.infer_type(env, sigma))
            env.substitute(subst)

        tv_globals = env.get_globals_with_tv()
        for (g, tv) in tv_globals:
            for d in self.declarations:
                if isinstance(d, VarDecl) and d.id_number == g:
                    raise UnknownVarTypeError(d.code_range, tv, d.name.value)

        return subst

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        has_main = False
        context.push_scope()
        # Add all global function and variable names to context
        for decl in self.declarations:
            if isinstance(decl, VarDecl):
                if context.get_variable_current_scope(decl.name.value) is not None:
                    feedback['errors'] = [] if feedback.get('errors') is None else feedback['errors']
                    feedback['errors'].append(
                        DuplicateIdentifierError(decl.name.code_range, decl.name.value))
                context.add_variable(decl.name.value)
            elif isinstance(decl, FunDecl):
                if decl.name.value == 'main':
                    has_main = True
                if context.has_function(decl.name.value):
                    feedback['errors'] = [] if feedback.get('errors') is None else feedback['errors']
                    feedback['errors'].append(
                        DuplicateFunctionError(decl.name.code_range, decl.name.value))
                context.add_function(decl.name.value)
            else:
                raise Exception('Unknown declaration')
        # Program needs a main function
        if not has_main:
            raise Exception('Function \'main\' is required but was not found')
        # Now perform binding analysis
        for decl in self.declarations:
            decl.binding_analysis(context, feedback)
        context.pop_scope()
