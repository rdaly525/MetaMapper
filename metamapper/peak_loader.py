import magma as m
import peak
from peak.assembler import Assembler
from hwtypes import Bit
from .node import Node, create_node

#Returns
def load_from_peak(peak_fc) -> ("dagnode", "magma_circuit"):
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
    dag_node = create_node(Node, peak_bv.__name__, inputs, outputs)
    return dag_node, peak_m

