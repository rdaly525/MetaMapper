import pytest
import delegator

from lassen import PE_fc as lassen_fc
import coreir
from metamapper.common_passes import print_dag
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper

#Assumes rules are in the src dir created by pip install -r requirements.txt
lassen_rules = "./src/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"


#def load_cgralib_mem(c: coreir.Context, nodes: Nodes):


@pytest.mark.parametrize("arch", [
    ("Lassen", lassen_fc, {}),
])
@pytest.mark.parametrize("app", [
    ("simple_kernel")
    ("pointwise_to_metamapper", "pointwise")])
def test_post_clockwork(arch, app):
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    arch_fc = lassen_fc
    rule_file = lassen_rules
    file_name, app_name = app

    #TODO this really should be loaded as a separate file with only the PE in it
    file_name = f"examples/clockwork/{file_name}.json"
    cutil.load_libs(["float", "commonlib", "cgralib"])
    cutil.load_from_json(file_name)
    #Grab the WrappedPE from the file
    pe_cmod = c.global_namespace.modules["WrappedPE"]


    #Load the ArchNodes namespace with the PE and the Memory tile
    ArchNodes = Nodes("Arch")
    CoreIRNodes = gen_CoreIRNodes(16)
    node = putil.load_from_peak(ArchNodes, arch_fc, cmod=pe_cmod)
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)
    #TODO load with cgralib.Mem

    #Load the coreir const (16 and 1)
    ArchNodes.add_from_nodes(CoreIRNodes, "coreir.const")
    ArchNodes.add_from_nodes(CoreIRNodes, "corebit.const")

    #c.run_passes(["rungenerators", "deletedeadinstances"])
    app_cmod = c.global_namespace.modules[app_name]
    dag = cutil.coreir_to_dag(ArchNodes, app_cmod)
    print_dag(dag)

    #output_file = f"build/{app_name}_bs.json"
    #print(f"saving to {output_file}")
    #c.save_to_file(output_file)
    #assert 0
    mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
    print("Mappped!")
    print_dag(mapped_dag)
    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{app_name}_mapped", convert_unbounds=True)
    mod.print_()
    assert 0

    print(f"Num PEs used: {mapper.num_pes}")
    output_file = f"build/{app_name}_mapped.json"
    print(f"saving to {output_file}")
    c.save_to_file(output_file)

    #c.run_passes(["wireclocks-clk"])
    #c.run_passes(["wireclocks-arst"])
    #c.run_passes(["markdirty"])

    ##Test syntax of serialized json
    #res = delegator.run(f"coreir -i {output_file} -l commonlib")
    #assert not res.return_code, res.out + res.err

    ##Test serializing to verilog
    #res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o build/{app_name}_mapped.v --inline')
    #assert not res.return_code, res.out + res.err

