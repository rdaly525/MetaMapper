from examples.alu import gen_ALU

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper

import pytest

@pytest.mark.parametrize("app", ["add4", "add_const"])
def test_app(app):
    if app == "add_const":
        pytest.skip()
    c = CoreIRContext(reset=True)
    file_name = f"examples/{app}.json"

    ArchNodes = Nodes("Arch")
    arch_fc = gen_ALU(16)
    putil.load_from_peak(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    mapper = Mapper(CoreIRNodes, ArchNodes)
    cmod = cutil.load_from_json(file_name)
    mapped_mod = mapper.do_mapping(cmod)
    mapped_mod.save_to_file(f"tests/build/{app}_mapped.json")
