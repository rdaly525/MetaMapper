from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, gen_dag_img_simp, Constant2CoreIRConstant
from metamapper.delay_matching import STA
import delegator
import pytest
from hwtypes import BitVector, Tuple, Bit, bit_vector

from peak_gen.sim import fp_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch, graph_arch
from peak_gen.isa import inst_arch_closure
from peak_gen.peak_wrapper import wrapped_peak_class
from peak.mapper import RewriteRule
from peak.mapper.utils import pretty_print_binding
import glob, jsonpickle
import peak
import shutil
import sys
import inspect
import importlib
import os
from lassen.sim import PE_fc as lassen_fc
import json


class _ArchCycles:
    def get(self, node):
        kind = node.kind()[0]
        if kind == "Rom":
            return 1
        elif kind == "global.PE":
            return pe_cycles
        return 0


file_name = str(sys.argv[1])
if len(sys.argv) > 2:
    pe_cycles = int(sys.argv[2])
else:
    pe_cycles = 0

if pe_cycles != 0:
    lassen_rules = "/aha/lassen/scripts/rewrite_rules/lassen_rewrite_rules_pipelined.json"
else:
    lassen_rules = "/aha/lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

lassen_header = "/aha/MetaMapper/libs/lassen_header.json"
lassen_def = "/aha/MetaMapper/libs/lassen_def.json"

verilog = False
app = os.path.basename(file_name).split(".json")[0]
output_dir = os.path.dirname(file_name)

c = CoreIRContext(reset=True)
cutil.load_libs(["commonlib"])
CoreIRNodes = gen_CoreIRNodes(16)

cutil.load_from_json(file_name) #libraries=["lakelib"])
kernels = dict(c.global_namespace.modules)


arch_fc = lassen_fc
ArchNodes = Nodes("Arch")
putil.load_and_link_peak(
    ArchNodes,
    lassen_header,
    {"global.PE": arch_fc}
)
#putil.load_from_peak(ArchNodes, arch_fc)
mr = "memory.rom2"
ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])


mapper = Mapper(CoreIRNodes, ArchNodes, rule_file=lassen_rules)

c.run_passes(["rungenerators", "deletedeadinstances"])
mods = []

for kname, kmod in kernels.items():
    print(f"Mapping kernel {kname}")
    dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
    Constant2CoreIRConstant(CoreIRNodes).run(dag)

    mapped_dag = mapper.do_mapping(dag, kname=kname, node_cycles=_ArchCycles(), convert_unbound=False, prove_mapping=False)
 #   gen_dag_img_simp(mapped_dag, f"img/{kname}")
#    print(STA(pe_cycles).doit(mapped_dag))
    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)
    mods.append(mod)

print(f"Num PEs used: {mapper.num_pes}")
output_file = f"{output_dir}/{app}_mapped.json"
print(f"saving to {output_file}")
c.serialize_definitions(output_file, mods)

with open(f'{output_dir}/{app}_kernel_latencies.json', 'w') as outfile:
    json.dump(mapper.kernel_cycles, outfile)

