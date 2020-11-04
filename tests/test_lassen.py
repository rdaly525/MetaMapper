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
#@pytest.mark.parametrize("app", ["camera_pipeline_compute"])
@pytest.mark.parametrize("app", ["gaussian_compute"])
# @pytest.mark.parametrize("app", ["camera_pipeline_compute", "gaussian_compute", "add2", "add1_const", "add4", "add3_const"])
def test_app(arch, app):
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    file_name = f"examples/clockwork/{app}.json"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cutil.load_from_json(file_name) #libraries=["lakelib"])
    kernels = dict(c.global_namespace.modules)

    arch_fc = lassen_fc
    rule_file = lassen_rules

    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)

    for kname, kmod in kernels.items():
    # kname = "hcompute_blur_unnormalized_stencil"
    # kmod = kernels[kname]
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        print_dag(dag)
        mapped_dag = mapper.do_mapping(dag, prove_mapping=False)    


    print(f"Num PEs used: {mapper.num_pes}")
    return
    c.run_passes(["wireclocks-clk"])
    c.run_passes(["wireclocks-arst"])
    c.run_passes(["markdirty"])
    output_file= f"examples/clockwork/{app}_mapped.json"
    c.save_to_file(output_file)

    #Test syntax of serialized json
    res = delegator.run(f"coreir -i {output_file} -l commonlib")
    assert not res.return_code, res.out + res.err

    #Test serializing to verilog
    res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o examples/clockwork/{app}_mapped.v --inline')
    assert not res.return_code, res.out + res.err

#test_app(("PE_lut", gen_PE_lut(16), {}),"add2")
