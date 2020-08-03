import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
from metamapper.family import set_fam, fam
import pytest
from hwtypes.adt import Product, Tuple
from metamapper.node import Dag

from metamapper.node import Input, Output

def test_app():
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()
    BV = riscv.family.PyFamily().BitVector
    #Define a simple add3 program
    input = Input(type=Product.from_fields("Input", {"in0": BV[32], "in1": BV[32]}))
    add0 = WasmNodes.dag_nodes["i32.add"](input.select("in0"), input.select("in0"))
    add1 = WasmNodes.dag_nodes["i32.add"](add0.select("out"), input.select("in1"))
    output = Output(add1.select("out"), type=Product.from_fields("Output", {"out":BV[32]}))
    app = Dag(sources=[input], sinks=[output])
    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    compiler = Compiler(WasmNodes, ArchNodes)
    binary = compiler.compile(app)
    res = binary.run(in0=10, in1=5)
    assert res == 25
