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

import delegator
import pytest

lassen_rules = "src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

#The problem is that there is a mapping problem between coreir port names and hwtypes port names
#I need a generic solution to be able to easily go between each of these.

@pytest.mark.parametrize("arch", [
    #("PE_lut", gen_PE_lut(16), {}),
    ("Lassen", lassen_fc, {}),
    #("ALU", gen_ALU(16), {}),
])
#@pytest.mark.parametrize("app", ["camera_pipeine"])#, "add2", "add1_const", "add4", "add3_const"])
#@pytest.mark.parametrize("app", ["conv_3_3"])#, "add2", "add1_const", "add4", "add3_const"])
#@pytest.mark.parametrize("app", ["add4_pipe"])
@pytest.mark.parametrize("app", ["add3_const"])
def test_app(arch, app):
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{app}.jsontest_full.py"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name)
    app_name = cmod.name
    dag = cutil.coreir_to_dag(CoreIRNodes, cmod)
    name, arch_fc, constraints = arch
    #if name == "ALU" and app == "add_or":
    #    pytest.skip()
    if name == "Lassen":
        rule_file = lassen_rules
    else:
        rule_file = None
    ArchNodes = Nodes("Arch")
    print("1")
    putil.load_from_peak(ArchNodes, arch_fc)
    print("2")
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
