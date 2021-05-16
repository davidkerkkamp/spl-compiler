from typing import List, Tuple

import compiler.code_generation.SSM.op_codes as ssm
from compiler.AST.fields import FieldType
from compiler.code_generation.SSM.Register import Register
from compiler.code_generation.generic.generator_utils import FunctionInstance, FunctionImpl
import compiler.code_generation.generic.op_codes as gen_codes


class SSMGenerator:
    def __init__(self, functions: List[Tuple[FunctionInstance, FunctionImpl]]):
        self.functions = functions
        self.heap_location = 2000
        self.ssm_code: List[List[ssm.SSMOpCode]] = []
        self.entry_point_name = None

    def generate(self):
        for fun_instance, fun_impl in self.functions:
            self.generate_function_code(fun_instance, fun_impl)
        return self.ssm_code

    def to_file(self, path: str):
        assert len(self.ssm_code) > 0, 'SSM code not yet generated, call generate() function'
        f = open(path, 'w')
        for codes in self.ssm_code:
            for code in codes:
                f.write(str(code))
                f.write('\n')
        f.close()

    def generate_function_code(self, fun_instance: FunctionInstance, fun_impl: FunctionImpl):
        ssm_ops = []
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

        ssm_ops.append(ssm.MarkFunction(fun_instance.create_identifier()))
        ssm_ops.append(ssm.Link(local_vars_size))

        if fun_instance.entry_point:
            assert self.entry_point_name is None, \
                f"Function '{fun_instance.name}' is marked as entry point, " \
                f"but '{self.entry_point_name}' is already the entry point"
            self.initialize_globals(fun_impl, ssm_ops)
            self.entry_point_name = fun_instance.name

        for gen_op in fun_impl.ops:
            self.map_generic_to_ssm(fun_instance, gen_op, ssm_ops)

        self.ssm_code.append(ssm_ops)

    # Push dummy values to reserve space for globals
    def initialize_globals(self, fun_impl: FunctionImpl, ssm_ops: List[ssm.SSMOpCode]):
        global_vars_size \
            = max([0] + [(g.glob.offset() + 1) for g in fun_impl.ops if isinstance(g, gen_codes.StGlob)])
        for i in range(global_vars_size):
            ssm_ops.append(ssm.Ldc(0))
        ssm_ops.append(ssm.Stmh(global_vars_size))

    def map_generic_to_ssm(self, fun_inst: FunctionInstance, gen_op: gen_codes.GenericOpCode,
                           ssm_ops: List[ssm.SSMOpCode]):
        if isinstance(gen_op, gen_codes.Add):
            ssm_ops.append(ssm.Add())
        elif isinstance(gen_op, gen_codes.And):
            ssm_ops.append(ssm.And())
        elif isinstance(gen_op, gen_codes.Div):
            ssm_ops.append(ssm.Div())
        elif isinstance(gen_op, gen_codes.Eq):
            ssm_ops.append(ssm.Eq())
        elif isinstance(gen_op, gen_codes.Ge):
            ssm_ops.append(ssm.Ge())
        elif isinstance(gen_op, gen_codes.Gt):
            ssm_ops.append(ssm.Gt())
        elif isinstance(gen_op, gen_codes.Le):
            ssm_ops.append(ssm.Le())
        elif isinstance(gen_op, gen_codes.Lt):
            ssm_ops.append(ssm.Lt())
        elif isinstance(gen_op, gen_codes.Mod):
            ssm_ops.append(ssm.Mod())
        elif isinstance(gen_op, gen_codes.Mul):
            ssm_ops.append(ssm.Mul())
        elif isinstance(gen_op, gen_codes.Ne):
            ssm_ops.append(ssm.Ne())
        elif isinstance(gen_op, gen_codes.Neg):
            ssm_ops.append(ssm.Neg())
        elif isinstance(gen_op, gen_codes.Not):
            ssm_ops.append(ssm.Not())
        elif isinstance(gen_op, gen_codes.Or):
            ssm_ops.append(ssm.Or())
        elif isinstance(gen_op, gen_codes.Sub):
            ssm_ops.append(ssm.Sub())
        elif isinstance(gen_op, gen_codes.Swp):
            ssm_ops.append(ssm.Swp())
        elif isinstance(gen_op, gen_codes.Pop):
            ssm_ops.append(ssm.Ajs(-1))
        elif isinstance(gen_op, gen_codes.Halt):
            ssm_ops.append(ssm.Halt())
        elif isinstance(gen_op, gen_codes.PushConst):
            ssm_ops.append(ssm.Ldc(gen_op.const))
        elif isinstance(gen_op, gen_codes.Br):
            ssm_ops.append(ssm.Bra(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrEq):
            ssm_ops.append(ssm.Eq())
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrNe):
            ssm_ops.append(ssm.Ne())
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrGe):
            ssm_ops.append(ssm.Ge())
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrGt):
            ssm_ops.append(ssm.Gt())
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrLe):
            ssm_ops.append(ssm.Le())
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrLt):
            ssm_ops.append(ssm.Lt())
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrTrue):
            ssm_ops.append(ssm.Brt(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.BrFalse):
            ssm_ops.append(ssm.Brf(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.MarkLabel):
            ssm_ops.append(ssm.MarkLabel(gen_op.label.get_distinct_name(fun_inst)))
        elif isinstance(gen_op, gen_codes.PrintInt):
            ssm_ops.append(ssm.Trap(0))
        elif isinstance(gen_op, gen_codes.PrintChar):
            ssm_ops.append(ssm.Trap(1))
        elif isinstance(gen_op, gen_codes.Call):
            ssm_ops.append(ssm.Bsr(gen_op.f))
            ssm_ops.append(
                ssm.Ajs(-gen_op.f.num_args))  # Clean up after subroutine ended (args are pushed before bsr call)
            ssm_ops.append(ssm.Ldr(Register.RR))
        elif isinstance(gen_op, gen_codes.Ret):
            ssm_ops.append(ssm.Str(Register.RR))
            ssm_ops.append(ssm.Unlink())
            ssm_ops.append(ssm.Ret())
        elif isinstance(gen_op, gen_codes.RetNoValue):
            ssm_ops.append(ssm.Unlink())
            ssm_ops.append(ssm.Ret())
        elif isinstance(gen_op, gen_codes.LdLoc):
            offset = gen_op.local.offset()
            offset = offset - 1 if offset < 0 else offset
            ssm_ops.append(ssm.Ldl(offset))
        elif isinstance(gen_op, gen_codes.StLoc):
            offset = gen_op.local.offset()
            offset = offset - 1 if offset < 0 else offset
            ssm_ops.append(ssm.Stl(offset))
        elif isinstance(gen_op, gen_codes.LdGlob):
            ssm_ops.append(ssm.Ldc(self.heap_location + gen_op.glob.offset()))
            ssm_ops.append(ssm.Lda(0))
        elif isinstance(gen_op, gen_codes.StGlob):
            ssm_ops.append(ssm.Ldc(self.heap_location + gen_op.glob.offset()))
            ssm_ops.append(ssm.Sta(0))
        elif isinstance(gen_op, gen_codes.CreateListCons) or isinstance(gen_op, gen_codes.CreateTuple):
            ssm_ops.append(ssm.Stmh(2))
        elif isinstance(gen_op, gen_codes.CreateListNil):
            ssm_ops.append(ssm.Ldc(0))
        elif isinstance(gen_op, gen_codes.LdFld):
            offset = 0
            if gen_op.field_type is FieldType.Fst or gen_op.field_type is FieldType.Hd:
                offset = -1  # Stmh returns address of last pushed value
            ssm_ops.append(ssm.Lda(offset))
        elif isinstance(gen_op, gen_codes.StFld):
            offset = 0
            if gen_op.field_type is FieldType.Fst or gen_op.field_type is FieldType.Hd:
                offset = -1  # Stmh returns address of last pushed value
            ssm_ops.append(ssm.Lda(offset))
