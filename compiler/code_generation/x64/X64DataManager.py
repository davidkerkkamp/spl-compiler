from __future__ import annotations

import copy
import itertools
from typing import List, Dict

import compiler.code_generation.x64.Operand as operand
import compiler.code_generation.generic.generator_utils as gen_utils
from compiler.code_generation.x64.Mnemonic import Mnemonic
from compiler.code_generation.x64.Instruction import Instruction
from compiler.code_generation.x64.Reg import Reg


class X64Data:
    def __init__(self):
        pass

    def to_operand(self):
        pass

    def equals(self, other: X64Data):
        return False


class StackLocal(X64Data):
    def __init__(self, offset: int):
        super().__init__()
        self.offset = offset

    def equals(self, other: X64Data):
        return isinstance(other, StackLocal) and other.offset == self.offset

    def to_operand(self):
        return operand.IndirectDisplaced(Reg.RBP, (self.offset * 8), operand.OperandSize.Qword)


class Register(X64Data):
    def __init__(self, reg: Reg):
        super().__init__()
        self.reg = reg

    def equals(self, other: X64Data):
        return isinstance(other, Register) and other.reg == self.reg

    def to_operand(self):
        return operand.Direct(self.reg)


# class Label(X64Data):
#     def __init__(self, name: str):
#         super().__init__()
#         self.name = name
#
#     def equals(self, other: X64Data):
#         return isinstance(other, Label) and other.name == self.name


class Constant(X64Data):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def equals(self, other: X64Data):
        return isinstance(other, Constant) and other.i == self.i

    def to_operand(self):
        return operand.Literal(self.i)


