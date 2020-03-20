from metamapper.irs.coreir import gen_CoreIRNodes
from metamapper.peak_loader import load_from_peak
from examples.alu import gen_ALU, Inst_fc
from metamapper.node import Nodes
from metamapper.common_passes import AddID, Printer
from metamapper.rewrite_table import RewriteTable
from metamapper.dag_rewrite import EagerCovering
import coreir
from metamapper import coreir_module_to_dag
from metamapper.visitor import Visitor
from metamapper.to_magma import dag_to_magma
import magma as m

def test_rewrite_rule():
    ArchNodes = Nodes("Arch")
    ALU_fc = gen_ALU(16)
    load_from_peak(ArchNodes, ALU_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover_1to1_rewrite("add", "ALU")
    assert rr is not None


def test_eager_covering():
    ArchNodes = Nodes("Arch")
    ALU_fc = gen_ALU(16)
    load_from_peak(ArchNodes, ALU_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover_1to1_rewrite("add", "ALU")
    assert rr

    c = coreir.Context()
    cmod = c.load_from_file("examples/add4.json")
    dag = coreir_module_to_dag(cmod)

    inst_sel = EagerCovering(table)

    mapped_dag = inst_sel(dag)
    AddID(mapped_dag)
    Printer(mapped_dag)

    class Verify(Visitor):
        def visit_Input(self, node):
            Visitor.generic_visit(self, node)

        def visit_Output(self, node):
            Visitor.generic_visit(self, node)

        def visit_Constant(self, node):
            Visitor.generic_visit(self, node)

        def generic_visit(self, node):
            if not isinstance(node, ArchNodes.dag_node_cls):
                print(f"{node} is not of type {ArchNodes.dag_node_cls}")
                assert 0
            Visitor.generic_visit(self, node)
    Verify(mapped_dag)

    mapped_m = dag_to_magma(cmod, mapped_dag, ArchNodes)
    m.compile("build/add4_mapped", mapped_m, output="coreir")
