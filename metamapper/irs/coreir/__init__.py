from .ir import gen_peak_CoreIR
from ...node import Nodes

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")

    Input = CoreIRNodes.create_dag_node("Input", [], [0], ("port_name",))
    Output = CoreIRNodes.create_dag_node("Output", [0], [], ("port_name",))
    CoreIRNodes.add("Input", Input, None, None)
    CoreIRNodes.add("Output", Output, None, None)
    peak_ir = gen_peak_CoreIR(width)
    #This a list of coreir nodes
    for op in ("add", "mul"):
        #TODO I need to associate a coreir module with each of these
        dag_node = CoreIRNodes.create_dag_node(op, ["in0","in1"], ["out"], ("iname",))
        peak_node = peak_ir.instructions[op]
        raise NotImplementedError("determine coreir module")
        cmod = None
        CoreIRNodes.add(op, dag_node, peak_node, cmod)
    return CoreIRNodes
