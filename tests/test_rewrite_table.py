import pytest
from examples.PEs.alu_basic import gen_ALU
from examples.PEs.alu_add3 import gen_ALU as gen_Add3
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc
from peak import family_closure, Peak
from metamapper.common_passes import print_dag
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
}
@pytest.mark.parametrize("arch", [
    ("PE_lut", gen_PE_lut(16), {}),
    ("basic_alu", gen_ALU(16), {}),
    ("lassen", lassen_fc, lassen_constraints)
])
@pytest.mark.parametrize("op", ["coreir.add", "coreir.const", "corebit.or_", "corebit.const"])
def test_discover(arch, op):
    CoreIRContext(reset=True)
    name, arch_fc, constraints = arch
    if name is "basic_alu" and "corebit" in op:
        return
    if name is "PE_lut" and op == "corebit.const":
        return

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover(op, name, constraints)
    assert rr is not None

def test_complex():
    CoreIRContext(reset=True)
    arch_fc = gen_Add3(16)
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)

    @family_closure
    def add3_fc(family):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        @family.assemble(locals(), globals())
        class add3(Peak):
            def __call__(self, in0: Data, in1: Data, in2: Data) -> Data:
                return (in0 + in1) + in2
        return add3

    rr = table.discover(add3_fc, "ALU")
    assert rr is not None
    rr = table.discover("coreir.add", "ALU")
    assert rr is not None

    cmod = cutil.load_from_json("examples/coreir/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    verify_and_print(CoreIRNodes, dag)

    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    print_dag(mapped_dag)
    verify_and_print(ArchNodes, mapped_dag)

def test_complex_dag_bad():
    CoreIRContext(reset=True)
    arch_fc = gen_Add3(16)
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)

    @family_closure
    def add2x_fc(family):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        @family.assemble(locals(), globals())
        class add2x(Peak):
            def __call__(self, in0: Data, in1: Data) -> Data:
                return (in0 + in1) + (in0 + in1)
        return add2x

    rr = table.discover(add2x_fc, "ALU")
    assert rr is not None

    cmod = cutil.load_from_json("examples/coreir/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    print_dag(mapped_dag)
    wrong = VerifyNodes(ArchNodes).verify(mapped_dag)
    assert wrong is not None

def test_complex_dag():
    CoreIRContext(reset=True)
    arch_fc = gen_Add3(16)
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)

    @family_closure
    def add2x_fc(family):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        @family.assemble(locals(), globals())
        class add2x(Peak):
            def __call__(self, in0: Data, in1: Data) -> Data:
                return (in0 + in1) + (in0 + in1)
        return add2x

    rr = table.discover(add2x_fc, "ALU")
    assert rr is not None

    cmod = cutil.load_from_json("examples/coreir/dag.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    verify_and_print(CoreIRNodes, dag)

    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    print_dag(mapped_dag)
    verify_and_print(ArchNodes, mapped_dag)

def verify_and_print(nodes, dag):
    wrong = VerifyNodes(nodes).verify(dag)
    if wrong is not None:
        raise ValueError(f"Unmapped: f{wrong}")

def test_eager_covering():
    CoreIRContext(reset=True)

    ArchNodes = Nodes("Arch")
    arch_fc = gen_ALU(16)
    name = putil.load_from_peak(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)
    rr = table.discover("coreir.add", "ALU")
    assert rr

    cmod = cutil.load_from_json("examples/coreir/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    verify_and_print(CoreIRNodes, dag)

    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    verify_and_print(ArchNodes, mapped_dag)

    #mapped_m = mutil.dag_to_magma(cmod, mapped_dag, ArchNodes)
    #m.compile("tests/build/add4_mapped", mapped_m, output="coreir")
