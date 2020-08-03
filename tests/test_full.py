from examples.PEs.alu_basic import gen_ALU
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper

import delegator
import pytest


lassen_constraints = {
    ("clk_en",): 1,
    ("config_addr",): 0,
    ("config_data",): 0,
    ("config_en",): 0,
}

@pytest.mark.parametrize("arch", [
    ("PE_lut", gen_PE_lut(16), {}),
    #("Lassen", lassen_fc, lassen_constraints),
    ("ALU", gen_ALU(16), {}),
])
#@pytest.mark.parametrize("app", ["camera_pipeine"])#, "add2", "add1_const", "add4", "add3_const"])
#@pytest.mark.parametrize("app", ["conv_3_3"])#, "add2", "add1_const", "add4", "add3_const"])
@pytest.mark.parametrize("app", ["add2", "add1_const", "add4", "add3_const"])
def test_app(arch, app):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{app}.json"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name) #, libraries=["lakelib"])
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)
    name, arch_fc, constraints = arch
    if name == "ALU" and app == "add_or":
        pytest.skip()
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mapper = Mapper(CoreIRNodes, ArchNodes, conv=True)
    mapped_cmod = mapper.do_mapping(pb_dags)
    mapped_cmod.print_()
    c.set_top(mapped_cmod)
    c.run_passes(["cullgraph"])
    mapped_file = f"tests/build/{name}_{app}_mapped"
    mapped_cmod.save_to_file(f"{mapped_file}.json")

    #Test syntax of serialized json
    res = delegator.run(f"coreir -i {mapped_file}.json -l commonlib")
    assert not res.return_code, res.out + res.err

    #Test serializing to verilog
    res = delegator.run(f'coreir -i {mapped_file}.json -l commonlib -p "wireclocks-clk; wireclocks-arst" -o {mapped_file}.v --inline')
    assert not res.return_code, res.out + res.err

#test_app(("PE_lut", gen_PE_lut(16), {}),"add2")

