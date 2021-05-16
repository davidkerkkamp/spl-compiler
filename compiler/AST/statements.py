from typing import Dict, List

import compiler.AST.base as base
import compiler.AST.declarations as decl
from compiler.AST.base import Expr, Statement, Field, Decl
from compiler.analysis.ReturnValueAnalyzable import ReturnValueAnalyzable
from compiler.analysis.binding import BindingAnalyzable, Context
from compiler.analysis.typing import TypeInferrable, Env
from compiler.analysis.unification import InferenceType, Subst, InferenceBool, InferenceVoid
from compiler.code_generation.generic.generator_utils import CodeGenerator
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder
from compiler.compiler_warnings import CompilerWarning, UnreachableCodeWarning, VariableHidingWarning
from compiler.errors import DuplicateIdentifierError
import compiler.code_generation.generic.op_codes as codes


class Block(base.SPL, TypeInferrable, BindingAnalyzable, ReturnValueAnalyzable, CodeGenerator):
    def __init__(self, statements: List[Statement]):
        super().__init__()
        self.statements = statements

    def pretty_print(self, i=0):
        stmts = ''.join([x.indented_print(i + 1) + ('\n' if index + 1 < len(self.statements) else '')
                         for index, x in enumerate(self.statements)])
        return f'{{\n{stmts}\n{base.get_indent(i)}}}\n'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        context.push_scope()
        for stmt in self.statements:
            stmt.binding_analysis(context, feedback)
        context.pop_scope()

    def infer_type(self, env: Env, sigma: InferenceType):
        subst = Subst.empty()
        for stmt in self.statements:
            subst = subst.compose(stmt.infer_type(env, sigma.substitute(subst)))
            env.substitute(subst)
        return subst

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        contains_return, all_return = False, False
        for stmt in self.statements:
            if all_return:
                warnings.append(UnreachableCodeWarning(stmt.code_range))
                pass
            contains_return_stmt, all_return_stmt = stmt.all_paths_return(warnings)
            contains_return = contains_return or contains_return_stmt
            all_return = all_return or all_return_stmt
        return contains_return, all_return

    def generate_code(self, code_builder: OpCodeBuilder):
        for s in self.statements:
            s.generate_code(code_builder)


# ************************** Statements **************************

class If(Statement):
    def __init__(self, expression: Expr, then_block: Block, else_block: Block):
        super().__init__()
        self.expression = expression
        self.then_block = then_block
        self.else_block = else_block

    def pretty_print(self, i=0):
        else_str = f'{base.get_indent(i)}else\n{self.else_block.indented_print(i)}' if self.else_block is not None else ''
        return f'if({self.expression.pretty_print(i)})\n{self.then_block.indented_print(i)}{else_str}'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.expression.binding_analysis(context, feedback)
        self.then_block.binding_analysis(context, feedback)
        if self.else_block is not None:
            self.else_block.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        star1 = self.expression.infer_type(env, InferenceBool())
        env.substitute(star1)
        star2 = self.then_block.infer_type(env, sigma.substitute(star1)).compose(star1)
        if self.else_block is not None:
            env.substitute(star2)
            return self.else_block.infer_type(env, sigma.substitute(star2)).compose(star2)
        return star2

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        contains_return_then, all_return_then = self.then_block.all_paths_return(warnings)
        if self.else_block:
            contains_return_else, all_return_else = self.else_block.all_paths_return(warnings)
            return contains_return_then or contains_return_else, all_return_then and all_return_else
        return contains_return_then, False

    def generate_code(self, code_builder: OpCodeBuilder):
        end_label = code_builder.fresh_label()
        else_label = code_builder.fresh_label() if self.else_block is not None else end_label
        self.expression.generate_code(code_builder)
        code_builder.add(codes.BrFalse(else_label))
        self.then_block.generate_code(code_builder)
        if self.else_block is not None:
            code_builder.add(codes.Br(end_label))
            code_builder.mark(else_label)
            self.else_block.generate_code(code_builder)
        code_builder.mark(end_label)


