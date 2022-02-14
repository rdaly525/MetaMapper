from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant, DagNode, Select, Dag, Input, Output
from ... import CoreIRContext
from ...peak_util import load_from_peak, peak_to_coreir
from ...common_passes import print_dag, Clone
import coreir
from hwtypes import BitVector, Product, strip_modifiers, Bit
from peak import family
import struct
import math

def strip_trailing(op):
    if op[-1] == "_":
        return op[:-1]
    return op

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()

    basic = ("mul", "add", "const", "and_", "or_", "neg")
    other = ("ashr", "eq", "neq", "lshr", "mux", "sub", "slt", "sle", "sgt", "sge", "ult", "ule", "ugt", "uge", "shl")
    bit_ops = ("const", "or_", "and_", "xor", "not_", "mux")
    commonlib_ops = ("abs", "smax", "smin", "umin", "umax")
    for namespace, ops, is_module in (
        ("corebit", bit_ops, True),
        ("coreir", basic + other, False)
        #("commonlib", commonlib_ops, False)
    ):
        for op in ops:
            assert c.get_namespace(namespace) is c.get_namespace(namespace)
            name = f"{namespace}.{op}"
            peak_fc = peak_ir.instructions[name]
            coreir_op = strip_trailing(op)
            if is_module:
                cmod = c.get_namespace(namespace).modules[coreir_op]
            else:
                gen = c.get_namespace(namespace).generators[coreir_op]
                cmod = gen(width=width)
            modparams = ()
            if op == "const":
                modparams = ("value",)
            name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name=name, modparams=modparams)
            assert name_ == name
            assert name in CoreIRNodes.coreir_modules
            assert CoreIRNodes.name_from_coreir(cmod) == name
    
    name = f"float_DW.fp_add"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float_DW.fp_add", modparams=())

    name = f"float.sub"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.sub", modparams=())

    name = f"float.exp"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.exp", modparams=())

    name = f"float_DW.fp_mul"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float_DW.fp_mul", modparams=())

    name = f"float.div"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.div", modparams=())


    name = f"float.mux"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.mux", modparams=())


    name = f"float.max"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.max", modparams=())

    name = f"float.min"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.min", modparams=())


    name = f"fp_gt"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_gt", modparams=())

    name = f"fp_lt"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_lt", modparams=())

    name = f"fp_getmant"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_getmant", modparams=())

    name = f"fp_addiexp"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_addiexp", modparams=())

    name = f"fp_subexp"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_subexp", modparams=())

    name = f"fp_cnvexp2f"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_cnvexp2f", modparams=())

    name = f"fp_getfint"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_getfint", modparams=())

    name = f"fp_getffrac"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_getffrac", modparams=())

    name = f"fp_cnvint2f"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="fp_cnvint2f", modparams=())

    name = f"commonlib.mult_middle"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="commonlib.mult_middle", modparams=())

    CoreIRNodes.custom_nodes = ["coreir.neq", "commonlib.mult_middle", "float.max", "float.min", "float.div", "float_DW.fp_mul", "float_DW.fp_add", "float.sub", "fp_getmant", "fp_addiexp", "fp_subexp", "fp_cnvexp2f", "fp_getfint", "fp_getffrac", "fp_cnvint2f", "fp_gt", "fp_lt", "float.exp", "float.mux"]


    class FPRom(DagNode):
        def __init__(self, raddr, ren, *, init, iname):
            super().__init__(raddr, ren, init=init, iname=iname)
            self.modparams=()
        @property
        def attributes(self):
            return ("init", "iname")

        #Hack to get correct port name
        def select(self, field, original=None):
            self._selects.add("rdata")
            return Select(self, field="rdata",type=BitVector[16])

        nodes = CoreIRNodes
        static_attributes = {}
        node_name = "memory.fprom2"
        num_children = 2
        type = Product.from_fields("Output",{"rdata":BitVector[16]})
  

    def float2bfbin(fnum):
       if (fnum=='NaN'):
         sign = '0'
         exp  = '11111111'
         lfrac = '11111111'
       elif (fnum=='-NaN'):
         sign = '1'
         exp  = '11111111'
         lfrac = '11111111'
       elif (fnum=='Inf'):
         sign = '0'
         exp  = '11111111'
         lfrac = '00000000'
       elif (fnum=='-Inf'):
         sign = '1'
         exp  = '11111111'
         lfrac = '00000000'
       else:
         fstr  = ''.join("{:08b}".format(elem) for elem in struct.pack('!f', fnum))
         sign  = fstr[0]
         exp   = fstr[1:9]
         lfrac = "0"+fstr[9:16]
         hfrac = fstr[16:]
         #Enable rounding
         if (hfrac[0]=="1"): #bit 8 of the float mantissa is set, so round up
           if (lfrac[1:8]=="1111111"): #roll over mantissa and increase exp if needed
             exp = "{:08b}".format((int(exp,2) + 1)) #exp overflow?
           lfrac = "{:08b}".format((int(lfrac,2) + 1))
             
       return sign + exp + lfrac[1:8]

    def div_lut(index):
        x = (1.0 + float(int(index))/128.0)
        x_inv = 1.0/x
        return int(float2bfbin(x_inv),2)
    depth = 1024
    div_rom_init = [div_lut(i) for i in range(0, 128)]+[0x0000]*(depth - 128)

    rom2 = CoreIRContext().get_namespace("memory").generators["rom2"](depth=256, width=width)
    CoreIRNodes.add("memory.fprom2", peak_ir.instructions["memory.rom2"], rom2, FPRom)

    input_t = Product.from_fields("Input", {f"in{i}": BitVector[16] for i in range(2)})
    output_t = Product.from_fields("Output", {"out": BitVector[16]})

    source_node = Input(iname="self", type=input_t)
    in0 = source_node.select("in0")
    in1 = source_node.select("in1")
    get_mant = CoreIRNodes.dag_nodes["fp_getmant"](in1,Constant(value=BitVector[16](0), type=BitVector[16]))

    en_const = Constant(value=Bit(1), type=Bit)
    en_const_dag = CoreIRNodes.dag_nodes["corebit.const"](en_const)

    rom = FPRom(get_mant.select("out"), en_const_dag.select("out"), init=div_rom_init, iname="fpdivrom")
    sub_exp = CoreIRNodes.dag_nodes["fp_subexp"](rom.select("rdata"), in1)
    mult = CoreIRNodes.dag_nodes["float_DW.fp_mul"](sub_exp.select("out"), in0)
    sink_node = Output(mult.select("out"), type=output_t)

    CoreIRNodes.custom_inline["float.div"] = (Dag(sources=[source_node], sinks=[sink_node]), [get_mant, sub_exp, mult])


    def exp_lut(index):
        x = (0.0 + float(int(index))/128.0)
        return int(float2bfbin((2**x)),2)


    exp_rom_init = [exp_lut(i) for i in range(0, 128)]+[exp_lut(i) for i in range(-128, 0)]+[0x0000]*(depth - 256)
    
    input_t = Product.from_fields("Input", {"in0": BitVector[16]})
    output_t = Product.from_fields("Output", {"out": BitVector[16]})

    source_node1 = Input(iname="self", type=input_t)
    in0 = source_node1.select("in0")

    ln2_inv = 1.0/math.log(2)
    ln2_inv_bf = int(float2bfbin(ln2_inv), 2)
    const_ln2_inv = Constant(value=BitVector[16](ln2_inv_bf), type=BitVector[16])
    const_ln2_inv_dag = CoreIRNodes.dag_nodes["coreir.const"](const_ln2_inv)
    ln2_mult = CoreIRNodes.dag_nodes["float_DW.fp_mul"](const_ln2_inv_dag.select("out"), in0)

    get_int = CoreIRNodes.dag_nodes["fp_getfint"](ln2_mult.select("out"), Constant(value=BitVector[16](0), type=BitVector[16]))
    get_frac = CoreIRNodes.dag_nodes["fp_getffrac"](ln2_mult.select("out"), Constant(value=BitVector[16](0), type=BitVector[16]))


    and_const = Constant(value=BitVector[16](255), type=BitVector[16])
    and_const_dag = CoreIRNodes.dag_nodes["coreir.const"](and_const)


    rom_idx = CoreIRNodes.dag_nodes["coreir.and_"](get_frac.select("out"), and_const_dag.select("out"))

    en_const = Constant(value=Bit(1), type=Bit)
    en_const_dag = CoreIRNodes.dag_nodes["corebit.const"](en_const)


    rom = FPRom(rom_idx.select("out"), en_const_dag.select("out"), init=exp_rom_init, iname="fpexprom")
    add_exp = CoreIRNodes.dag_nodes["fp_addiexp"](rom.select("rdata"), get_int.select("out"))

    sink_node = Output(add_exp.select("out"), type=output_t)

    CoreIRNodes.custom_inline["float.exp"] = (Dag(sources=[source_node1], sinks=[sink_node]), [ln2_mult])





    input_t = Product.from_fields("Input", {f"in{i}": BitVector[16] for i in range(2)})
    output_t = Product.from_fields("Output", {"out": BitVector[16]})

    source_node2 = Input(iname="self", type=input_t)
    in0 = source_node2.select("in0")
    in1 = source_node2.select("in1")

    gt = CoreIRNodes.dag_nodes["fp_gt"](in0, in1)

    max_ = CoreIRNodes.dag_nodes["coreir.mux"](in0, in1, gt.select("out"))

    sink_node = Output(max_.select("out"), type=output_t)

    CoreIRNodes.custom_inline["float.max"] = (Dag(sources=[source_node2], sinks=[sink_node]), [gt, max_])

    input_t = Product.from_fields("Input", {f"in{i}": BitVector[16] for i in range(2)})
    output_t = Product.from_fields("Output", {"out": BitVector[16]})

    source_node3 = Input(iname="self", type=input_t)
    in0 = source_node3.select("in0")
    in1 = source_node3.select("in1")

    lt = CoreIRNodes.dag_nodes["fp_lt"](in0, in1)

    min_ = CoreIRNodes.dag_nodes["coreir.mux"](in0, in1, lt.select("out"))

    sink_node = Output(min_.select("out"), type=output_t)

    CoreIRNodes.custom_inline["float.min"] = (Dag(sources=[source_node3], sinks=[sink_node]), [lt, min_])
 


    input_t = Product.from_fields("Input", {f"in{i}": BitVector[16] for i in range(2)})
    output_t = Product.from_fields("Output", {"out": Bit})

    source_node4 = Input(iname="self", type=input_t)
    in0 = source_node4.select("in0")
    in1 = source_node4.select("in1")

    eq = CoreIRNodes.dag_nodes["coreir.eq"](in0, in1)

    not_ = CoreIRNodes.dag_nodes["corebit.not_"](eq.select("out"))

    sink_node = Output(not_.select("out"), type=output_t)

    CoreIRNodes.custom_inline["coreir.neq"] = (Dag(sources=[source_node4], sinks=[sink_node]), [eq])
 


    return CoreIRNodes


