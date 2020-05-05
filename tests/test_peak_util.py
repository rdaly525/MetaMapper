from peak.mapper import RewriteRule as PeakRule
import metamapper.peak_util as putil
from metamapper.node import Nodes
from examples.alu import gen_ALU
from metamapper import CoreIRContext
import metamapper.coreir_util as cutil
from metamapper.irs.coreir import gen_CoreIRNodes
from peak import Peak, family_closure
import pytest

def test_peak_to_node():
    ArchNodes = Nodes("Arch")
    ALU_fc = gen_ALU(16)
    dag_name = putil.peak_to_node(ArchNodes, ALU_fc)
    assert dag_name == "ALU"
    dag_node = ArchNodes.dag_nodes[dag_name]
    assert dag_node.input_names() == ["inst", "a", "b"]
    assert dag_node.output_names() == [0]

@pytest.mark.skip()
def test_dag_to_peak():
    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(c, "examples/add4.json")
    CoreIRNodes = gen_CoreIRNodes(16)
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    peak_fc = putil.dag_to_peak(CoreIRNodes, dag)

    #Verify using a peak rewrite rule
    @family_closure
    def Add4_fc(family):
        Data = family.BitVector[16]
        @family.assemble(globals(), locals())
        class Add4(Peak):
            def __call__(a:Data, b:Data, c:Data, d:Data) -> Data:
                return (a+b) + (c+d)
        return Add4

    rule = PeakRule(
        peak_fc,
        Add4_fc,
        ibinding=[
            (("in0",), ("a",)),
            (("in1",), ("b",)),
            (("in2",), ("c",)),
            (("in3",), ("d",)),
        ],
        obinding=[("out",), (0,)],
    )
    ce = rule.verify()
    assert ce is not None

