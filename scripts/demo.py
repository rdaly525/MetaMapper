from peak.demo.demo_pe import PE_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, Constant2CoreIRConstant, gen_dag_img

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
import json

class _ArchLatency:
    def get(self, node):
        kind = node.kind()[0]
        print(kind)
        if kind == "Rom":
            return 1
        elif kind == "PE":
            return latency
        return 0

app = str(sys.argv[1])
if len(sys.argv) > 2:
    latency = int(sys.argv[2])
else:
    latency = 0

lassen_rules = "../peak/peak/demo/demo_rewrite_rules.json"

verilog = False
print("STARTING TEST")
base = "examples/clockwork"
file_name = f"{base}/{app}.json"

c = CoreIRContext(reset=True)
cutil.load_libs(["commonlib"])
CoreIRNodes = gen_CoreIRNodes(16)

cutil.load_from_json(file_name) 
kernels = dict(c.global_namespace.modules)

ArchNodes = Nodes("Arch")
arch_fc = PE_fc
putil.load_from_peak(ArchNodes, arch_fc)


mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=lassen_rules)

c.run_passes(["rungenerators", "deletedeadinstances"])
mods = []

for kname, kmod in kernels.items():
    if kname == "hcompute_conv_stencil_1":
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        Constant2CoreIRConstant(CoreIRNodes).run(dag)
        gen_dag_img(dag, "premapped")

        mapped_dag = mapper.do_mapping(dag, kname=kname, node_latencies=_ArchLatency(), convert_unbound=False, prove_mapping=False)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)
        mods.append(mod)
        gen_dag_img(mapped_dag, "mapped")

print(f"Num PEs used: {mapper.num_pes}")
output_file = f"outputs/{app}_mapped.json"
print(f"saving to {output_file}")
c.serialize_definitions(output_file, mods)

with open(f'outputs/{app}_kernel_latencies.json', 'w') as outfile:
    json.dump(mapper.kernel_latencies, outfile)
