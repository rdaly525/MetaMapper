import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
from metamapper.family import set_fam
import metamapper.wasm_util as wutil

def test_app():
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    #Define a simple add3 program
    wasm_file = './examples/wasm/wasm/add_const.wasm'
    app = wutil.wasm_to_dag(wasm_file, "add3")

    compiler = Compiler(WasmNodes)
    binary = compiler.compile(app, prove=False)

    res = binary.run(in0=10, in1=5, in2=13)
    assert res == 10 + 5 + 13

from metamapper.common_passes import ExtractNames
def test_prove():

    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    #Compile the c file to wasm
    wasm_file = wutil.compile_c_to_wasm("nop")
    app = wutil.wasm_to_dag(wasm_file, "nop")

    op_cnt = ExtractNames(WasmNodes).extract(app)
    compiler = Compiler(WasmNodes, ops=op_cnt.keys())
    binary = compiler.compile(app)

    #assert binary.run(in0=10) == -10
    ce = binary.prove()
    assert ce is None

def test_c():

    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    #Compile the c file to wasm
    wasm_file = wutil.compile_c_to_wasm("foo")
    app = wutil.wasm_to_dag(wasm_file, "foo")

    compiler = Compiler(WasmNodes)
    binary = compiler.compile(app)

    res = binary.run(in0=10, in1=5, in2=2)
    assert res == (10*5) & 2






