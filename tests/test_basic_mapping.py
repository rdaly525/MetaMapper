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


#This tests loading, mapping, serializing of toy examples


lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

lassen_header = "libs/lassen_header.json"
lassen_def = "libs/lassen_def.json"
mem_header = "libs/mem_header.json"




@pytest.mark.parametrize("app", [
    "add4_pipe",
    "add3_const",
])
#@pytest.mark.parametrize("app", ["add4_pipe"])
def test_kernel_mapping(app):
    base = "examples/coreir"
    app_file = f"{base}/{app}.json"
    build_file = f"tests/build/{app}_mapped.json"

    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(app_file)

    IRNodes = gen_CoreIRNodes(16)

    app_name = cmod.name
    dag = cutil.coreir_to_dag(IRNodes, cmod)
    #print_dag(dag)
    #gen_dag_img(dag, f"img/{app}")

    Constant2CoreIRConstant(IRNodes).run(dag)

    #print_dag(dag)

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(
        ArchNodes,
        lassen_header,
        {"global.PE": arch_fc}
    )

    mapper = Mapper(IRNodes, ArchNodes, lazy=True, rule_file=lassen_rules)
    mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)

    #gen_dag_img(mapped_dag, f"img/{app}_mapped")

    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{app_name}_mapped", convert_unbounds=False)
    c.serialize_definitions(build_file, [mod])


class LatencyInfo:

    @staticmethod
    def get(node):
        if node.node_name == "global.PE":
            return 1
        return 0

@pytest.mark.parametrize("app", [
    "branch"
])
def test_kernel_mapping_with_delay(app):
    base = "examples/coreir"
    app_file = f"{base}/{app}.json"
    build_file = f"tests/build/{app}_mapped.json"

    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(app_file)

    IRNodes = gen_CoreIRNodes(16)

    app_name = cmod.name
    dag = cutil.coreir_to_dag(IRNodes, cmod)

    #gen_dag_img(dag, f"img/{app}")

    Constant2CoreIRConstant(IRNodes).run(dag)
    print_dag(dag)

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(
        ArchNodes,
        lassen_header,
        {"global.PE": arch_fc}
    )

    mapper = Mapper(IRNodes, ArchNodes, lazy=True, rule_file=lassen_rules)
    mapped_dag = mapper.do_mapping(dag, node_latencies=LatencyInfo, convert_unbound=False, prove_mapping=False)

    #gen_dag_img(mapped_dag, f"img/{app}_mapped")
    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{app_name}_mapped", convert_unbounds=False)
    c.serialize_definitions(build_file, [mod])



@pytest.mark.parametrize("app", [
    "add3_const",
    "add4_pipe",
    "branch"
])
def test_post_mapped_loading(app):
    base = "examples/post_mapping"
    app_file = f"{base}/{app}_mapped.json"
    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(app_file)
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

    dag = cutil.coreir_to_dag(IRNodes, cmod)
    #print_dag(dag)
    #gen_dag_img(dag, f"img/{app}_mapped_loaded")
