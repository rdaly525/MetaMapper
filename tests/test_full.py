from examples.PEs.alu_basic import gen_ALU
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
import pytest

lassen_constraints = {
    ("clk_en",): 1,
    ("config_addr",): 0,
    ("config_data",): 0,
    ("config_en",): 0,
}

@pytest.mark.parametrize("arch", [
    ("PE_lut", gen_PE_lut(16), {}),
    ("Lassen", lassen_fc, lassen_constraints),
    ("ALU", gen_ALU(16), {}),
])
#@pytest.mark.parametrize("app", ["camera_pipeline"])#, "add2", "add1_const", "add4", "add3_const"])
#@pytest.mark.parametrize("app", ["conv_3_3"])#, "add2", "add1_const", "add4", "add3_const"])
@pytest.mark.parametrize("app", ["add2", "add1_const", "add4", "add3_const"])
def test_app(arch, app):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{app}.json"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name) # libraries=["lakelib"])
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)
    name, arch_fc, constraints = arch
    if name == "ALU" and app == "add_or":
        pytest.skip()
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mapper = Mapper(CoreIRNodes, ArchNodes, conv=True)
    mod = mapper.do_mapping(pb_dags)
    mod.print_()
    #c.run_passes(["cullgraph"])
    mod.save_to_file(f"tests/build/{name}_{app}_mapped.json")
