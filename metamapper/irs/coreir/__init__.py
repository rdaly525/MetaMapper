from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant
from ... import CoreIRContext
from ...peak_util import load_from_peak
import coreir

def strip_trailing(op):
    if op[-1] == "_":
        return op[:-1]
    return op
def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()

    basic = ("mul", "add", "const", "and_", "or_")
    other = ("ashr", "eq", "lshr", "mux", "sub", "ult", 'ule', 'uge', 'ugt', "slt", 'sle', 'sge', 'sgt', "shl")
    bit_ops = ("const", "or_", "and_", "xor", "mux", "not_")
    commonlib_ops = ("abs", "smax", "smin", "umin", "umax")
    for namespace, ops, is_module in (
        ("coreir", basic + other, False),
        ("corebit", bit_ops, True),
        ("commonlib", commonlib_ops, False)
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
            name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name=name)
            assert name_ == name
            assert name in CoreIRNodes.coreir_modules
            assert CoreIRNodes.name_from_coreir(cmod) == name
            print(f"Loaded {name}!")

    #Load reg
    name = f"coreir.reg"
    peak_fc = peak_ir.instructions[name]
    cmod = c.get_namespace("coreir").generators["reg"](width=width)
    name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.reg", stateful=True, modparams=("clk_posedge", "init"))

    return CoreIRNodes

