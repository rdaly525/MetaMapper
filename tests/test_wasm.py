from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.wasm_compiler import Compiler
from peak.examples.riscv import sim, isa, family, asm
from metamapper.family import set_fam, fam

import pytest

@pytest.mark.parametrize("app", ["add2", "add1_const", "add4", "add3_const"])
def test_app(app):
    c = CoreIRContext(reset=True)
    set_fam(family)
    print("SET FAMILY", family)
    print("FAM", fam())
    file_name = f"examples/coreir/{app}.json"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name)
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)
    arch_fc = sim.R32I_mappable_fc
    ArchNodes = Nodes("RISCV")
    putil.load_from_peak(ArchNodes, arch_fc, wasm=True)
    mapper = Compiler(CoreIRNodes, ArchNodes, conv=True)
    mapped_cmod = mapper.do_mapping(pb_dags)
    mapped_cmod.print_()

