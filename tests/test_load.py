import coreir
import metamapper.coreir_util as cutil
from metamapper.common_passes import VerifyNodes

def test_coreir_to_dag():
    c = CoreIRContext()
    cmod = cutil.load_from_json(c, "examples/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    VerifyNodes(CoreIRNodes, dag)
    for i in range(4):
        assert dag.inputs[i].idx == f"in{i}"
    assert len(dag.outputs) == 1
    assert expr.outputs[0].idx == "out"
