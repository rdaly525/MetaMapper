from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant, DagNode, Select
from ... import CoreIRContext
from ...peak_util import load_from_peak, peak_to_coreir
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
    
   

    name = f"coreir.mul32"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("coreir").generators["mul"](width=32)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.mul32", modparams=())

    name = f"coreir.sext"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("coreir").generators["sext"](width_in=16, width_out=32)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.sext", modparams=())

    name = f"coreir.slice"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("coreir").generators["slice"](width=32, hi=24, lo=8)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.slice", modparams=())


    return CoreIRNodes


