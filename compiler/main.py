import sys

from compiler.analysis.structure import ReturnValueChecker
from compiler.analysis.typing import Env
from compiler.analysis.unification import InferenceVoid, Subst
from compiler.code_generation.SSM.SSMGenerator import SSMGenerator
from compiler.code_generation.generic.GenericGenerator import GenericGenerator
from compiler.code_generation.generic.builtin.Add import Add
from compiler.code_generation.generic.builtin.IsEmpty import IsEmpty
from compiler.code_generation.generic.builtin.Len import Len
from compiler.code_generation.generic.builtin.Print import Print
from compiler.code_generation.generic.builtin.Eq import Eq
from compiler.code_generation.generic.builtin.PrintLn import PrintLn
from compiler.code_generation.generic.builtin.RefEq import RefEq
from compiler.code_generation.x64.X64Generator import X64Generator
from compiler.logging import Logger
from compiler.utils import InputHandler
from compiler.lexer import Lexer
from compiler.parser import *
from compiler.analysis.binding import Context


class Compiler:
    def __init__(self, verbosity='debug'):
        Logger.set_level(verbosity)
        self.builtins = [Print(), PrintLn(), Eq(), RefEq(), Len(), IsEmpty(), Add()]

    def get_builtin_str(self):
        return ', '.join([b.name for b in self.builtins])

    def parse_input(self, path: str):
        f = open(path, 'r')
        InputHandler.set_input_text(f.read())
        Logger.info('-------------------------------------------------------------')
        Logger.info('------------------- Starting parsing phase ------------------')
        Logger.info('-------------------------------------------------------------')
        lexer = Lexer()
        Logger.info('* Starting lexing')
        tokens = lexer.lex_input()
        Logger.info('- Lexing DONE')

        Logger.debug('*** Printing lexed tokens: ***')
        for i, t in enumerate(tokens):
            Logger.debug('{token_type}::{value}'.format(token_type=t.token_type, value=t.value))
        if len(lexer.lex_errors) > 0:
            for e in lexer.lex_errors:
                Logger.error(e)
            sys.exit(1)

        tr = TokenReader(tokens)
        parser = Parser(tr)
        Logger.info('* Starting parsing')
        ast = parser.parse_spl()
        Logger.info('- Parsing DONE')
        Logger.info('*** Pretty printing AST: ***')
        Logger.info('\n' + ast.indented_print())

        if len(parser.errors) > 0:
            for e in parser.errors:
                Logger.error(e)
            sys.exit(1)
        return ast

    def analysis(self, ast: SPLFile):
        Logger.info('-------------------------------------------------------------')
        Logger.info('------------------ Starting analysis phase ------------------')
        Logger.info('-------------------------------------------------------------')

        Logger.info('* Starting return value checking')
        rvc = ReturnValueChecker()
        return_warnings, return_errors = rvc.check_spl_file(ast)
        Logger.info('- Return value checking DONE')
        if len(return_warnings) > 0:
            for w in return_warnings:
                Logger.warning(w)
        if len(return_errors) > 0:
            for e in return_errors:
                Logger.error(e)
            sys.exit(1)
        context = Context()
        for b in self.builtins:
            b.add_to_context(context)
        Logger.info(f'- Added {len(self.builtins)} builtin functions to binding context: {self.get_builtin_str()}')

        binding_feedback = {'errors': [], 'warnings': []}
        Logger.info('* Starting binding analysis')
        ast.binding_analysis(context, binding_feedback)
        Logger.info('- Binding analysis DONE')

        Logger.info('*** Pretty printing AST with identifier IDs after binding analysis: ***')
        Logger.info('\n' + ast.indented_print())

        if len(binding_feedback['warnings']) > 0:
            for w in binding_feedback['warnings']:
                Logger.warning(w)
        if len(binding_feedback['errors']) > 0:
            for e in binding_feedback['errors']:
                Logger.error(e)
            sys.exit(1)

        env = Env()
        for b in self.builtins:
            b.add_to_env(env)
        Logger.info(f'- Added {len(self.builtins)} builtin functions to type environment: {self.get_builtin_str()}')
        subst = Subst.empty()
        Logger.info('* Starting type inference')
        try:
            subst = ast.infer_type(env, InferenceVoid())
        except Exception as e:
            Logger.error(str(e))
            # raise e
            sys.exit(1)
        env.substitute(subst)

        Logger.debug('* Inferred function types after inference:')
        for name, f in env.functions.items():
            Logger.debug(
                f'- {name} :: args: [{", ".join(str(a) for a in f.usage.arg_types)}], ret: {str(f.usage.return_type)}')
        Logger.debug('* Inferred variable types after inference:')
        for num, v in env.variables.items():
            Logger.debug(f'- {num} :: {str(v)}')

        Logger.info('- Typing DONE')
        return env

    def generate_generic_code(self, ast: SPLFile, env: Env):
        Logger.info('-------------------------------------------------------------')
        Logger.info('----------------- Starting code generation ------------------')
        Logger.info('-------------------------------------------------------------')
        Logger.info('* Starting generation of intermediate code')
        generic_functions_code = GenericGenerator(ast, env, self.builtins).generate()
        Logger.info('- Generation of intermediate code DONE')
        return generic_functions_code

    def generate_ssm_code(self, generic_functions_code: List, out_path: str):
        Logger.info('* Starting generation of SSM code')
        ssm_generator = SSMGenerator(generic_functions_code)
        ssm_generator.generate()
        Logger.info('- Generation of SSM code DONE')
        Logger.info(f'* Writing SSM code to file: {out_path}.ssm')
        ssm_generator.to_file(out_path + '.ssm')

    def generate_x64_code(self, generic_functions_code: List, out_path: str):
        Logger.info('* Starting generation of x86_64 code')
        gen = X64Generator(generic_functions_code)
        gen.generate_x64_instructions()
        Logger.info('- Generation of x86_64 code DONE')
        Logger.info(f'* Writing x86_64 code to file {out_path}.asm')
        gen.write_to_file(out_path + '.asm')
        Logger.info('* Assembling and linking x86_64 code')
        gen.assemble_and_link(out_path + '.asm', out_path)

    def compile(self, input_path: str, platform: str, out_path: str):
        ast = self.parse_input(input_path)
        env = self.analysis(ast)
        generic = self.generate_generic_code(ast, env)
        if platform == 'ssm':
            self.generate_ssm_code(generic, out_path)
        elif platform == 'x64':
            self.generate_x64_code(generic, out_path)
        else:
            Logger.error(f'Unknown target platform {platform}')
            sys.exit(1)
        print(f'Compilation of {input_path} to {out_path} succeeded')


if __name__ == "__main__":
    compiler = Compiler()
    compiler.compile('../input.spl', 'x64', '../out')
