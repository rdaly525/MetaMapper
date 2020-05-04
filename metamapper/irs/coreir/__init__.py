from .ir import gen_peak_CoreIR
from ...node import Nodes
from ...__init__ import CoreIRContext
from ...peak_util import peak_to_node

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()
    #This a list of coreir nodes
    for op in ("add", "mul"):
        peak_fc = peak_ir.instructions[op]
        cmod = c.get_namespace("coreir").generators[op](width=width)
        peak_to_node(CoreIRNodes, peak_fc, cmod)
    return CoreIRNodes
