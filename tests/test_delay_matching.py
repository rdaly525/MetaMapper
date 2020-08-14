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
    cmod = cutil.load_from_json("examples/coreir/add3.json")
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)
    arch_fc = gen_ALU(16)
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mapper = Mapper(CoreIRNodes, ArchNodes, conv=True)

    mapped_cmod = mapper.do_mapping(pb_dags, node_latencies=_ArchLatency())

    mapped_dag = mapper._history_[0]
    print_dag(mapped_dag)

    mapped_cmod.print_()
    c.set_top(mapped_cmod)
    c.run_passes(["cullgraph"])
    mapped_file = "tests/build/delay_matching"
    mapped_cmod.save_to_file(f"{mapped_file}.json")

    # Test syntax of serialized json.
    res = delegator.run(f"coreir -i {mapped_file}.json -l commonlib")
    assert not res.return_code, res.out + res.err

    # Test serializing to verilog.
    res = delegator.run(f'coreir -i {mapped_file}.json -l commonlib -p "wireclocks-clk; wireclocks-arst" -o {mapped_file}.v --inline')
    assert not res.return_code, res.out + res.err
