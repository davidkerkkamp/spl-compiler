from __future__ import annotations
import compiler.code_generation.generic.generator_utils as gen_utils


class GenericOpCode:
    pass


class Add(GenericOpCode):
    pass


class Call(GenericOpCode):
    def __init__(self, f: gen_utils.Function):
        self.f = f


class Ret(GenericOpCode):
    pass


class RetNoValue(GenericOpCode):
    pass


class LdLoc(GenericOpCode):
    def __init__(self, local: gen_utils.Local):
        self.local = local


class StLoc(GenericOpCode):
    def __init__(self, local: gen_utils.Local):
        self.local = local


class LdGlob(GenericOpCode):
    def __init__(self, glob: gen_utils.Global):
        self.glob = glob


class StGlob(GenericOpCode):
    def __init__(self, glob: gen_utils.Global):
        self.glob = glob


class Br(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrEq(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrNe(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrGe(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrGt(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrLe(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrLt(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrTrue(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class BrFalse(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class PushConst(GenericOpCode):
    def __init__(self, const: int):
        self.const = const


class CreateTuple(GenericOpCode):
    pass


class CreateListCons(GenericOpCode):
    pass


class CreateListNil(GenericOpCode):
    pass


class LdFld(GenericOpCode):
    def __init__(self, field_type):  # FieldType
        self.field_type = field_type


class StFld(GenericOpCode):
    def __init__(self, field_type):  # FieldType
        self.field_type = field_type


class And(GenericOpCode):
    pass


class Or(GenericOpCode):
    pass


class Div(GenericOpCode):
    pass


class Mul(GenericOpCode):
    pass


class Mod(GenericOpCode):
    pass


class Eq(GenericOpCode):
    pass


class Ne(GenericOpCode):
    pass


class Lt(GenericOpCode):
    pass


class Le(GenericOpCode):
    pass


class Gt(GenericOpCode):
    pass


class Ge(GenericOpCode):
    pass


class Neg(GenericOpCode):
    pass


class Not(GenericOpCode):
    pass


class Sub(GenericOpCode):
    pass


class Swp(GenericOpCode):
    pass


class Pop(GenericOpCode):
    pass


class MarkLabel(GenericOpCode):
    def __init__(self, label: gen_utils.Label):
        self.label = label


class PrintInt(GenericOpCode):
    pass


class PrintChar(GenericOpCode):
    pass


class Halt(GenericOpCode):
    pass