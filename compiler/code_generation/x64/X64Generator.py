import subprocess
from typing import List, Tuple, Dict

import compiler.code_generation.generic.op_codes as gen_codes
from compiler.AST.fields import FieldType
from compiler.code_generation.generic.generator_utils import FunctionImpl, FunctionInstance
from compiler.code_generation.x64.Mnemonic import Mnemonic
from compiler.code_generation.x64.Instruction import Instruction
import compiler.code_generation.x64.Operand as operand
from compiler.code_generation.x64.Reg import Reg
from compiler.code_generation.x64.X64DataManager import X64DataManager, Constant, StackLocal, Register
from compiler.code_generation.x64.global_data import BssVariable
from compiler.logging import Logger


class X64Generator:
    def __init__(self, functions: List[Tuple[FunctionInstance, FunctionImpl]]):
        self.functions = functions
        self.x64_code: Dict[str, List[Instruction]] = {}
        self.callee_preserved_regs = [Reg.RBX, Reg.R12, Reg.R13, Reg.R14, Reg.R15]
        self.caller_preserved_regs = [
            Reg.RAX,
            Reg.RDI,
            Reg.RSI,
            Reg.RDX,
            Reg.RCX,
            Reg.R8,
            Reg.R9,
            Reg.R10,
            Reg.R11,
        ]
        self.caller_preserved_regs_without_rax = self.caller_preserved_regs[1:]
        self.globals: Dict[int, BssVariable] = {}
        self.externals: Dict[str, bool] = {}

    def declare_globals(self, fun_impl: FunctionImpl):  # Create uninitialized var declarations for .bss section
        for gen_op in fun_impl.ops:
            if isinstance(gen_op, gen_codes.StGlob):
                self.globals[gen_op.glob.id] = BssVariable(gen_op.glob.id)

    def add_function_call(self, insts: List[Instruction], is_aligned: bool, fun_name: str):
        if is_aligned:
            insts.append(Instruction(Mnemonic.CALL, operand.Label(fun_name)))
        else:  # Align stack to 16 bytes
            insts.append(Instruction(Mnemonic.SUB, operand.Direct(Reg.RSP), operand.Literal(8)))
            insts.append(Instruction(Mnemonic.CALL, operand.Label(fun_name)))
            insts.append(Instruction(Mnemonic.ADD, operand.Direct(Reg.RSP), operand.Literal(8)))

    def generate_function_code(self, fun_instance: FunctionInstance, fun_impl: FunctionImpl):
        gen_type = 'entry point' if fun_instance.entry_point else 'function'
        Logger.debug(f'Generating code for {gen_type} \'{fun_instance.name}\' '
                     f'(instance: \'{fun_instance.create_identifier()}\')')
        if fun_instance.entry_point:
            self.declare_globals(fun_impl)
        insts = []
        local_vars_size = 0
        for op in fun_impl.ops:
            if isinstance(op, gen_codes.LdLoc):
                off = op.local.offset() + 1
                if off > local_vars_size:
                    local_vars_size = off
            elif isinstance(op, gen_codes.StLoc):
                off = op.local.offset() + 1
                if off > local_vars_size:
                    local_vars_size = off

        dm = X64DataManager(len(fun_instance.arg_types), local_vars_size)

        dm.add_push_instr(insts, operand.Direct(Reg.RBP))  # Save rbp
        insts.append(Instruction(Mnemonic.MOV, operand.Direct(Reg.RBP),
                                 operand.Direct(Reg.RSP)))  # Use rbp for access to local vars

        # Store object ref to update stack size later
        stack_size = local_vars_size * 8 if (local_vars_size * 8) % 16 == 0 else (local_vars_size * 8) + 8
        stack_size_op = operand.Literal(stack_size)
        insts.append(Instruction(Mnemonic.SUB, operand.Direct(Reg.RSP), stack_size_op))  # Make room for local vars

        # Push callee preserved regs to stack to be able to restore at function end
        for reg in self.callee_preserved_regs:
            dm.add_push_instr(insts, operand.Direct(reg))

        for op in fun_impl.ops:
            self.map_generic_to_ssm(fun_instance, dm, op, insts)
        self.x64_code['f_' + fun_instance.create_identifier() if not fun_instance.entry_point else '_main'] = insts

        # Update stack size after knowing how much was used
        stack_usage = dm.max_stack_used * 8
        if stack_usage > stack_size_op.lit:
            stack_size_op.lit = stack_usage if stack_usage % 16 == 0 else stack_usage + 8

    def map_generic_to_ssm(self, fun_inst: FunctionInstance, dm: X64DataManager,
                           gen_op: gen_codes.GenericOpCode, insts: List[Instruction]):
        if isinstance(gen_op, gen_codes.Add) \
                or isinstance(gen_op, gen_codes.Sub) \
                or isinstance(gen_op, gen_codes.And) \
                or isinstance(gen_op, gen_codes.Or)\
                or isinstance(gen_op, gen_codes.Mul):  # add, sub, and, or, mul op1 with op2, put result in op1 register
            op2 = dm.pop()
            dm.reserve_if_register(op2)
            dm.copy_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            op1 = dm.pop()
            dm.reserve_if_register(op1)
            if isinstance(gen_op, gen_codes.Add):
                instr = Mnemonic.ADD
            elif isinstance(gen_op, gen_codes.Sub):
                instr = Mnemonic.SUB
            elif isinstance(gen_op, gen_codes.And):
                instr = Mnemonic.AND
            elif isinstance(gen_op, gen_codes.Mul):
                instr = Mnemonic.IMUL
            else:
                instr = Mnemonic.OR
            insts.append(Instruction(instr, op1.to_operand(), op2.to_operand()))
            dm.push(op1)
            dm.release_if_register(op1)
            dm.release_if_register(op2)
        # elif isinstance(gen_op, gen_codes.Mul):  # multiply op1 and op2, put result in dest register
        #     op2 = dm.pop()
        #     dm.reserve_if_register(op2)
        #     dm.copy_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
        #     op1 = dm.pop()
        #     dm.reserve_if_register(op1)
        #     dest = dm.find_free_register(insts, X64DataManager.ALL_REGISTERS)
        #     insts.append(Instruction(Mnemonic.IMUL, operand.Direct(dest), op1.to_operand(), op2.to_operand()))
        #     dm.push(Register(dest))
        #     dm.release_if_register(op1)
        #     dm.release_if_register(op2)
        elif isinstance(gen_op, gen_codes.Div) or isinstance(gen_op, gen_codes.Mod):  # div and mod
            # IDIV divides RDX:RAX by first operand, puts result in RAX and remainder in RDX
            dm.reserve_register(Reg.RDX)  # divide value in RDX:RAX, so reserve RDX
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            divisor = dm.pop()
            dm.reserve_if_register(divisor)
            dm.copy_to_register(insts, 0, [Reg.RAX])
            val = dm.pop()
            dm.reserve_if_register(val)  # divide value in RDX:RAX, so reserve RAX
            insts.append(Instruction(Mnemonic.XOR, operand.Direct(Reg.RDX), operand.Direct(Reg.RDX)))  # Set RDX to 0
            insts.append(Instruction(Mnemonic.IDIV, divisor.to_operand()))
            reg_to_push = Reg.RAX if isinstance(gen_op, gen_codes.Div) else Reg.RDX  # If div, use RAX, if mod use RDX
            dm.push(Register(reg_to_push))
            dm.release_if_register(divisor)
            dm.release_if_register(val)
            dm.release_register(Reg.RDX)
        elif isinstance(gen_op, gen_codes.Eq) or isinstance(gen_op, gen_codes.Ge) \
                or isinstance(gen_op, gen_codes.Gt) or isinstance(gen_op, gen_codes.Le) \
                or isinstance(gen_op, gen_codes.Lt) or isinstance(gen_op, gen_codes.Ne):  # comparisons

            target = dm.find_free_register(insts, X64DataManager.ALL_REGISTERS)
            dm.reserve_register(target)
            op2 = dm.pop()
            dm.reserve_if_register(op2)
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            op1 = dm.pop()
            dm.reserve_if_register(op1)
            insts.append(Instruction(Mnemonic.XOR, operand.Direct(target), operand.Direct(target)))  # Set to 0 (False)
            insts.append(Instruction(Mnemonic.CMP, op1.to_operand(), op2.to_operand()))
            mov = Instruction(Mnemonic.MOV, operand.Direct(target), operand.Literal(-1))  # Set to -1 (True)

            if isinstance(gen_op, gen_codes.Eq):  # Decide which jump instruction to use
                m = Mnemonic.JNE  # Jump if not equal
            elif isinstance(gen_op, gen_codes.Ge):
                m = Mnemonic.JL  # Jump if less
            elif isinstance(gen_op, gen_codes.Gt):
                m = Mnemonic.JLE  # Jump if less or equal
            elif isinstance(gen_op, gen_codes.Le):
                m = Mnemonic.JG  # Jump if greater
            elif isinstance(gen_op, gen_codes.Lt):
                m = Mnemonic.JGE  # Jump if greater or equal
            elif isinstance(gen_op, gen_codes.Ne):
                m = Mnemonic.JE  # Jump if equal
            else:
                raise Exception('Should not happen')
            label = operand.Label(dm.fresh_label(fun_inst))
            insts.append(Instruction(m, label))  # add jump instr to jump to label
            insts.append(mov)  #
            insts.append(Instruction(Mnemonic.MARK_LABEL, label))  # Mark label to skip setting reg to -1
            dm.push(Register(target))
            dm.release_register(target)
            dm.release_if_register(op2)
            dm.release_if_register(op1)

        elif isinstance(gen_op, gen_codes.Not):
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.reserve_if_register(val)
            insts.append(Instruction(Mnemonic.NOT, val.to_operand()))
            dm.push(val)
            dm.release_if_register(val)
        elif isinstance(gen_op, gen_codes.Neg):  # replace val of op with 2's complement,
            # equivalent to subtracting op from 0
            dm.copy_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.reserve_if_register(val)
            if isinstance(val, Constant):
                dm.push(Constant(-val.i))
            else:
                insts.append(Instruction(Mnemonic.NEG, val.to_operand()))
                dm.push(val)
            dm.release_if_register(val)
        elif isinstance(gen_op, gen_codes.Swp):  # Swap two top values on virtual stack
            val1 = dm.pop()
            val2 = dm.pop()
            dm.push(val1)
            dm.push(val2)
        elif isinstance(gen_op, gen_codes.Pop):  # Pop value from virtual stack
            dm.pop()
        elif isinstance(gen_op, gen_codes.PushConst):  # Add constant to virtual stack
            dm.push(Constant(gen_op.const))
        elif isinstance(gen_op, gen_codes.Br):  # Jump to label
            dm.restore_arguments(insts, gen_op.label)
            insts.append(Instruction(Mnemonic.JMP, operand.Label(gen_op.label.get_distinct_name(fun_inst))))
        elif isinstance(gen_op, gen_codes.BrEq) or isinstance(gen_op, gen_codes.BrNe) \
                or isinstance(gen_op, gen_codes.BrGe) or isinstance(gen_op, gen_codes.BrGt)\
                or isinstance(gen_op, gen_codes.BrLe or isinstance(gen_op, gen_codes.BrLt)):
            op2 = dm.pop()
            dm.reserve_if_register(op2)
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            op1 = dm.pop()
            dm.reserve_if_register(op1)
            insts.append(Instruction(Mnemonic.CMP, op1.to_operand(), op2.to_operand()))
            dm.restore_arguments(insts, gen_op.label)

            if isinstance(gen_op, gen_codes.BrEq):
                mnemonic = Mnemonic.JE
            elif isinstance(gen_op, gen_codes.BrNe):
                mnemonic = Mnemonic.JNE
            elif isinstance(gen_op, gen_codes.BrGe):
                mnemonic = Mnemonic.JGE
            elif isinstance(gen_op, gen_codes.BrGt):
                mnemonic = Mnemonic.JG
            elif isinstance(gen_op, gen_codes.BrLe):
                mnemonic = Mnemonic.JLE
            elif isinstance(gen_op, gen_codes.BrLt):
                mnemonic = Mnemonic.JL
            else:
                raise Exception('Should not happen')
            insts.append(Instruction(mnemonic, gen_op.label.get_distinct_name(fun_inst)))
            dm.release_if_register(op1)
            dm.release_if_register(op2)
        elif isinstance(gen_op, gen_codes.BrTrue):
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.restore_arguments(insts, gen_op.label)
            insts.append(Instruction(Mnemonic.CMP, val.to_operand(), operand.Literal(0)))  # CMP with 0 (false)
            insts.append(Instruction(Mnemonic.JNE, gen_op.label.get_distinct_name(fun_inst)))  # Jump if not equal
        elif isinstance(gen_op, gen_codes.BrFalse):
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.restore_arguments(insts, gen_op.label)
            insts.append(Instruction(Mnemonic.CMP, val.to_operand(), operand.Literal(0)))  # CMP with 0 (false)
            insts.append(Instruction(Mnemonic.JE, gen_op.label.get_distinct_name(fun_inst)))  # Jump if equal
        elif isinstance(gen_op, gen_codes.MarkLabel):
            dm.restore_arguments(insts, gen_op.label)
            insts.append(Instruction(Mnemonic.MARK_LABEL, operand.Label(gen_op.label.get_distinct_name(fun_inst))))
        elif isinstance(gen_op, gen_codes.PrintInt):
            # Move int from virtual stack to SECOND arg register (RSI), first is for printf format
            dm.move_to_register(insts, 0, [X64DataManager.ARGUMENT_REGISTERS[1]])
            val = dm.pop()
            dm.reserve_if_register(val)
            for r in self.caller_preserved_regs:  # Save values in caller preserved registers
                dm.clear_register(insts, r)
                dm.reserve_register(r)
            # Load printf format into RDI (which is already cleared above)
            insts.append(Instruction(Mnemonic.LEA, operand.Direct(Reg.RDI), operand.IndirectVar('int_format')))
            self.add_function_call(insts, dm.is_aligned(), '_printf')
            self.externals['_printf'] = True
            for r in self.caller_preserved_regs:
                dm.release_register(r)
            dm.release_if_register(val)
        elif isinstance(gen_op, gen_codes.PrintChar):
            # Move char from virtual stack to first arg register (RDI)
            dm.move_to_register(insts, 0, [X64DataManager.ARGUMENT_REGISTERS[0]])
            val = dm.pop()
            dm.reserve_if_register(val)
            for r in self.caller_preserved_regs:  # Save values in caller preserved registers
                dm.clear_register(insts, r)
                dm.reserve_register(r)
            self.add_function_call(insts, dm.is_aligned(), '_putchar')  # Call C function 'putchar'
            self.externals['_putchar'] = True
            for r in self.caller_preserved_regs:
                dm.release_register(r)
            dm.release_if_register(val)
        elif isinstance(gen_op, gen_codes.Call):
            args_on_stack_bytes = 0
            for i in reversed(range(gen_op.f.num_args)):  # Place fun args in registers (and on stack)
                if i < len(X64DataManager.ARGUMENT_REGISTERS):
                    dm.move_to_register(insts, 0, [X64DataManager.ARGUMENT_REGISTERS[i]])
                    dm.pop()
                    dm.reserve_register(X64DataManager.ARGUMENT_REGISTERS[i])
                else:
                    dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
                    reg = dm.pop()
                    dm.reserve_if_register(reg)
                    dm.add_push_instr(insts, reg.to_operand())
                    args_on_stack_bytes += 8

            dm.clear_register(insts, Reg.RAX)
            dm.reserve_register(Reg.RAX)
            for r in self.caller_preserved_regs_without_rax:
                dm.clear_register(insts, r)
                dm.reserve_register(r)
            self.add_function_call(insts, dm.is_aligned(), str(gen_op.f))
            dm.push(Register(Reg.RAX))
            for r in self.caller_preserved_regs_without_rax:
                dm.release_register(r)

            if args_on_stack_bytes > 0:  # 'pop' arguments on stack
                insts.append(Instruction(Mnemonic.ADD, operand.Direct(Reg.RSP), operand.Literal(args_on_stack_bytes)))
                dm.current_stack_alignment -= args_on_stack_bytes

            dm.release_register(Reg.RAX)
            for i in reversed(range(gen_op.f.num_args)):
                if i < len(X64DataManager.ARGUMENT_REGISTERS):
                    dm.release_register(X64DataManager.ARGUMENT_REGISTERS[i])

        elif isinstance(gen_op, gen_codes.LdLoc):
            if gen_op.local.offset() < 0:
                dm.push_arg(len(fun_inst.arg_types) + gen_op.local.offset())  # Function argument
            else:
                dm.push(StackLocal(-gen_op.local.offset() - 1))  # Local variable
        elif isinstance(gen_op, gen_codes.StLoc):
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.reserve_if_register(val)
            if gen_op.local.offset() < 0:  # If offset < 0, then it's a function argument
                arg = dm.args[len(fun_inst.arg_types) + gen_op.local.offset()]
                insts.append(Instruction(Mnemonic.MOV, arg.to_operand(), val.to_operand()))
            else:  # Local variable
                insts.append(Instruction(Mnemonic.MOV,
                                         operand.IndirectDisplaced(Reg.RBP, (-gen_op.local.offset() - 1) * 8,
                                                                   operand.OperandSize.Qword), val.to_operand()))
            dm.release_if_register(val)

        elif isinstance(gen_op, gen_codes.LdGlob):
            reg = dm.find_free_register(insts, X64DataManager.ALL_REGISTERS)
            assert gen_op.glob.id in self.globals, f'Global with id {gen_op.glob.id} should be known, but isn\'t!'
            insts.append(Instruction(Mnemonic.MOV, operand.Direct(reg),
                                     operand.IndirectVar(self.globals[gen_op.glob.id].name, operand.OperandSize.Qword)))
            dm.push(Register(reg))
        elif isinstance(gen_op, gen_codes.StGlob):
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.reserve_if_register(val)
            assert gen_op.glob.id in self.globals, f'Global with id {gen_op.glob.id} should be known, but isn\'t!'
            insts.append(Instruction(Mnemonic.MOV, operand.IndirectVar(self.globals[gen_op.glob.id].name,
                                                                       operand.OperandSize.Qword), val.to_operand()))
            dm.release_if_register(val)

        elif isinstance(gen_op, gen_codes.CreateListCons) or isinstance(gen_op, gen_codes.CreateTuple):
            dm.clear_register(insts, Reg.RAX)  # Clear RAX because its used for result of malloc
            dm.reserve_register(Reg.RAX)
            dm.clear_register(insts, Reg.RDI)  # Clear RDI because its used for 1st arg of call to malloc
            dm.reserve_register(Reg.RDI)

            for r in self.caller_preserved_regs_without_rax:  # Clear registers that might be overwritten
                dm.clear_register(insts, r)
                dm.reserve_register(r)
            # We want to allocate space for 2 ints, so 16 bytes
            insts.append(Instruction(Mnemonic.MOV, operand.Direct(Reg.RDI), operand.Literal(16)))
            self.add_function_call(insts, dm.is_aligned(), '_malloc')  # Call C function malloc
            self.externals['_malloc'] = True  # Let compiler know to include extern _malloc
            for r in self.caller_preserved_regs_without_rax:
                dm.release_register(r)

            # First write second list/tuple element to offset 8 of 16, then first element to offset 0 of 16
            for offset in [8, 0]:
                dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
                val = dm.pop()
                dm.reserve_if_register(val)
                insts.append(Instruction(Mnemonic.MOV, operand.IndirectDisplaced(Reg.RAX, offset, operand.OperandSize.Qword),
                                         val.to_operand()))
                dm.release_if_register(val)
            dm.push(Register(Reg.RAX))  # Push address to virtual stack

            dm.release_register(Reg.RDI)
            dm.release_register(Reg.RAX)
        elif isinstance(gen_op, gen_codes.CreateListNil):
            dm.push(Constant(0))
        elif isinstance(gen_op, gen_codes.LdFld):
            reg = dm.find_free_register(insts, X64DataManager.ALL_REGISTERS)
            dm.clear_register(insts, reg)
            dm.reserve_register(reg)
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.reserve_if_register(val)

            op2_dis = {
                FieldType.Fst: 0,
                FieldType.Hd: 0,
                FieldType.Snd: 8,
                FieldType.Tl: 8,
            }.get(gen_op.field_type)
            assert isinstance(val, Register)
            insts.append(Instruction(Mnemonic.MOV, operand.Direct(reg),
                                     operand.IndirectDisplaced(val.reg, op2_dis, operand.OperandSize.Qword)))
            dm.push(Register(reg))
            dm.release_if_register(val)
            dm.release_register(reg)
        elif isinstance(gen_op, gen_codes.StFld):
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            val = dm.pop()
            dm.reserve_if_register(val)
            dm.move_to_register(insts, 0, X64DataManager.ALL_REGISTERS)
            addr = dm.pop()
            dm.reserve_if_register(addr)

            op_dis = {
                FieldType.Fst: 0,
                FieldType.Hd: 0,
                FieldType.Snd: 8,
                FieldType.Tl: 8,
            }.get(gen_op.field_type)
            assert isinstance(addr, Register)
            insts.append(Instruction(Mnemonic.MOV,
                                     operand.IndirectDisplaced(addr.reg, op_dis, operand.OperandSize.Qword),
                                     val.to_operand()))
            dm.release_if_register(val)
            dm.release_if_register(addr)
        elif isinstance(gen_op, gen_codes.Ret) or isinstance(gen_op, gen_codes.RetNoValue) \
                or isinstance(gen_op, gen_codes.Halt):

            if isinstance(gen_op, gen_codes.Ret):  # Move result to RAX before returning
                dm.move_to_register(insts, 0, [Reg.RAX])
                val = dm.pop()
                dm.reserve_if_register(val)

            # Pop callee preserved regs again to restore value
            for reg in reversed(self.callee_preserved_regs):
                dm.add_pop_instr(insts, operand.Direct(reg))

            # Restore stack pointer
            insts.append(Instruction(Mnemonic.MOV, operand.Direct(Reg.RSP), operand.Direct(Reg.RBP)))
            # Restore stack base pointer
            dm.add_pop_instr(insts, operand.Direct(Reg.RBP))
            insts.append(Instruction(Mnemonic.RET))

            if isinstance(gen_op, gen_codes.Ret):  # Release RAX
                dm.release_if_register(val)

    def generate_x64_instructions(self):
        for fun_inst, fun_impl in self.functions:
            self.generate_function_code(fun_inst, fun_impl)

    def write_to_file(self, file_path: str):
        assert len(self.x64_code) > 0, 'x64 instructions not yet generated, call generate_x64_instructions()!'
        f = open(file_path, 'w')

        # configuration
        f.write('default rel\n')  # RIP-relative offsets by default
        f.write('global _main\n')  # Program entry point (function name)
        for e in self.externals.keys():
            f.write(f'extern {e}\n')

        # text section for instructions
        f.write('        section .text\n')
        for f_name, insts in self.x64_code.items():
            f.write(f'    {f_name}:\n')
            for i in insts:
                if i.inst is Mnemonic.MARK_LABEL:
                    f.write(f'      {i.op1}:\n')
                else:
                    f.write(f'        {i}\n')

        # bss section for global variables
        if len(self.globals) > 0:
            f.write('        section .bss\n')
            for i, g in self.globals.items():
                f.write(str(g) + '\n')

        # data section
        if '_printf' in self.externals:
            f.write('        section .data\n')
            f.write('    int_format:     db      "%d", 0\n')

        f.close()

    def assemble_and_link(self, file_path: str, out_path: str):
        object_path = out_path + '.o'
        cp = subprocess.run([
            'nasm',
            '-g',  # Include debug info
            '-f macho64',  # Macho-O file format
            '-o',
            object_path,
            file_path,
        ])
        if cp.returncode == 0:
            cp = subprocess.run([
                'ld',
                '/usr/lib/libSystem.dylib',  # Include C library
                object_path,  # object file
                '-o',
                out_path
            ])
            if cp.returncode == 0:
                Logger.info(f'Input file {file_path} assembled and linked to {out_path}')
            else:
                Logger.error('Error: linker returned non-zero status code')
        else:
            Logger.error('Error: assembler returned non-zero status code')
