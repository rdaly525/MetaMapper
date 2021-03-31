from examples.PEs.alu_basic import gen_ALU
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc

from metamapper.common_passes import print_dag
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
import coreir

import delegator
import pytest

lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

#The problem is that there is a mapping problem between coreir port names and hwtypes port names
#I need a generic solution to be able to easily go between each of these.



lassen_header = "build/lassen_header.json"
lassen_def = "build/lassen_def.json"

#Compiles
def compile_PE_spec(arch_fc: "peak_fc", header_file: str, def_file: str):
    cmod = putil.peak_to_coreir(arch_fc)
    c = CoreIRContext()
    c.save_header(header_file, [cmod.ref_name])
    c.save_definitions(def_file, [cmod.ref_name])

#Loads a coreir header file, associates each coreir file with a peak_fc, creates a dag_node in nodes
def load_and_link_peak(nodes: Nodes, header_file: str, peak_dict: dict):
    c = CoreIRContext()
    header_modules = c.load_header(header_file)
    for cmod in header_modules:
        if cmod.ref_name not in peak_dict:
            raise ValueError(f"{cmod.ref_name} does not have an associated peak_dict")
        peak_fc = peak_dict[cmod.ref_name]
        node_name = putil.load_from_peak(nodes, peak_fc, stateful=False, cmod=cmod, name=cmod.ref_name)
        assert node_name == cmod.ref_name


@pytest.mark.parametrize("app", ["add3_const"])
def test_app(app):

    #Done once during spec generation
    c = CoreIRContext(reset=True)
    compile_PE_spec(lassen_fc, lassen_header, lassen_def)

    #Loading
    c = CoreIRContext(reset=True)
    cmod = cutil.load_from_json(file_name)

    CoreIRNodes = gen_CoreIRNodes(16)
    app_name = cmod.name
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    name, arch_fc, constraints = arch
    rule_file = lassen_rules
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)
    mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
    print_dag(mapped_dag)
    ArchNodes.copy(CoreIRNodes, "coreir.reg")
    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{app_name}_mapped", convert_unbounds=False)
    mod.print_()
    output_file= f"build/{app}_mapped.json"
    c.set_top(mod)
    for n,m in c.get_namespace("global").modules.items():
        print("M", n, flush=True)
        m.print_()

    c.save_to_file(output_file)
    mod.print_()

#test_app(("PE_lut", gen_PE_lut(16), {}),"add2")
