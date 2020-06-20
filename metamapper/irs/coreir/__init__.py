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
    namespace = "coreir"
    for op in ("mul", "add", "and_", "or_", "const"):
        name = f"{namespace}.{op}"
        peak_fc = peak_ir.instructions[name]
        coreir_op = strip_trailing(op)
        cmod = c.get_namespace(namespace).generators[coreir_op](width=width)
        name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name=name)
        assert name_ == name
        assert name in CoreIRNodes.coreir_modules
        assert CoreIRNodes.name_from_coreir(cmod) == name
        print(f"Loaded {name}!")
    namespace = "corebit"
    for op in ("const",):
        name = f"{namespace}.{op}"
        peak_fc = peak_ir.instructions[name]
        coreir_op = strip_trailing(op)
        cmod = c.get_namespace(namespace).modules[coreir_op]
        name = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name=name)
        print(f"Loaded {name}!")
        assert name in CoreIRNodes.coreir_modules
        assert CoreIRNodes.name_from_coreir(cmod) == name
    return CoreIRNodes
