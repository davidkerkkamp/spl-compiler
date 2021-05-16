from compiler.AST.spl_file import SPLFile
from compiler.AST.types import VoidReturn
from compiler.AST.declarations import FunDecl
from compiler.errors import NotAllPathsReturnError


class ReturnValueChecker:
    def check_spl_file(self, spl: SPLFile):
        warnings, errors = [], []
        for decl in spl.declarations:
            if isinstance(decl, FunDecl):
                contains_return, all_return = decl.block.all_paths_return(warnings)
                if decl.fun_type:
                    if isinstance(decl.fun_type.return_type, VoidReturn):
                        continue  # Ret types will be checked in type inference, missing returns no problem
                    if not all_return:
                        errors.append(NotAllPathsReturnError(decl.code_range, decl.name.value))
                else:  # No fun type
                    if contains_return is not all_return:  # Not all paths return
                        errors.append(NotAllPathsReturnError(decl.code_range, decl.name.value))

        return warnings, errors
