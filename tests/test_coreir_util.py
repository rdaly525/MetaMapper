import metamapper.coreir_util as cutil
from metamapper.common_passes import VerifyNodes
from metamapper import CoreIRContext
from metamapper.irs.coreir import gen_CoreIRNodes

def test_coreir_to_dag():
    c = CoreIRContext(reset=True)
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(c, "examples/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    VerifyNodes(CoreIRNodes, dag)
    for i in range(4):
        assert dag.inputs[i].idx == f"in{i}"
    assert len(dag.outputs) == 1
    assert dag.outputs[0].idx == "out"
