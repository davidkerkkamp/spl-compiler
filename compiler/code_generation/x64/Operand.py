from enum import Enum, auto

from compiler.code_generation.x64.Reg import Reg


class OperandSize(Enum):
    Unsized = auto(),
    Byte = auto(),  # 8 - bit
    Word = auto(),  # 16 - bit
    Dword = auto(),  # 32 - bit
    Far16 = auto(),  # 16: 16
    Fword = auto(),  # 48 - bit
    Far32 = auto(),  # 16: 32
    Qword = auto(),  # 64 - bit
    Tbyte = auto(),  # 80 - bit
    Far64 = auto(),  # 16: 64
    Xmmword = auto(),  # 128 - bit
    Ymmword = auto(),  # 256 - bit
    Zmmword = auto(),  # 512 - bit

    def __str__(self):
        return self.name.lower()


class SegmentReg(Enum):
    CS = auto(),
    DS = auto(),
    ES = auto(),
    FS = auto(),
    GS = auto(),
    SS = auto()


class Operand:
    def __init__(self):
        pass


class Direct(Operand):
    def __init__(self, reg: Reg):
        super().__init__()
        self.reg = reg

    def __str__(self):
        return str(self.reg)


class Indirect(Operand):
    def __init__(self, reg: Reg, op_size: OperandSize = None, seg: SegmentReg = None):
        super().__init__()
        self.reg = reg
        self.op_size = op_size
        self.seg = seg

    def __str__(self):
        op_sz_str = str(self.op_size) if self.op_size is not None else ''
        return f'{op_sz_str} [{str(self.reg)}]'


class IndirectDisplaced(Operand):
    def __init__(self, reg: Reg, disp: int, op_size: OperandSize = None, seg: SegmentReg = None):
        super().__init__()
        self.reg = reg
        self.disp = disp
        self.op_size = op_size
        self.seg = seg

    def __str__(self):
        op_sz_str = str(self.op_size) if self.op_size is not None else ''
        disp_str = f'+ {self.disp}' if self.disp >= 0 else f'- {abs(self.disp)}'
        return f'{op_sz_str} [{str(self.reg)} {disp_str}]'


class IndirectVar(Operand):
    def __init__(self, var_name: str, op_size: OperandSize = None, seg: SegmentReg = None):
        super().__init__()
        self.var_name = var_name
        self.op_size = op_size
        self.seg = seg

    def __str__(self):
        op_sz_str = str(self.op_size) if self.op_size is not None else ''
        return f'{op_sz_str} [{self.var_name}]'

class Literal(Operand):
    def __init__(self, lit: int):
        super().__init__()
        self.lit = lit

    def __str__(self):
        return str(self.lit)


class Label(Operand):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name
