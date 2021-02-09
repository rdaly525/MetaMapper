from metamapper.irs.coreir import gen_CoreIRNodes
from metamapper.peak_loader import load_from_peak
from examples.alu import gen_ALU
from metamapper.node import Nodes
from metamapper.common_passes import AddID, Printer, VerifyMapping
from metamapper.rewrite_table import RewriteTable
from metamapper.dag_rewrite import GreedyCovering
import coreir
from metamapper import coreir_module_to_dag
from metamapper.to_magma import dag_to_magma
import magma as m
import pytest

kernels = [
    "add4",
]

@pytest.mark.parametrize("kernel", kernels)
def test_greedy_covering(kernel):
    ArchNodes = Nodes("Arch")
    ALU_fc = gen_ALU(16)
    load_from_peak(ArchNodes, ALU_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover_1to1_rewrite("add", "ALU")
    assert rr

    json_file = f"examples/{kernel}.json"

    c = coreir.Context()
    cmod = c.load_from_file(json_file)
    dag = coreir_module_to_dag(cmod)

    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    #AddID(mapped_dag)
    #Printer(mapped_dag)
    VerifyMapping(mapped_dag)

    mapped_m = dag_to_magma(cmod, mapped_dag, ArchNodes)
    m.compile(
        f"tests/build/{kernel}",
        mapped_m,
        output="coreir",
        #passes = ["rungenerators", "inline_single_instances", "clock_gate"] TODO this inlines too much. I want to maintain the Peak class hierarchy
    )
