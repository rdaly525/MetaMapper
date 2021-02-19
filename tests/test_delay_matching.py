import delegator
import pytest
from examples.PEs.alu_basic import gen_ALU
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag
from lassen import PE_fc as lassen_fc

lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"


class _ArchLatency:
    def get(self, node):
        kind = node.kind()[0]
        if kind == "ALU":
            return 1
        return 0


def test_app():
    c = CoreIRContext(reset=True)
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json("examples/coreir/add4.json")
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)

    arch_fc = lassen_fc
    rule_file = lassen_rules

    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)

    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)

    mapped_cmod = mapper.do_mapping(pb_dags, node_latencies=_ArchLatency())

    mapped_dag = mapper._history_[0]
    print_dag(mapped_dag)

    output_file = f"build/{app}_mapped.json"
    print(f"saving to {output_file}")
    c.save_to_file(output_file)

    c.run_passes(["wireclocks-clk"])
    c.run_passes(["wireclocks-arst"])
    c.run_passes(["markdirty"])


    #Test syntax of serialized json
    res = delegator.run(f"coreir -i {output_file} -l commonlib")
    assert not res.return_code, res.out + res.err

    #Test serializing to verilog
    res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o build/{app}_mapped.v --inline')
    assert not res.return_code, res.out + res.err

