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
        # Create CoreIR node if not specified
        #if op == "const":
        #    const = CoreIRNodes.create_dag_node("const", [], [0], ("iname", "value",), other_parents=(Constant,))
        #    const = nodes.create_dag_node(node_name, len(inputs), stateful=False, attrs=dag_attrs), node_name
        #    CoreIRNodes.add("const", const, peak_fc, cmod)
        #else:
        load_from_peak(CoreIRNodes, peak_fc, cmod=cmod)
    #Deal with coreir.const separately. Have it inheret from Constant

    return CoreIRNodes
