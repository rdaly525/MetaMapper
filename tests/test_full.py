from examples.alu import gen_ALU
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
    #("inst", "rega",): Mode_t.BYPASS
}
@pytest.mark.parametrize("arch", [
    #("ALU", gen_ALU(16), {}),
    ("Lassen", lassen_fc, lassen_constraints)
])
@pytest.mark.parametrize("app", ["conv_3_3", "add2", "add1_const", "add4", "add3_const"])
#@pytest.mark.parametrize("app", ["add2", "add1_const", "add4", "add3_const"])
def test_app(arch, app):
    c = CoreIRContext(reset=True)
    file_name = f"examples/{app}.json"

    name, arch_fc, constraints = arch
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    mapper = Mapper(CoreIRNodes, ArchNodes)
    cmod = cutil.load_from_json(file_name, ["lakelib"])
    mapped_mod = mapper.do_mapping(cmod)
    mapped_mod.save_to_file(f"tests/build/{name}_{app}_mapped.json")
    assert 0
