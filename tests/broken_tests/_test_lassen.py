import pytest
import delegator

from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper

#Assumes rules are in the src dir created by pip install -r requirements.txt
lassen_rules = "./src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

@pytest.mark.parametrize("arch", [
    ("Lassen", lassen_fc, {}),
])
# @pytest.mark.parametrize("app", ["camera_pipeline_compute", "harris_compute", "gaussian_compute", "laplacian_pyramid_compute", "cascade_compute",
#                                "resnet_block_compute", "resnet_compute"])
@pytest.mark.parametrize("app", ["camera_pipeline_compute"])
def test_app(arch, app):
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    arch_fc = lassen_fc
    rule_file = lassen_rules

    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    file_name = f"examples/clockwork/{app}.json"
    cutil.load_libs(["commonlib", "cgralib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cutil.load_from_json(file_name) 
    kernels = dict(c.global_namespace.modules)

    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)

    c.run_passes(["rungenerators", "deletedeadinstances"])

    for kname, kmod in kernels.items():
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=True)

    print(f"Num PEs used: {mapper.num_pes}")
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

