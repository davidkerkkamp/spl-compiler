from enum import Enum, auto


class Reg(Enum):
    R12 = auto(),
    R13 = auto(),
    R14 = auto(),
    R15 = auto(),
    RCX = auto(),
    RBX = auto(),
    R11 = auto(),
    RAX = auto(),
    R9 = auto(),
    R8 = auto(),
    R10 = auto(),
    RDX = auto(),
    RSI = auto(),
    RDI = auto(),
    RSP = auto(),
    RBP = auto()

    def __str__(self):
        return self.name
