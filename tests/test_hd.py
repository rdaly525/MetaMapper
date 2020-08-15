import metamapper.peak_util as putil
from metamapper.node import Nodes, Input, Output, Constant
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
from metamapper.common_passes import TypeLegalize
from metamapper.family import set_fam
import metamapper.wasm_util as wutil
from examples.PEs.alu_basic import gen_ALU
from metamapper import CoreIRContext
import metamapper.coreir_util as cutil
from peak import Peak, family_closure, name_outputs, Const
from hwtypes import Product
from peak.family import PyFamily
from metamapper.node import Dag
import pytest





@pytest.mark.skip
@pytest.mark.parametrize("i", range(1,26))
def compile_c(i):

    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    p = f"p{i}"

    #Compile the c file to wasm
    cpath = "results/hd"
    build_path= "results/hd_results"
    wasm_file = wutil.compile_c_to_wasm(p, cpath=cpath, build_path=build_path)
    print(wasm_file)

    #app = wutil.wasm_to_dag(wasm_file, "foo")

    #arch_fc = riscv.sim.R32I_mappable_fc
    #ArchNodes = Nodes("RiscV")
    #putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    #compiler = Compiler(WasmNodes, ArchNodes)
    #binary = compiler.compile(app)

    #res = binary.run(in0=10, in1=5, in2=2)
    #assert res == (10*5) & 2


from metamapper.rewrite_table import RewriteTable
def test_single():
    op = "const12"
    print("Looking for Op", op)
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    table = RewriteTable(WasmNodes, ArchNodes)
    rr = table.discover(op, "R32I_mappable")
    assert rr is not None



from metamapper.common_passes import print_dag, ExtractNames
#@pytest.mark.parametrize("i", range(1, 26))
#@pytest.mark.parametrize("i", range(10, 11))
@pytest.mark.parametrize("i", range(10,26))
def test_load(i):
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    p = f"p{i}"
    wasm_file = f"results/hd_results/{p}.wasm"
    app = wutil.wasm_to_dag(wasm_file, p)
    print_dag(app)

    # Type Legalize (Translate constants appropriately)
    TypeLegalize(WasmNodes).run(app)
    print("legalized")
    print_dag(app)

    op_cnt = ExtractNames(WasmNodes).extract(app)

    mset = [
        "i32.mul",
        "i32.div_s",
        "i32.div_u",
        "i32.rem_s",
        "i32.rem_u",
    ]
    m = any(op in mset for op in op_cnt)
    if m:
        print(f"HERE {i} in mset")
        assert 0

    print("Need to search for", op_cnt.keys())
    compiler = Compiler(WasmNodes, ops=op_cnt.keys(), solver='z3')
    binary = compiler.compile(app, prove=True)

    #assert binary.run(in0=8) == 1
    #assert binary.run(in0=7) == 0
    #assert binary.run(in0=16) == 0
