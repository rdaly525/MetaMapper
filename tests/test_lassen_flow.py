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

#@pytest.mark.parametrize("app", ["add3_const"])
@pytest.mark.parametrize("app", ["add4_pipe"])
def test_app(app):
    base = "examples/coreir"
    app_file = f"{base}/{app}.json"
    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(app_file)

    #Contains an empty nodes
    IRNodes = gen_CoreIRNodes(16)

    app_name = cmod.name
    dag = cutil.coreir_to_dag(IRNodes, cmod)

    #print_dag(dag)
    gen_dag_img(dag, f"img/{app}")

    Constant2CoreIRConstant(IRNodes).run(dag)
    print_dag(dag)

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(
        ArchNodes,
        lassen_header,
        {"global.PE": arch_fc}
    )
    ArchNodes.copy(IRNodes, "coreir.reg")

    rule_file = lassen_rules

    mapper = Mapper(IRNodes, ArchNodes, lazy=True, rule_file=rule_file)
    mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
    print_dag(mapped_dag)
    gen_dag_img(mapped_dag, f"img/{app}_mapped")

    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{app_name}_mapped", convert_unbounds=False)
    mod.print_()
    output_file = f"tests/build/{app}_mapped.json"
    c.serialize_definitions(output_file, [mod])



@pytest.mark.parametrize("app", [
    #"add3_const_mapped",
    #"add4_pipe_mapped",
    "pointwise_to_metamapper",
    #"gaussian_to_metamapper",
    #"harris_to_metamapper",
])
def test_post_mapped(app):
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
    return
    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(ArchNodes, lassen_header, {"global.PE": arch_fc})

    #rule_file = lassen_rules
    #mapper = Mapper(IRNodes, ArchNodes, lazy=True, rule_file=rule_file)
    #mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)

    mod = cutil.dag_to_coreir(ArchNodes, dag, f"{app_name}_mapped_mapped", convert_unbounds=False)
    mod.print_()
    output_file = f"tests/build/{app}_mapped_mapped.json"
    c.serialize_definitions(output_file, [mod])




