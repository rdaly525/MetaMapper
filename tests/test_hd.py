import metamapper.peak_util as putil
from metamapper.node import Nodes, Input, Output, Constant
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
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


    print("Need to search for", op_cnt.keys())
    compiler = Compiler(WasmNodes, ops=op_cnt.keys(), solver='z3')
    #compiler = Compiler(WasmNodes, ArchNodes, ops=op_cnt.keys(), solver='btor')
    binary = compiler.compile(app)

    # res = binary.run(in0=10, in1=5, in2=2)


@pytest.mark.parametrize("args", [
    (gen_ALU(16), 3, "ALU"),
    #(lassen_fc, 10, "PE"),
])
def test_peak_to_node(args):
    c = CoreIRContext(reset=True)
    MyNodes = Nodes("MyNodes")

    # Create an FMA node based off a peak class
    @family_closure
    def FMA_fc(family):
        Data = family.Unsigned[16]
        class Config(Product):
            imm=Data
        @family.assemble(globals(), locals())
        class FMA(Peak):
            @name_outputs(out=Data)
            def __call__(self, config: Const(Config), a:Data, b:Data) -> Data:
                return a*config.imm + b
        return FMA

    putil.load_from_peak(MyNodes, FMA_fc, stateful=False)
    FMANode = MyNodes.dag_nodes["FMA"]

    # Create Dag using FMA nodes
    BV16 = PyFamily().BitVector[16]
    input_type = Product.from_fields("Input", {"in0":BV16, "in1":BV16, "in2":BV16})
    output_type = Product.from_fields("Output", {"out":BV16})

    input_node = Input(type=input_type)
    in0 = input_node.select("in0")
    in1 = input_node.select("in1")
    in2 = input_node.select("in2")
    fma1 = FMANode(Constant(value=BV16(5), type=BV16), in0, in1)
    fma2 = FMANode(Constant(value=BV16(2), type=BV16), in2, fma1.select("out"))
    output_node = Output(fma2.select("out"), type=output_type)
    dag = Dag(sources=[input_node], sinks=[output_node])

    #You can print the dag
    print_dag(dag)