class X64DataManager:
    ALL_REGISTERS = [
        Reg.R12,
        Reg.R13,
        Reg.R14,
        Reg.R15,
        Reg.R10,
        Reg.RBX,
        Reg.R11,
        Reg.RAX,
        Reg.R9,
        Reg.R8,
        Reg.RCX,
        Reg.RDX,
        Reg.RSI,
        Reg.RDI
    ]
    ARGUMENT_REGISTERS = [Reg.RDI, Reg.RSI, Reg.RDX, Reg.RCX, Reg.R8, Reg.R9]

    def __init__(self, num_args: int, locals_space: int):
        self.stack: List[X64Data] = []
        self.reserved_registers: List[Reg] = []
        self.args: List[X64Data] = []
        self.max_stack_used = 0
        self.locals_space = locals_space
        self.label_counter = 0
        self.current_stack_alignment = 8  # 8 initially upon entrance of function because return address is pushed first
        self.restore_points: Dict[int, List[X64Data]] = {}

        for i in range(num_args):
            d = Register(X64DataManager.ARGUMENT_REGISTERS[i]) \
                if i < len(X64DataManager.ARGUMENT_REGISTERS) \
                else StackLocal(((i + 2) - len(X64DataManager.ARGUMENT_REGISTERS)))
            self.args.append(d)

    def is_aligned(self):
        return self.current_stack_alignment % 16 == 0

    def add_push_instr(self, insts: List[Instruction], operand: operand.Operand):
        self.current_stack_alignment += 8
        insts.append(Instruction(Mnemonic.PUSH, operand))

    def add_pop_instr(self, insts: List[Instruction], operand: operand.Operand):
        self.current_stack_alignment -= 8
        insts.append(Instruction(Mnemonic.POP, operand))

    def fresh_label(self, fun_inst: gen_utils.FunctionInstance):
        self.label_counter += 1
        return gen_utils.Label(self.label_counter).get_distinct_name(fun_inst) + '_f'

    def push(self, data: X64Data):
        if isinstance(data, StackLocal) and data.offset <= 0 and self.max_stack_used < -data.offset:
            self.max_stack_used = -data.offset
        self.stack.append(data)

    def push_arg(self, i: int):
        self.push(self.args[i])

    def pop(self):
        return self.stack.pop()

    def reserve_if_register(self, val: X64Data):
        assert not isinstance(val, Reg)
        if isinstance(val, Register):
            self.reserve_register(val.reg)

    def reserve_register(self, reg: Reg):
        self.reserved_registers.append(reg)

    def release_if_register(self, val: X64Data):
        assert not isinstance(val, Reg)
        if isinstance(val, Register):
            self.release_register(val.reg)

    def release_register(self, reg: Reg):
        for i, r in enumerate(self.reserved_registers):
            if r == reg:
                self.reserved_registers.pop(i)
                return

    # Allocate room on the stack
    def allocate_stack_space(self):
        pos = self.locals_space + 1
        while True:
            new_stack_val = StackLocal(-pos)
            same = len([x for x in itertools.chain(self.stack, self.args) if x.equals(new_stack_val)])
            if same == 0:
                if self.max_stack_used < pos:
                    self.max_stack_used = pos
                return new_stack_val
            pos += 1

    # Find a free register and return it. If none are free, make one free by moving something to stack
    def find_free_register(self, insts: List[Instruction], allowed_regs: List[Reg]):
        for reg in allowed_regs:
            occs = len([r for r in itertools.chain(self.stack, self.args) if isinstance(r, Register) and r.reg == reg])
            if occs == 0 and reg not in self.reserved_registers:
                return reg

        # No unused registers, so make one
        for v in itertools.chain(self.stack, self.args):
            if isinstance(v, Register) and v.reg in allowed_regs and v.reg not in self.reserved_registers:
                stack_val = self.allocate_stack_space()
                self.move_register_to_stack_val(insts, v.reg, stack_val)
                return self.find_free_register(insts, allowed_regs)
        raise Exception('Unable to find a free register')

    # Move given register content to a free register to clear given register
    def clear_register(self, insts: List[Instruction], reg: Reg):
        free_reg = None  # Defer finding free reg until actually needed
        for index, value in enumerate(self.stack):
            if isinstance(value, Register) and value.reg == reg:
                if free_reg is None:
                    free_reg = self.find_free_register(insts, X64DataManager.ALL_REGISTERS)
                self.stack[index] = Register(free_reg)
        for index, value in enumerate(self.args):  # Also for arguments
            if isinstance(value, Register) and value.reg == reg:
                if free_reg is None:
                    free_reg = self.find_free_register(insts, X64DataManager.ALL_REGISTERS)
                self.args[index] = Register(free_reg)
        if free_reg is not None:
            insts.append(Instruction(Mnemonic.MOV, operand.Direct(free_reg), operand.Direct(reg)))

    # Copy value from virtual stack to register
    def copy_to_register(self, insts: List[Instruction], offset: int, allowed_regs: List[Reg]):
        stack_offset = len(self.stack) - 1 - offset
        stack_item = self.stack[stack_offset]
        if isinstance(stack_item, Register):
            occs = len([x for x in itertools.chain(self.stack, self.args) if
                        isinstance(x, Register) and x.reg == stack_item.reg])
            if stack_item.reg in allowed_regs and occs == 1:
                # Only 1 occurence of this register on stack, so no need to move
                return stack_item.reg
        free_reg = self.find_free_register(insts, allowed_regs)
        insts.append(Instruction(Mnemonic.MOV, operand.Direct(free_reg), stack_item.to_operand()))
        self.stack[stack_offset] = Register(free_reg)
        return free_reg

    # Move value from virtual stack to register, return register
    def move_to_register(self, insts: List[Instruction], offset: int, allowed_regs: List[Reg]):
        stack_offset = len(self.stack) - 1 - offset
        stack_item = self.stack[stack_offset]
        if isinstance(stack_item, Register) and stack_item.reg in allowed_regs:
            return stack_item.reg  # Already in allowed reg

        return self.move_stack_val_to_register(insts, stack_item, allowed_regs)

    # Move value from virtual stack to register, return register
    def move_stack_val_to_register(self, insts: List[Instruction], value: X64Data, allowed_regs: List[Reg]):
        free_reg = self.find_free_register(insts, allowed_regs)
        insts.append(Instruction(Mnemonic.MOV, operand.Direct(free_reg), value.to_operand()))

        for index, v in enumerate(self.stack):
            if v.equals(value):  # Update references on virtual stack
                self.stack[index] = Register(free_reg)
        for index, v in enumerate(self.args):
            if v.equals(value):  # Update references in args
                self.args[index] = Register(free_reg)
        return free_reg

    # Move register to virtual stack
    def move_register_to_stack_val(self, insts: List[Instruction], reg: Reg, value: X64Data):
        insts.append(Instruction(Mnemonic.MOV, value.to_operand(), operand.Direct(reg)))

        for index, v in enumerate(self.stack):
            if isinstance(v, Register) and v.reg == reg:
                self.stack[index] = value  # Update references on virtual stack
        for index, v in enumerate(self.args):
            if isinstance(v, Register) and v.reg == reg:
                self.args[index] = value  # Update references in args

    def restore_arguments(self, insts: List[Instruction], label: gen_utils.Label):
        assert len(self.stack) == 0, 'Stack must be empty when restoring arguments'
        if (args := self.restore_points.get(label.id)) is not None:
            assert len(self.args) == len(args), 'Error while restoring arguments: lengths are not the same!'
            diff = [i for i, (x, y) in enumerate(zip(args, copy.copy(self.args))) if not x.equals(y)]
            if len(diff) == 0:
                return  # Arguments are the same already, no need to restore anything

            num_reserved_push = 0
            for i in diff:
                from_arg = self.args[i]
                to_arg = args[i]
                if isinstance(to_arg, Register):
                    num_reserved_push += 1
                    self.move_stack_val_to_register(insts, from_arg, [to_arg.reg])
                    self.reserved_registers.append(to_arg.reg)
                elif isinstance(to_arg, StackLocal):
                    tmp_reg = self.move_stack_val_to_register(insts, from_arg, self.ALL_REGISTERS)
                    insts.append(Instruction(Mnemonic.MOV, to_arg.to_operand(), operand.Direct(tmp_reg)))
                else:
                    raise Exception('Argument cannot be a constant')
            for _ in range(num_reserved_push):
                self.reserved_registers.pop()
        else:
            self.restore_points[label.id] = copy.copy(self.args)
