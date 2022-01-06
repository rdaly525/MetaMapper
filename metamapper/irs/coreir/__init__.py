from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant, DagNode, Select, Dag, Input, Output
from ... import CoreIRContext
from ...peak_util import load_from_peak, peak_to_coreir
from ...common_passes import print_dag
import coreir
from hwtypes import BitVector, Product, strip_modifiers
from peak import family

def strip_trailing(op):
    if op[-1] == "_":
        return op[:-1]
    return op

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()

    basic = ("mul", "add", "const", "and_", "or_", "neg")
    other = ("ashr", "eq", "lshr", "mux", "sub", "slt", "sle", "sgt", "sge", "ult", "ule", "ugt", "uge", "shl")
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
    
    name = f"float.add"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("float").generators["add"](exp_bits=8, frac_bits=7)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.add", modparams=())

    name = f"float.sub"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("float").generators["sub"](exp_bits=8, frac_bits=7)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.sub", modparams=())

    name = f"float.mul"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("float").generators["mul"](exp_bits=8, frac_bits=7)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="float.mul", modparams=())

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

    name = f"mult_middle"
    peak_fc = peak_ir.instructions[name]
    cmod = None
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="mult_middle", modparams=())

    CoreIRNodes.custom_nodes = ["mult_middle", "fp_getmant", "fp_addiexp", "fp_subexp", "fp_cnvexp2f", "fp_getfint", "fp_getffrac", "fp_cnvint2f"]

    # class FPRom(DagNode):
    #     def __init__(self, raddr, ren, *, init, iname):
    #         super().__init__(raddr, ren, init=init, iname=iname)
    #         self.modparams=()

    #     @property
    #     def attributes(self):
    #         return ("init", "iname")

    #     #Hack to get correct port name
    #     def select(self, field, original=None):
    #         self._selects.add("rdata")
    #         return Select(self, field="rdata",type=BitVector[16])

    #     nodes = CoreIRNodes
    #     static_attributes = {}
    #     node_name = "memory.rom2"
    #     num_children = 2
    #     type = Product.from_fields("Output",{"rdata":BitVector[16]})
    

    # source_node = Input(iname="self", type=BitVector[16])
    # in0 = source_node.select("in0")
    # in1 = source_node.select("in1")
    # get_mant = CoreIRNodes.dag_nodes["fp_getmant"](in1)
    # rom = FPRom(get_mant.select("out"), None, None)
    # sub_exp = CoreIRNodes.dag_nodes["fp_subexp"](rom.select("rdata"))
    # mult = CoreIRNodes.dag_nodes["fp_mul"](sub_exp.select("out"), in0.select("out"))
    # sink_node = Output(mult.select("out"))

    # CoreIRNodes.custom_inline["float.div"] = Dag([source_node], [sink_node])
    # print_dag(CoreIRNodes.custom_inline["float.div"])
    # breakpoint()



    return CoreIRNodes


