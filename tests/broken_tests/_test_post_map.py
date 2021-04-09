from examples.PEs.alu_basic import gen_ALU
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import  print_dag

import delegator
import pytest

lassen_rules = "../lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

@pytest.mark.parametrize("arch", [
    ("Lassen", lassen_fc, {}),
])
@pytest.mark.parametrize("app", ["resnet_3x_med_dse"])
def test_app(arch, app):
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    file_name = f"examples/post_mapping/{app}.json"
    CoreIRNodes = gen_CoreIRNodes(16)
    cutil.load_from_json(file_name, libraries=["cgralib"])

    arch_fc = lassen_fc
    rule_file = lassen_rules

    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)

    c.run_passes(["rungenerators", "deletedeadinstances"])


    for kname, kmod in kernels.items():
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        #print_dag(dag)
        mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
        #print("Mapped",flush=True)
        #print_dag(mapped_dag)
        #mod = cutil.dag_to_coreir_def(ArchNodes, mapped_dag, kmod)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)
        #mod.print_()

    print(f"Num PEs used: {mapper.num_pes}")
    output_file = f"build/{app}_mapped.json"
    print(f"saving to {output_file}")
    c.save_to_file(output_file)

    if verilog:
        c.run_passes(["wireclocks-clk"])
        c.run_passes(["wireclocks-arst"])
        c.run_passes(["markdirty"])


        #Test syntax of serialized json
        res = delegator.run(f"coreir -i {output_file} -l commonlib")
        assert not res.return_code, res.out + res.err

        #Test serializing to verilog
        res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o build/{app}_mapped.v --inline')
        assert not res.return_code, res.out + res.err

#test_app(("PE_lut", gen_PE_lut(16), {}),"add2")
