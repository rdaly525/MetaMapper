from metamapper.rewrite_table import RewriteTable
from metamapper.instruction_selection import GreedyCovering

from examples.alu import gen_ALU, Inst, OP

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
import metamapper.magma_util as mutil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule

import coreir

from metamapper.common_passes import AddID, Printer, VerifyNodes

import magma as m

def test_discover():
    ArchNodes = Nodes("Arch")
    arch_fc = gen_ALU(16)
    name = putil.peak_to_node(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover("add", "ALU")
    assert rr is not None

def test_eager_covering():
    ArchNodes = Nodes("Arch")
    arch_fc = gen_ALU(16)
    name = putil.peak_to_node(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover_1to1_rewrite("add", "ALU")
    assert rr

    c = coreir.Context()
    dag = load_from_json(c, "examples/add4.json")
    #dag = coreir_module_to_dag(cmod)

    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    AddID(mapped_dag)
    Printer(mapped_dag)
    Verify(mapped_dag)

    mapped_m = mutil.dag_to_magma(cmod, mapped_dag, ArchNodes)
    m.compile("tests/build/add4_mapped", mapped_m, output="coreir")
