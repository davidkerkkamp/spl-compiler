from compiler.utils import CodeRange, Colors


class CompilerWarning(Exception):
    def __init__(self, code_range: CodeRange):
        self.code_range = code_range

    def print_warning(self, class_name, message: str):
        return f'{Colors.WARNING}{class_name}: {message} at: \n{self.code_range}{Colors.ENDC}'


class VariableHidingWarning(CompilerWarning):
    def __init__(self, code_range: CodeRange, var_name: str):
        super().__init__(code_range)
        self.var_name = var_name

    def __str__(self):
        return self.print_warning(self.__class__.__name__,
                                  f'Variable declaration of \'{self.var_name}\' '
                                  f'hides variable \'{self.var_name}\' from outer scope')


class UnreachableCodeWarning(CompilerWarning):
    def __init__(self, code_range: CodeRange):
        super().__init__(code_range)

    def __str__(self):
        return self.print_warning(self.__class__.__name__, f'Code is unreachable')
