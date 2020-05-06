from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant
from ...__init__ import CoreIRContext
from ...peak_util import peak_to_node

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()
    for op in ("add", "mul", "const"):
        peak_fc = peak_ir.instructions[op]
        cmod = c.get_namespace("coreir").generators[op](width=width)
        if op == "const":
            const = CoreIRNodes.create_dag_node("const", [], [0], ("iname", "value",), other_parents=(Constant,))
            CoreIRNodes.add("const", const, peak_fc, cmod)
        else:
            peak_to_node(CoreIRNodes, peak_fc, cmod)
    #Deal with coreir.const separately. Have it inheret from Constant

    return CoreIRNodes
