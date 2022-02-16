from peak.ir import IR
from hwtypes import BitVector, Bit
from hwtypes.adt import Product
from peak import Peak, name_outputs, family_closure, Const
from peak.family import AbstractFamily, MagmaFamily, SMTFamily
from ...node import Nodes, Constant, DagNode, Select
from .custom_ops_ir import gen_custom_ops_peak_CoreIR
from hwtypes import SMTFPVector, FPVector, RoundingMode
import magma

def gen_peak_CoreIR(width):
    DATAWIDTH = 16
    CoreIR = gen_custom_ops_peak_CoreIR(DATAWIDTH)

    @family_closure
    def rom_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        Bit = family.Bit
        class rom(Peak):
            @name_outputs(rdata=Data)
            def __call__(self, raddr: Data, ren: Bit) -> Data:
                return Data(0)
        return rom

    CoreIR.add_instruction("memory.rom2", rom_fc)
    
    @family_closure
    def abs_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        class abs(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data) -> Data:
                in0_s = SData(in0)
                in0_neg = Data(-in0_s)
                return (in0_s >=0).ite(in0, in0_neg)
        return abs

    CoreIR.add_instruction("commonlib.abs", abs_fc)

    @family_closure
    def absd_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        class absd(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data, in1: Data) -> Data:
                d = in0 - in1
                d_s = SData(d)
                d_neg = Data(-d_s)
                return (d_s >=0 ).ite(d, d_neg)
        return absd
    CoreIR.add_instruction("commonlib.absd", absd_fc)

    @family_closure
    def smax_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        class smax(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data, in1: Data) -> Data:
                return (SData(in0) >= SData(in1)).ite(in0, in1)
        return smax

    CoreIR.add_instruction("commonlib.smax", smax_fc)


    @family_closure
    def smin_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        class smin(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data, in1: Data) -> Data:
                return (SData(in0) <= SData(in1)).ite(in0, in1)
        return smin

    CoreIR.add_instruction("commonlib.smin", smin_fc)

    @family_closure
    def umax_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        class umax(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data, in1: Data) -> Data:
                return (in0 >= in1).ite(in0, in1)
        return umax

    CoreIR.add_instruction("commonlib.umax", umax_fc)


    @family_closure
    def umin_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        class umin(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data, in1: Data) -> Data:
                return (in0 <= in1).ite(in0, in1)
        return umin

    CoreIR.add_instruction("commonlib.umin", umin_fc)


    @family_closure
    def const_fc(family):
        Data = family.BitVector[width]
        class const(Peak):
            @name_outputs(out=Data)
            def __call__(self, value: Const(Data)):
                return value

        return const

    CoreIR.add_instruction("coreir.const", const_fc)

    @family_closure
    def constBit_fc(family):
        Bit = family.Bit
        class const(Peak):
            @name_outputs(out=Bit)
            def __call__(self, value: Const(Bit)):
                return value
        return const

    CoreIR.add_instruction("corebit.const", constBit_fc)

    @family_closure
    def reg_fc(family):
        Data = family.BitVector[width]
        Bit = family.Bit
        class reg(Peak):
            def __init__(self):
                self.value = Data(0)

            @name_outputs(out=Data)
            def __call__(self, in___: Data, clk_posedge: Const(Bit), init: Const(Data)) -> Data:
                value = self.value
                self.value = in___
                return value
        return reg

    CoreIR.add_instruction("coreir.reg", reg_fc)

    @family_closure
    def pipeline_reg_fc(family):
        Data = family.BitVector[width]
        Bit = family.Bit
        class pipeline_reg(Peak):
            @name_outputs(out=Data)
            def __call__(self, value: Data) -> Data:
                return value
        return pipeline_reg

    CoreIR.add_instruction("coreir.pipeline_reg", pipeline_reg_fc)

    @family_closure
    def pipeline_reg_bit_fc(family):
        Bit = family.Bit
        class pipeline_reg_1_bit(Peak):
            @name_outputs(out=Bit)
            def __call__(self, value: Bit) -> Bit:
                return value
        return pipeline_reg_1_bit

    CoreIR.add_instruction("corebit.pipeline_reg", pipeline_reg_bit_fc)


    class UnaryInput(Product):
        in___ = BitVector[width]

    class UnaryInputBit(Product):
        in___=Bit

    class BinaryInput(Product):
        in0=BitVector[width]
        in1=BitVector[width]

    class BinaryInputBit(Product):
        in0=Bit
        in1=Bit

    class TernaryInput(Product):
        in0 = BitVector[width]
        in1 = BitVector[width]
        sel = Bit

    class TernaryInputBit(Product):
        in0 = Bit
        in1 = Bit
        sel = Bit

    class OutputBV(Product):
        out=BitVector[width]

    class OutputBit(Product):
        out=Bit

    for name, fun in (
        ("add", lambda f, x, y: x+y),
        ("sub", lambda f, x, y: x-y),
        ("shl", lambda f, x, y: x<<y),
        ("lshr", lambda f, x, y: x.bvlshr(y)),
        ("ashr", lambda f, x, y: x.bvashr(y)),
        ("mul", lambda f, x, y: x*y),
        #("udiv", lambda x, y: x.bvudiv(y)),
        #("urem", lambda x, y: x.bvurem(y)),
        #("sdiv", lambda x, y: x.bvsdiv(y)),
        #("srem", lambda x, y: x.bvsrem(y)),
        #("smod", lambda x, y: x.bvsmod(y)),
    ):
        CoreIR.add_peak_instruction(f"coreir.{name}", BinaryInput, OutputBV, fun, cls_name=name)

    for name, fun in (
        ("and_", lambda f, x, y: x&y),
        ("or_", lambda f, x, y: x|y),
        ("xor", lambda f, x, y: x^y),
    ):
        CoreIR.add_peak_instruction(f"coreir.{name}", BinaryInput, OutputBV, fun, cls_name=name)
        CoreIR.add_peak_instruction(f"corebit.{name}", BinaryInputBit, OutputBit, fun, cls_name=name)

    for name, fun in (
        ("wire", lambda f, x: x),
        ("not_", lambda f, x: ~x),
        ("neg", lambda f, x: -x)
    ):
        CoreIR.add_peak_instruction(f"coreir.{name}", UnaryInput, OutputBV, fun, cls_name=name)
        CoreIR.add_peak_instruction(f"corebit.{name}", UnaryInputBit, OutputBit, fun, cls_name=name)

    def reduce(fun):
        def _reduce(val):
            ret = val[0]
            for i in range(1, len(val)):
                ret = fun(ret, val[i])
            return ret
        return _reduce

    for name, fun in (
        ("andr", lambda f, x: reduce(lambda a, b : a&b)(x)),
        ("orr", lambda f, x: reduce(lambda a, b : a|b)(x)),
        ("xorr", lambda f, x: reduce(lambda a, b : a^b)(x)),
    ):
        CoreIR.add_peak_instruction(f"coreir.{name}", UnaryInput, OutputBit, fun, cls_name=name)

    for name, fun in (
        ("eq" , lambda f, x, y: x==y),
        ("neq", lambda f, x, y: x!=y),
        ("slt", lambda f, x, y: x.bvslt(y)),
        ("sle", lambda f, x, y: x.bvsle(y)),
        ("sgt", lambda f, x, y: x.bvsgt(y)),
        ("sge", lambda f, x, y: x.bvsge(y)),
        ("ult", lambda f, x, y: x.bvult(y)),
        ("ule", lambda f, x, y: x.bvule(y)),
        ("ugt", lambda f, x, y: x.bvugt(y)),
        ("uge", lambda f, x, y: x.bvuge(y)),
    ):
        CoreIR.add_peak_instruction(f"coreir.{name}", BinaryInput, OutputBit, fun, cls_name=name)

    CoreIR.add_peak_instruction("coreir.mux", TernaryInput, OutputBV, lambda f, in0, in1, sel: sel.ite(in1, in0), cls_name="mux")
    CoreIR.add_peak_instruction("corebit.mux", TernaryInputBit, OutputBit, lambda f, in0, in1, sel: sel.ite(in1, in0), cls_name="mux")


    return CoreIR
#TODO missing:
# slice, concat, sext, zext
