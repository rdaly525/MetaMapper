import pytest
from examples.PEs.alu_basic import gen_ALU
from examples.PEs.alu_add3 import gen_ALU as gen_Add3
from peak import family_closure, Peak, Const, family
from metamapper.common_passes import print_dag, SimplifyCombines, RemoveSelects
from metamapper.irs.coreir import gen_CoreIRNodes
#from metamapper.irs.wasm import gen_WasmNodes

import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering

from metamapper.common_passes import VerifyNodes
from metamapper import CoreIRContext
#from peak.examples import riscv #import sim, isa, family, asm
from metamapper.family import set_fam, fam

lassen_constraints = {
    ("clk_en",): 1,
    ("config_addr",): 0,
    ("config_data",): 0,
    ("config_en",): 0,
}
@pytest.mark.parametrize("arch", [
    ("basic_alu", gen_ALU(16), {}),
])
@pytest.mark.parametrize("op", [
    "coreir.add",
    "coreir.const",
    "corebit.or_",
    "corebit.const"
])
def test_discover(arch, op):
    CoreIRContext(reset=True)
    name, arch_fc, constraints = arch
    if name is "basic_alu" and "corebit" in op:
        return
    if name is "PE_lut" and op == "corebit.const":
        return

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

    rr = table.discover(add2x_fc, "ALU", rr_name="add2x")
    assert rr is not None

    cmod = cutil.load_from_json("examples/coreir/dag.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    print_dag(dag)
    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    print_dag(mapped_dag)
    verify_and_print(ArchNodes, mapped_dag)

@pytest.mark.skip
def test_complex_dag_const():
    CoreIRContext(reset=True)
    arch_fc = gen_Add3(16)
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)

    @family_closure
    def add_const_fc(family):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        @family.assemble(locals(), globals())
        class add_const(Peak):
            def __call__(self, in0: Data, imm: Const(Data)) -> Data:
                return in0 + imm
        return add_const

    rr = table.discover(add_const_fc, "ALU", rr_name="add_const")
    assert rr is not None
    #rr = table.discover("coreir.const", "ALU", rr_name="const")
    #assert rr is not None
    #rr = table.discover("coreir.add", "ALU", rr_name="add")
    #assert rr is not None

    cmod = cutil.load_from_json("examples/coreir/dag_const.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    print_dag(dag)
    inst_sel = GreedyCovering(table)

    mapped_dag = inst_sel(dag)
    print_dag(mapped_dag)
    verify_and_print(ArchNodes, mapped_dag)

@pytest.mark.skip
def test_complex_dag_const2():
    CoreIRContext(reset=True)
    arch_fc = gen_Add3(16)
    ArchNodes = Nodes("Arch")
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False)
    CoreIRNodes = gen_CoreIRNodes(16)
    table = RewriteTable(CoreIRNodes, ArchNodes)

    @family_closure
    def rr1_fc(family):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        @family.assemble(locals(), globals())
        class rr1(Peak):
            def __call__(self, a: Data, b: Data, c: Data, d: Data, imm: Const(Data), imm1: Const(Data), imm2: Const(Data)) -> Data:
                return a + (imm * b) + (imm1 * c) + (imm2 * d)
        return rr1

    rr = table.discover(rr1_fc, "ALU", rr_name="amc")
    assert rr is not None
    rr = table.discover("corebit.const", "ALU", rr_name="corebit.const")
    assert rr is not None
    rr = table.discover("coreir.const", "ALU", rr_name="coreir.const")
    assert rr is not None

    cmod = cutil.load_from_json("examples/coreir/conv_3_3.json") # libraries=["lakelib"])
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)
    for dag in pb_dags.values():
        break
    print_dag(dag)
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
    print("mapped")
    print_dag(mapped_dag)
    SimplifyCombines().run(mapped_dag)
    print("simplifiedCombineds")
    print_dag(mapped_dag)
    RemoveSelects().run(mapped_dag)
    print("removes selects")
    print_dag(mapped_dag)

    verify_and_print(ArchNodes, mapped_dag)

    #mapped_m = mutil.dag_to_magma(cmod, mapped_dag, ArchNodes)
    #m.compile("tests/build/add4_mapped", mapped_m, output="coreir")


@pytest.mark.skip
@pytest.mark.parametrize("op", ["i32.add"]) #, "coreir.const", "corebit.or_", "corebit.const"])
def test_discover_wasm(op):
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    WasmNodes = gen_WasmNodes()
    name = putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)
    table = RewriteTable(WasmNodes, ArchNodes)
    rr = table.discover(op, name)
    assert rr is not None
    set_fam(family)
