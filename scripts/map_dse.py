from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, Constant2CoreIRConstant, gen_dag_img

from peak_gen.arch import read_arch
from peak_gen.peak_wrapper import wrapped_peak_class

from peak.mapper import read_serialized_bindings

import delegator
import pytest
import glob
import importlib
import sys, os
import json

class _ArchLatency:
    def get(self, node):
        kind = node.kind()[0]
        print(kind)
        if kind == "Rom":
            return 1
        elif kind == "global.PE":
            return latency
        
        return 0

app = str(sys.argv[1])
if len(sys.argv) > 2:
    latency = int(sys.argv[2])
else:
    latency = 0

metamapper_location = "/aha/MetaMapper"
DSE_PE_location = "/aha/DSEGraphAnalysis/outputs"
pe_header = f"{metamapper_location}/libs/pe_header.json"
pe_def = f"{metamapper_location}/libs/pe_def.json"

def gen_rrules():

    arch = read_arch(f"{DSE_PE_location}/PE.json")
    PE_fc = wrapped_peak_class(arch, debug=True)
    c = CoreIRContext()
    cmod = putil.peak_to_coreir(PE_fc)
    c.serialize_header(pe_header, [cmod])
    # c.serialize_definitions(pe_def, [cmod])
    mapping_funcs = []
    rrules = []

    num_rrules = len(glob.glob(f'{DSE_PE_location}/rewrite_rules/*.json'))

    if not os.path.exists(f'{metamapper_location}/examples/peak_gen'):
        os.makedirs(f'{metamapper_location}/examples/peak_gen')

    for ind in range(num_rrules):

        with open(f"{DSE_PE_location}/peak_eqs/peak_eq_" + str(ind) + ".py", "r") as file:
            with open(f"{metamapper_location}/examples/peak_gen/peak_eq_" + str(ind) + ".py", "w") as outfile:
                for line in file:
                    outfile.write(line.replace('mapping_function', 'mapping_function_'+str(ind)))
        peak_eq = importlib.import_module("examples.peak_gen.peak_eq_" + str(ind))

        ir_fc = getattr(peak_eq, "mapping_function_" + str(ind) + "_fc")
        mapping_funcs.append(ir_fc)

        with open(f"{DSE_PE_location}/rewrite_rules/rewrite_rule_" + str(ind) + ".json", "r") as json_file:
            rewrite_rule_in = json.load(json_file)

        rewrite_rule = read_serialized_bindings(rewrite_rule_in, ir_fc, PE_fc)
        counter_example = rewrite_rule.verify()


        rrules.append(rewrite_rule)
    return PE_fc, rrules



arch_fc, rrules = gen_rrules()
verilog = False
print("STARTING TEST")

file_name = str(sys.argv[1])
app = os.path.basename(file_name).split(".json")[0]
output_dir = os.path.dirname(file_name)

c = CoreIRContext(reset=True)
cutil.load_libs(["commonlib"])
CoreIRNodes = gen_CoreIRNodes(16)
cutil.load_from_json(file_name) #libraries=["lakelib"])
c.run_passes(["rungenerators"])
kernels = dict(c.global_namespace.modules)


ArchNodes = Nodes("Arch")
putil.load_and_link_peak(
    ArchNodes,
    pe_header,
    {"global.PE": arch_fc}
)
# putil.load_from_peak(ArchNodes, arch_fc)
#mr = "memory.rom2"
#ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])

mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rrules=rrules)

mods = []
for kname, kmod in kernels.items():
    print(kname)
    dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
    Constant2CoreIRConstant(CoreIRNodes).run(dag)
    mapped_dag = mapper.do_mapping(dag, kname=kname, node_cycles=_ArchLatency(), convert_unbound=False, prove_mapping=False)        
    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)
    mods.append(mod)

print(f"Num PEs used: {mapper.num_pes}")
output_file = f"{output_dir}/{app}_mapped.json"
print(f"saving to {output_file}")
c.serialize_definitions(output_file, mods)


with open(f'{output_dir}/{app}_kernel_latencies.json', 'w') as outfile:
    json.dump(mapper.kernel_cycles, outfile)