class While(Statement):
    def __init__(self, expression: Expr, body: Block):
        super().__init__()
        self.expression = expression
        self.body = body

    def pretty_print(self, i=0):
        return f'while({self.expression.pretty_print(i)})\n{self.body.indented_print(i)}'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.expression.binding_analysis(context, feedback)
        self.body.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        star = self.expression.infer_type(env, InferenceBool())
        env.substitute(star)
        return self.body.infer_type(env, sigma.substitute(star)).compose(star)

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        contains_return, all_return = self.body.all_paths_return(warnings)
        return contains_return, False
        # return self.body.all_paths_return(warnings)

    def generate_code(self, code_builder: OpCodeBuilder):
        while_label = code_builder.fresh_label()
        end_label = code_builder.fresh_label()
        code_builder.mark(while_label)
        self.expression.generate_code(code_builder)
        code_builder.add(codes.BrFalse(end_label))
        self.body.generate_code(code_builder)
        code_builder.add(codes.Br(while_label))
        code_builder.mark(end_label)


class Assign(Statement):
    def __init__(self, field: Field, expression: Expr):
        super().__init__()
        self.field = field
        self.expression = expression

    def pretty_print(self, i=0):
        return f'{self.field.pretty_print(i)} = {self.expression.pretty_print(i)};'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.field.binding_analysis(context, feedback)
        self.expression.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        tv = env.fresh_type_var()
        star = self.field.infer_type(env, tv)
        return self.expression.infer_type(env, tv.substitute(star)).compose(star)

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return False, False

    def generate_code(self, code_builder: OpCodeBuilder):
        self.expression.generate_code(code_builder)
        self.field.generate_storage_code(code_builder)


class Return(Statement):
    def __init__(self, expression: Expr):
        super().__init__()
        self.expression = expression

    def pretty_print(self, i=0):
        expr = f' {self.expression.pretty_print(i)}' if self.expression is not None else ''
        return f'return{expr};'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        if self.expression is not None:
            self.expression.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        if self.expression is not None:
            return self.expression.infer_type(env, sigma)
        else:
            return sigma.unify_or_type_error(InferenceVoid(), self.code_range)

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return True, True

    def generate_code(self, code_builder: OpCodeBuilder):
        if self.expression is None:
            code_builder.add(codes.RetNoValue())
        else:
            self.expression.generate_code(code_builder)
            code_builder.add(codes.Ret())


class BlockStatement(Statement):
    def __init__(self, block: Block):
        super().__init__()
        self.block = block

    def pretty_print(self, i=0):
        return self.block.pretty_print(i)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.block.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        return self.block.infer_type(env, sigma)

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return self.block.all_paths_return(warnings)

    def generate_code(self, code_builder: OpCodeBuilder):
        self.block.generate_code(code_builder)


class DeclWrapper(Statement):
    def __init__(self, declaration: Decl):
        super().__init__()
        self.declaration = declaration

    def pretty_print(self, i=0):
        return self.declaration.pretty_print(i)

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        if isinstance(self.declaration, decl.VarDecl):
            name = self.declaration.name.value
            # if context.get_variable(name) is not None or name in context.functions or context.has_type(name):
            if context.get_variable_current_scope(name) is not None:
                feedback['errors'] = [] if feedback.get('errors') is None else feedback['errors']
                feedback['errors'].append(DuplicateIdentifierError(self.declaration.name.code_range, self.declaration.name.value))
            elif context.get_variable(name) is not None:  # Search all scopes
                feedback['warnings'] = [] if feedback.get('warnings') is None else feedback['warnings']
                feedback['warnings'].append(VariableHidingWarning(self.declaration.code_range, self.declaration.name.value))
                context.add_variable(name)
                self.declaration.binding_analysis(context, feedback)
            else:
                context.add_variable(name)
                self.declaration.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        return self.declaration.infer_type(env, sigma)

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return False, False

    def generate_code(self, code_builder: OpCodeBuilder):
        if isinstance(self.declaration, decl.VarDecl):
            self.declaration.expression.generate_code(code_builder)
            loc = code_builder.get_local(self.declaration.id_number)
            code_builder.add(codes.StLoc(loc))


class ExprWrapper(Statement):
    def __init__(self, expression: Expr):
        super().__init__()
        self.expression = expression

    def pretty_print(self, i=0):
        return self.expression.pretty_print(i) + ';'

    def binding_analysis(self, context: Context, feedback: Dict[str, list]):
        self.expression.binding_analysis(context, feedback)

    def infer_type(self, env: Env, sigma: InferenceType):
        return self.expression.infer_type(env, env.fresh_type_var())  # sigma is throw-away fresh tv

    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return False, False

    def generate_code(self, code_builder: OpCodeBuilder):
        self.expression.generate_code(code_builder)
        code_builder.add(codes.Pop())
