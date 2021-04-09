import metamapper.coreir_util as cutil
from metamapper.common_passes import VerifyNodes, print_dag
from metamapper import CoreIRContext
from metamapper.irs.coreir import gen_CoreIRNodes
import pytest


examples_coreir = [
    "add2",
    "multi",
    #"add4_pipe_mapped",
    #"add4_pipe",
    #"pipe",
    #"add1_const",
    #"add3",
    #"add4",
    #"add3_const"
]


@pytest.mark.parametrize("name", examples_coreir)
def test_examples_coreir(name):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{name}.json"
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name)

    kernels = dict(c.global_namespace.modules)
    for kname, kmod in kernels.items():
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        cutil.dag_to_coreir(CoreIRNodes, dag, f"{kname}_copy")
    out_name = f"build/{name}_copy.json"
    c.save_to_file(out_name)




full_apps = [
    "gaussian_compute",
]
@pytest.mark.parametrize("name", full_apps)
def test_apps(name):
    c = CoreIRContext(reset=True)
    file_name = f"examples/clockwork/{name}.json"
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name)

    kernels = dict(c.global_namespace.modules)
    for kname, kmod in kernels.items():
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        print_dag(dag)
        cutil.dag_to_coreir(CoreIRNodes, dag, f"{kname}_copy")
        print(kname, "complete")
    out_name = f"build/{name}_copy.json"
    c.save_to_file(out_name)

