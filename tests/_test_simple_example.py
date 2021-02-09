from peak.mapper import RewriteRule as PeakRule
import metamapper.peak_util as putil
from metamapper.node import Nodes, Input, Output, Constant
from examples.PEs.alu_basic import gen_ALU
from metamapper import CoreIRContext
import metamapper.coreir_util as cutil
from metamapper.irs.coreir import gen_CoreIRNodes
from peak import Peak, family_closure, name_outputs, Const
from hwtypes import Product
from peak.family import PyFamily
from metamapper.node import Dag
from metamapper.common_passes import print_dag
import pytest
import delegator

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
    fma2 = FMANode(Constant(value=BV16(2), type=BV16), in2, fma1.select(0))
    output_node = Output(fma2.select(0), type=output_type)
    dag = Dag(sources=[input_node], sinks=[output_node])

    #You can print the dag
    print_dag(dag)

    #Compile the dag to coreir, then to verilog
    coreir_module = cutil.dag_to_coreir(MyNodes, dag, name="my_module")

    c.set_top(coreir_module)
    c.run_passes(["cullgraph"])
    file = f"tests/build/simple"
    coreir_module.save_to_file(f"{file}.json")

    #Test syntax of serialized json
    res = delegator.run(f"coreir -i {file}.json -l commonlib")
    assert not res.return_code, res.out + res.err

    #Test serializing to verilog
    res = delegator.run(f'coreir -i {file}.json -l commonlib -p "wireclocks-clk; wireclocks-arst" -o {file}.v --inline')
    assert not res.return_code, res.out + res.err

