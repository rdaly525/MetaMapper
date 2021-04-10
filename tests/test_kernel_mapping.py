from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, Constant2CoreIRConstant
import pytest
import delegator
from lassen.sim import PE_fc as lassen_fc

lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"
lassen_header = "libs/lassen_header.json"
lassen_def = "libs/lassen_def.json"


class _ArchLatency:

    @staticmethod
    def get(node):
        kind = node.kind()[0]
        if kind == "PE" or kind == "Rom":
            return 1
        return 0


@pytest.mark.parametrize("lat", [
    None,
    #_ArchLatency
])
@pytest.mark.parametrize("app", [
    "gaussian",
    "harris",
    "camera_pipeline",
    "laplacian_pyramid",
    "cascade",
    #"resnet_block",
    #"resnet"
])
def test_kernel_mapping(lat, app):

    verilog = False
    base = "examples/clockwork"
    app_file = f"{base}/{app}_compute.json"
    if lat is None:
        mapped_file = f"tests/build/{app}_mapped.json"
    else:
        mapped_file = f"tests/build/{app}_delay_mapped.json"

    c = CoreIRContext(reset=True)
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)

    cutil.load_from_json(app_file)
    c.run_passes(["rungenerators", "deletedeadinstances"])
    kernels = dict(c.global_namespace.modules)

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(
        ArchNodes,
        lassen_header,
        {"global.PE": arch_fc}
    )
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=lassen_rules)

    #c.run_passes(["rungenerators", "deletedeadinstances"])
    mods = []

    for kname, kmod in kernels.items():
        print(f"Mapping kernel {kname}")
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        Constant2CoreIRConstant(CoreIRNodes).run(dag)
        mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False, node_latencies=lat)
        #print_dag(mapped_dag)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)
        mods.append(mod)

    print(f"saving to {mapped_file}")
    c.serialize_definitions(mapped_file, mods)

    #if verilog:
    #    c.run_passes(["wireclocks-clk"])
    #    c.run_passes(["wireclocks-arst"])
    #    c.run_passes(["markdirty"])


    #    #Test syntax of serialized json
    #    res = delegator.run(f"coreir -i {output_file} -l commonlib")
    #    assert not res.return_code, res.out + res.err

    #    #Test serializing to verilog
    #    res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o build/{app}_mapped.v --inline')
    #    assert not res.return_code, res.out + res.err