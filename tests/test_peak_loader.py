from examples.alu import gen_ALU, Inst_fc
from metamapper.peak_loader import load_from_peak
from metamapper.node import Nodes

def test_load():
    ArchNodes = Nodes("Arch")
    ALU_fc = gen_ALU(16)
    load_from_peak(ArchNodes, ALU_fc)
    dag_node = ArchNodes.dag_nodes["ALU"]
    assert dag_node.input_names() == ["inst", "a", "b"]
    assert dag_node.output_names() == ["O"]
