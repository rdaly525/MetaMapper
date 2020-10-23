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
if len(sys.argv) > 2:
    print("Mapping with custom PEs not working yet")
    exit()
    arch = read_arch(str(sys.argv[2]))
    PE_fc = wrapped_peak_class(arch)
else:
    PE_fc = lassen_fc


c = CoreIRContext(reset=True)
file_name = f"examples/mapping/{app}.json"
cutil.load_libs(["commonlib"])
# cutil.load_libs(["lakelib"])
CoreIRNodes = gen_CoreIRNodes(16)
c = CoreIRContext()

cutil.load_from_json(file_name)
kernels = dict(c.global_namespace.modules)


ArchNodes = Nodes("Arch")
putil.load_from_peak(ArchNodes, PE_fc)
mr = "memory.rom2"
ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
mapper = Mapper(CoreIRNodes, ArchNodes, conv=False)
for kname, kmod in kernels.items():
    mapped_mod = mapper.map_module(cmod=kmod, prove=False)

c.run_passes(["wireclocks-clk"])
c.run_passes(["wireclocks-arst"])
c.run_passes(["markdirty"])
output_file= f"examples/mapping/{app}_mapped.json"
c.save_to_file(output_file)
