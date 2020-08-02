from metamapper import CoreIRContext
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
from metamapper.common_passes import SMT, print_dag, prove_equal

def test_dag_to_smt():
    CoreIRContext(reset=True)
    CoreIRNodes = gen_CoreIRNodes(16)

    cmod = cutil.load_from_json("examples/coreir/add1_const.json")
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    print_dag(dag)
    counter_example = prove_equal(dag, dag)
    assert counter_example is None
