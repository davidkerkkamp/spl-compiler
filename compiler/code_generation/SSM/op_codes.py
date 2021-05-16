from __future__ import annotations

from compiler.code_generation.SSM.Register import Register
from compiler.code_generation.generic.generator_utils import Function


class SSMOpCode:
    def __init__(self):
        pass

    def indent(self):
        if isinstance(self, MarkLabel):
            return '  '
        elif isinstance(self, MarkFunction):
            return ''
        return '    '


class Ldc(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ldc {self.i}'


class Lds(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}lds {self.i}'


class Ldms(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}ldms {self.i} {self.size}'


class Sts(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}sts {self.i}'


class Stms(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}stms {self.i} {self.size}'


class Ldsa(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ldsa {self.i}'


class Ldl(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ldl {self.i}'


class Ldml(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}ldml {self.i} {self.size}'


class Stl(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}stl {self.i}'


class Stml(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}stml {self.i} {self.size}'


class Ldla(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ldla {self.i}'


class Lda(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}lda {self.i}'


class Ldma(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}ldma {self.i} {self.size}'


class Ldaa(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ldaa {self.i}'


class Sta(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}sta {self.i}'


class Stma(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}stma {self.i} {self.size}'


class Ldr(SSMOpCode):
    def __init__(self, reg: Register):
        super().__init__()
        self.reg = reg

    def __str__(self):
        return f'{self.indent()}ldr {self.reg}'


class Ldrr(SSMOpCode):
    def __init__(self, reg1: Register, reg2: Register):
        super().__init__()
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return f'{self.indent()}ldrr {self.reg1} {self.reg2}'


class Str(SSMOpCode):
    def __init__(self, reg: Register):
        super().__init__()
        self.reg = reg

    def __str__(self):
        return f'{self.indent()}str {self.reg}'


class Swp(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}swp'


class Swpr(SSMOpCode):
    def __init__(self, reg: Register):
        super().__init__()
        self.reg = reg

    def __str__(self):
        return f'{self.indent()}swpr {self.reg}'


class Swprr(SSMOpCode):
    def __init__(self, reg1: Register, reg2: Register):
        super().__init__()
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return f'{self.indent()}swprr {self.reg1} {self.reg2}'


class Ajs(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ajs {self.i}'


class Add(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}add'


class Mul(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}mul'


class Sub(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}sub'


class Div(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}div'


class Mod(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}mod'


class And(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}and'


class Or(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}or'


class Xor(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}xor'


class Eq(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}eq'


class Ne(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}ne'


class Lt(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}lt'


class Le(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}le'


class Gt(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}gt'


class Ge(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}ge'


class Neg(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}neg'


class Not(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}not'


class Bsr(SSMOpCode):
    def __init__(self, f: Function):
        super().__init__()
        self.f = f

    def __str__(self):
        return f'{self.indent()}bsr {self.f}'


class Bra(SSMOpCode):
    def __init__(self, l: str):
        super().__init__()
        self.l = l

    def __str__(self):
        return f'{self.indent()}bra {self.l}'


class Brf(SSMOpCode):
    def __init__(self, l: str):
        super().__init__()
        self.l = l

    def __str__(self):
        return f'{self.indent()}brf {self.l}'


class Brt(SSMOpCode):
    def __init__(self, l: str):
        super().__init__()
        self.l = l

    def __str__(self):
        return f'{self.indent()}brt {self.l}'


class Jsr(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}jsr'


class Ret(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}ret'


class Link(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}link {self.i}'


class Unlink(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}unlink'


class Nop(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}nop'


class Halt(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}halt'


class Trap(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}trap {self.i}'


class Annote(SSMOpCode):
    def __init__(self, reg: Register, l_off: int, h_off: int, color: str, text: str):
        super().__init__()
        self.reg = reg
        self.l_off = l_off
        self.h_off = h_off
        self.color = color
        self.text = text

    def __str__(self):
        return f'{self.indent()}annote {self.reg} {self.l_off} {self.h_off} {self.color} "{self.text}"'


class Ldh(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}ldh {self.i}'


class Ldmh(SSMOpCode):
    def __init__(self, i: int, size: int):
        super().__init__()
        self.i = i
        self.size = size

    def __str__(self):
        return f'{self.indent()}ldmh {self.i} {self.size}'


class Sth(SSMOpCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.indent()}sth'


class Stmh(SSMOpCode):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self):
        return f'{self.indent()}stmh {self.i}'


class MarkFunction(SSMOpCode):
    def __init__(self, l: str):
        super().__init__()
        self.l = l

    def __str__(self):
        return f'{self.indent()}f_{self.l}: '


class MarkLabel(SSMOpCode):
    def __init__(self, l: str):
        super().__init__()
        self.l = l

    def __str__(self):
        return f'{self.indent()}{self.l}: '
