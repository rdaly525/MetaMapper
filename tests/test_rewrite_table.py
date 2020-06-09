import pytest
from examples.alu import gen_ALU
from lassen import PE_fc as lassen_fc
#from lassen.mode import Mode_t
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering

from metamapper.common_passes import AddID, Printer, VerifyNodes
from metamapper import CoreIRContext

lassen_constraints = {
    ("clk_en",): 1,
    ("config_addr",): 0,
    ("config_data",): 0,
    ("config_en",): 0,
    #("inst", "rega",): Mode_t.BYPASS
}

#@pytest.mark.parametrize("arch_fc", [gen_ALU(16), lassen_fc])
@pytest.mark.parametrize("arch", [
    (gen_ALU(16), {}),
    (lassen_fc, lassen_constraints)
])
@pytest.mark.parametrize("op", ["const", "add", "and_", "or_"])
def test_discover(arch, op):
    CoreIRContext(reset=True)
    arch_fc, constraints = arch
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover(op, name, constraints)
    assert rr is not None

def verify_and_print(nodes, dag):
    AddID().run(dag)
    print(Printer().run(dag).res)
    VerifyNodes(nodes).run(dag)

def test_eager_covering():
    CoreIRContext(reset=True)

    ArchNodes = Nodes("Arch")
    arch_fc = gen_ALU(16)
    name = putil.load_from_peak(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover("add", "ALU")
    assert rr

    cmod = cutil.load_from_json("examples/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    verify_and_print(CoreIRNodes, dag)

    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    verify_and_print(ArchNodes, mapped_dag)

    #mapped_m = mutil.dag_to_magma(cmod, mapped_dag, ArchNodes)
    #m.compile("tests/build/add4_mapped", mapped_m, output="coreir")
