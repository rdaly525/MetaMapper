import metamapper.coreir_util as cutil
from metamapper.common_passes import VerifyNodes, print_dag
from metamapper import CoreIRContext
from metamapper.irs.coreir import gen_CoreIRNodes
import pytest

examples_coreir = [
    "add4_pipe",
    "add2",
    "pipe",
    "add1_const",
    "add3",
    "add4",
    "add3_const"
]

@pytest.mark.parametrize("name", examples_coreir)
def test_examples_coreir(name):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{name}.json"
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name)
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    print_dag(dag)

full_apps = [
    "conv_3_3",
    #"camera_pipeline"
]

@pytest.mark.parametrize("name", full_apps)
def test_apps(name):
    c = CoreIRContext(reset=True)
    file_name = f"apps/{name}.json"
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name, libraries=["commonlib", "lakelib"])
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    cmod.print_()
    print_dag(dag)

