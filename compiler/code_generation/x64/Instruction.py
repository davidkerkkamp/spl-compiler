from compiler.code_generation.x64.Mnemonic import Mnemonic
from compiler.code_generation.x64.Operand import Operand


class Instruction:
    def __init__(self, inst: Mnemonic, op1: Operand = None, op2: Operand = None, op3: Operand = None):
        self.inst = inst
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __str__(self):
        ops = [
            str(self.op1) if self.op1 is not None else '',
            str(self.op2) if self.op2 is not None else '',
            str(self.op3) if self.op3 is not None else ''
        ]
        op_str = ', '.join(o for o in ops if len(o) > 0)
        return f'{str(self.inst)}    {op_str}'
