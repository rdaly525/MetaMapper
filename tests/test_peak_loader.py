from examples.alu import gen_ALU, Inst_fc
from metamapper.peak_loader import load_from_peak

def test_load():
    ALU_fc = gen_ALU(16)
    dag_node, alu_m = load_from_peak(ALU_fc)
    assert dag_node.input_names() == ["inst", "a", "b"]
    assert dag_node.output_names() == ["O"]
