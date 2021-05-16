from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from compiler.analysis.unification import InferenceType
from compiler.code_generation.generic.OpCodeBuilder import OpCodeBuilder


class Local:
    def __init__(self, id: int):
        self.id = id

    def offset(self):
        return self.id


class Global:
    def __init__(self, id: int):
        self.id = id

    def offset(self):
        return self.id


class Function:
    def __init__(self, ident: str, num_args: int):
        self.ident = ident
        self.num_args = num_args

    def __str__(self):
        return f'f_{self.ident}'


class Label:
    def __init__(self, id: int):
        self.id = id

    def get_distinct_name(self, fun_inst: FunctionInstance):
        return f'lbl_{fun_inst.create_identifier()}_{self.id}'


class FunctionInstance:
    def __init__(self, name: str, arg_types: List[InferenceType], hide_from_user: bool = False, entry_point=False):
        self.name = name
        self.arg_types = arg_types
        self.hide_from_user = hide_from_user
        self.entry_point = entry_point

    def create_identifier(self):
        if self.entry_point:
            return self.name
        hide = '' if self.hide_from_user else '_'
        args = '_'.join([str(a) for a in self.arg_types])
        raw_ident = f'{hide}{self.name}_{len(self.arg_types)}_{args}'
        ident = ''
        for i in raw_ident:
            ident += {
                '(': '_PO_',
                ')': '_PC_',
                '[': '_BO_',
                ']': '_BC_',
                ',': '_CM_',
                ' ': '_',
            }.get(i, i)
        return ident


class FunctionImpl:
    def __init__(self, ops):
        self.ops = ops


class CodeGenerator(ABC):
    @abstractmethod
    def generate_code(self, code_builder: OpCodeBuilder):
        pass


class StorageCodeGenerator(ABC):
    @abstractmethod
    def generate_storage_code(self, code_builder: OpCodeBuilder):
        pass