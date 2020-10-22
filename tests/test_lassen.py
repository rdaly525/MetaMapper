from examples.PEs.alu_basic import gen_ALU
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc
from importlib import reload  

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


from peak.mapper import RewriteRule
from peak.mapper.utils import pretty_print_binding
import glob, jsonpickle
import peak
import shutil 
import sys
import inspect
import importlib
import os




def test_camera():
    print("STARTING TEST")
    app = "laplacian_pyramid"
    c = CoreIRContext(reset=True)
    file_name = f"examples/dse/{app}.json"
    cutil.load_libs(["commonlib"])
    # cutil.load_libs(["lakelib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    c = CoreIRContext()

    cutil.load_from_json(file_name)
    kernels = dict(c.global_namespace.modules)

    # rrules, PE_fc = gen_rrules()
    rrules, PE_fc = None, lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, PE_fc)
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    # breakpoint()
    mapper = Mapper(CoreIRNodes, ArchNodes, peak_rules=rrules, conv=False)
    for kname, kmod in kernels.items():
        mapped_mod = mapper.map_module(cmod=kmod, prove=False)

    print("Num PEs used:",  mapper.num_pes)
    c.run_passes(["wireclocks-clk"])
    c.run_passes(["wireclocks-arst"])
    c.run_passes(["markdirty"])
    output_file= f"examples/dse/{app}_mapped.json"
    c.save_to_file(output_file)