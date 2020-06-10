from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant
from ...__init__ import CoreIRContext
from ...peak_util import load_from_peak

def strip_trailing(op):
    if op[-1] == "_":
        return op[:-1]
    return op
def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()
    for op in ("mul", "add", "and_", "or_", "const"):
        peak_fc = peak_ir.instructions[op]
        coreir_op = strip_trailing(op)
        cmod = c.get_namespace("coreir").generators[coreir_op](width=width)
        name = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod)
        print(f"Loaded {name}!")
        assert name in CoreIRNodes.coreir_modules
        assert CoreIRNodes.name_from_coreir(cmod) == name
    return CoreIRNodes
