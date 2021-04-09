from lassen import PE_fc as lassen_fc

from metamapper.common_passes import print_dag, Constant2CoreIRConstant, gen_dag_img
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.lake_mem import gen_MEM_fc

import pytest

lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

lassen_header = "libs/lassen_header.json"
lassen_def = "libs/lassen_def.json"
mem_header = "libs/mem_header.json"



#Test first part of netlist generation: loading the post_mapped files
@pytest.mark.parametrize("app", [
    "pointwise_to_metamapper",
    "gaussian_to_metamapper",
    "harris_to_metamapper",
])
def test_post_mapped_loading(app):
    base = "examples/post_mapping"
    app_file = f"{base}/{app}.json"
    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(app_file)
    cmod.print_()

    MEM_fc = gen_MEM_fc()
    # Contains an empty nodes
    IRNodes = gen_CoreIRNodes(16)
    putil.load_and_link_peak(
        IRNodes,
        lassen_header,
        {"global.PE": lassen_fc},
    )
    putil.load_and_link_peak(
        IRNodes,
        mem_header,
        {"global.MEM": MEM_fc},
    )
    app_name = cmod.name
    dag = cutil.coreir_to_dag(IRNodes, cmod)
    gen_dag_img(dag, f"img/{app}_mapped")
    print_dag(dag)
