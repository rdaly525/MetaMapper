import magma as m
import peak
from peak.assembler import Assembler
from hwtypes import Bit
from .node import Nodes

def load_from_peak(nodes: Nodes, peak_fc) -> ("dagnode", "magma_circuit"):
    class HashableDict(dict):
        def __hash__(self):
            return hash(tuple(sorted(self.keys())))

    peak_m = peak_fc(m.get_family())

    #TODO Better way to get the first port name?
    instr_name = list(peak_m.interface.items())[0][0]

    peak_bv = peak_fc(Bit.get_family())
    instr_type = peak_bv.input_t.field_dict[instr_name]
    asm = Assembler(instr_type)
    instr_magma_type = type(peak_m.interface.ports[instr_name])
    peak_m = peak.wrap_with_disassembler(
        peak_m,
        asm.disassemble,
        asm.width,
        HashableDict(asm.layout),
        instr_magma_type
    )

    io = peak_m.interface
    inputs = []
    outputs = []
    for p, T in io.items():
        if p in ("CLK", "ASYNCRESET"):
            continue
        if T.is_input():
            inputs.append(p)
        elif T.is_output():
            outputs.append(p)
        else:
            assert 0
    node_name = peak_bv.__name__
    dag_node = nodes.create_dag_node(node_name, inputs, outputs)
    nodes.add(node_name, dag_node, peak_fc, peak_m)
