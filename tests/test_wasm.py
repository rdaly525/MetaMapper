import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
from metamapper.family import set_fam
import metamapper.wasm_util as wutil
from peak import family

def test_app():
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    #Define a simple add3 program
    wasm_file = './examples/wasm/add3.wasm'
    app = wutil.wasm_to_dag(wasm_file, "add3")

    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    compiler = Compiler(WasmNodes, ArchNodes)
    binary = compiler.compile(app)

    res = binary.run(in0=10, in1=5, in2=13)
    assert res == 10 + 5 + 13
    set_fam(family)
