import delegator
import pytest
from examples.PEs.alu_basic import gen_ALU
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, dag_to_pdf
from lassen import PE_fc as lassen_fc

lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"


class _ArchLatency:
    @staticmethod
    def get(node):
        kind = node.kind()[0]
        print(kind)
        if kind == "PE" or kind == "Rom":
            return 1
        
        return 0

@pytest.mark.parametrize("app", ["camera_pipeline_compute","harris_compute", "gaussian_compute", "laplacian_pyramid_compute", "cascade_compute",
                               "resnet_block_compute", "resnet_compute"])


def test_app(app):
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
    reg = "coreir.pipeline_reg"
    ArchNodes.add(reg, CoreIRNodes.peak_nodes[reg], CoreIRNodes.coreir_modules[reg], CoreIRNodes.dag_nodes[reg])
    reg1 = "corebit.pipeline_reg"
    ArchNodes.add(reg1, CoreIRNodes.peak_nodes[reg1], CoreIRNodes.coreir_modules[reg1], CoreIRNodes.dag_nodes[reg1])


    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)
    c.run_passes(["rungenerators", "deletedeadinstances"])


    for kname, kmod in kernels.items():
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        mapped_dag = mapper.do_mapping(dag, node_latencies=_ArchLatency(), prove_mapping=False)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=True)
        # mod.add_metadata("latency", "2")
    
    


    output_file = f"examples/clockwork/{app}_mapped.json"
    print(f"saving to {output_file}")
    # c.set_top(mod)
    c.save_to_file(output_file)

    c.run_passes(["wireclocks-clk"])
    c.run_passes(["wireclocks-arst"])
    c.run_passes(["markdirty"])


    #Test syntax of serialized json
    res = delegator.run(f"coreir -i {output_file} -l commonlib cgralib")
    assert not res.return_code, res.out + res.err

    #Test serializing to verilog
    res = delegator.run(f'coreir -i {output_file} -l commonlib cgralib -p "wireclocks-clk; wireclocks-arst" -o build/{app}_mapped.v --inline')
    assert not res.return_code, res.out + res.err

