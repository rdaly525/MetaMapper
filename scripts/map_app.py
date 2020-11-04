from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag

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


    
app = str(sys.argv[1])

PE_fc = lassen_fc

lassen_rules = "../lassen/scripts/rewrite_rules/lassen_rewrite_rules.json"

c = CoreIRContext(reset=True)
file_name = f"examples/clockwork/{app}.json"
cutil.load_libs(["commonlib"])
CoreIRNodes = gen_CoreIRNodes(16)
cutil.load_from_json(file_name) #libraries=["lakelib"])
kernels = dict(c.global_namespace.modules)

arch_fc = lassen_fc
rule_file = lassen_rules

ArchNodes = Nodes("Arch")
putil.load_from_peak(ArchNodes, arch_fc)
mr = "memory.rom2"
ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rule_file=rule_file)

for kname, kmod in kernels.items():
# kname = "hcompute_blur_unnormalized_stencil"
# kmod = kernels[kname]
    print(kname)
    
    dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
    print_dag(dag)
    mapped_dag = mapper.do_mapping(dag, prove_mapping=False)    


print(f"Num PEs used: {mapper.num_pes}")
c.run_passes(["wireclocks-clk"])
c.run_passes(["wireclocks-arst"])
c.run_passes(["markdirty"])
output_file= f"examples/clockwork/{app}_mapped.json"
c.save_to_file(output_file)

#Test syntax of serialized json
res = delegator.run(f"coreir -i {output_file} -l commonlib")
assert not res.return_code, res.out + res.err

#Test serializing to verilog
res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o examples/clockwork/{app}_mapped.v --inline')
assert not res.return_code, res.out + res.err
