import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
from metamapper.family import set_fam
import metamapper.wasm_util as wutil
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

from metamapper.common_passes import print_dag, ExtractNames
#@pytest.mark.parametrize("i", range(1, 26))
#@pytest.mark.parametrize("i", range(10, 11))
@pytest.mark.parametrize("i", range(1, 2))
def test_load(i):
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    p = f"p{i}"
    wasm_file = f"results/hd_results/{p}.wasm"
    app = wutil.wasm_to_dag(wasm_file, p)
    print_dag(app)
    op_cnt = ExtractNames(WasmNodes).extract(app)
    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    compiler = Compiler(WasmNodes, ArchNodes, ops=op_cnt.keys(), solver='z3')
    #compiler = Compiler(WasmNodes, ArchNodes, ops=op_cnt.keys(), solver='btor')
    binary = compiler.compile(app)

    # res = binary.run(in0=10, in1=5, in2=2)

