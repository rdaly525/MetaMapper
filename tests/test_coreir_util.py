import metamapper.coreir_util as cutil
from metamapper.common_passes import VerifyNodes
from metamapper import CoreIRContext
from metamapper.irs.coreir import gen_CoreIRNodes

def test_coreir_to_dag():
    CoreIRContext(reset=True)
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json("examples/add4.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    VerifyNodes(CoreIRNodes).run(dag)
