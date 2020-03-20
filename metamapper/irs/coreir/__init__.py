from .ir import gen_peak_CoreIR
from ...node import Nodes

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")

    Input = CoreIRNodes.create_dag_node("Input", [], [0], ("port_name",))
    Output = CoreIRNodes.create_dag_node("Output", [0], [], ("port_name",))
    CoreIRNodes.add("Input", Input, None, None)
    CoreIRNodes.add("Output", Output, None, None)
    peak_ir = gen_peak_CoreIR(width)
    for op in ("add", "mul"):
        dag_node = CoreIRNodes.create_dag_node(op, ["in0","in1"], ["out"], ("iname",))
        peak_node = peak_ir.instructions[op]
        CoreIRNodes.add(op, dag_node, peak_node, None)
    return CoreIRNodes
