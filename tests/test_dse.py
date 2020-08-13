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


def gen_rrules():

    # for ind, name in enumerate(glob.glob('examples/peak_gen/rewrite_rules/*.json')): 
    #     try:
    #         os.remove(name)
    #         os.remove("examples/peak_gen/peak_eqs/peak_eq_" + str(ind) + ".py")
    #         os.remove("examples/peak_gen/subgraph_arch_merged.json")
    #     except:
    #         pass

    # mapping_funcs = []

    # shutil.copyfile("../DSEGraphAnalysis/outputs/subgraph_archs/subgraph_arch_merged.json", "examples/peak_gen/subgraph_arch_merged.json")
    # for ind, name in enumerate(glob.glob('../DSEGraphAnalysis/outputs/subgraph_rewrite_rules/*.json')): 
    #     shutil.copyfile("../DSEGraphAnalysis/outputs/subgraph_rewrite_rules/subgraph_rr_" + str(ind) + ".json", "examples/peak_gen/rewrite_rules/subgraph_rr_" + str(ind) + ".json")
    #     shutil.copyfile("../DSEGraphAnalysis/outputs/peak_eqs/peak_eq_" + str(ind) + ".py", "examples/peak_gen/peak_eqs/peak_eq_" + str(ind) + ".py")

    #     with open("../DSEGraphAnalysis/outputs/peak_eqs/peak_eq_" + str(ind) + ".py", "r") as file:
    #         with open("examples/peak_gen/peak_eqs/peak_eq_" + str(ind) + ".py", "w") as outfile:
    #             for line in file:
    #                 outfile.write(line.replace('mapping_function', 'mapping_function_'+str(ind)))

    #     peak_eq = importlib.import_module("examples.peak_gen.peak_eqs.peak_eq_" + str(ind))

    #     mapping_funcs.append(getattr(peak_eq, "mapping_function_" + str(ind) + "_fc"))

    mapping_funcs = []
    for ind, name in enumerate(glob.glob('examples/peak_gen/peak_eqs/*.py')):
        peak_eq = importlib.import_module("examples.peak_gen.peak_eqs.peak_eq_" + str(ind))

        mapping_funcs.append(getattr(peak_eq, "mapping_function_" + str(ind) + "_fc"))

    arch = read_arch("examples/peak_gen/subgraph_arch_merged.json")
    PE_fc = wrapped_peak_class(arch)

    rrules = []

    for ind, name in enumerate(glob.glob('examples/peak_gen/rewrite_rules/*.json')):
        #if ind==1:
        #    break
        print("examples/peak_gen/rewrite_rules/subgraph_rr_" + str(ind) + ".json")
        with open("examples/peak_gen/rewrite_rules/subgraph_rr_" + str(ind) + ".json") as json_file:
            rewrite_rule_in = jsonpickle.decode(json_file.read())

        input_binding = []

        input_binding_tmp = rewrite_rule_in["ibinding"]
        # breakpoint()

        for i in input_binding_tmp:
            if i[1][0] != "fp_vals":
                if isinstance(i[0], dict):
                    u = i[0]
                    v = i[1]
                    if u['type'] == "BitVector":
                        u = (BitVector[u['width']](u['value']))
                    elif u['type'] == "Bit":
                        u = (Bit(u['value']))

                    input_binding.append(tuple([u, tuple(v) ]))
                elif i[0] == "unbound":
                    input_binding.append(tuple( [peak.mapper.utils.Unbound, tuple(i[1])] ))
                else:
                    input_binding.append(tuple( [tuple(i[0]), tuple(i[1])] ))


        output_binding_tmp = rewrite_rule_in["obinding"]
        output_binding = []

        for o in output_binding_tmp:
            output_binding.append(tuple( [tuple(o[0]), tuple(o[1])] ))

        #pretty_print_binding(input_binding)
        #pretty_print_binding(output_binding)
        rrules.append(RewriteRule(input_binding, output_binding, mapping_funcs[ind], PE_fc))
    return rrules, PE_fc

def test_camera():
    print("STARTING TEST")
    app = "gaussian"
    c = CoreIRContext(reset=True)
    file_name = f"examples/dse/{app}.json"
    cutil.load_libs(["commonlib"])
    # cutil.load_libs(["lakelib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    c = CoreIRContext()

    cutil.load_from_json(file_name)
    kernels = dict(c.global_namespace.modules)

    rrules, PE_fc = gen_rrules()
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, PE_fc)
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    # breakpoint()
    mapper = Mapper(CoreIRNodes, ArchNodes, peak_rules=rrules, conv=False)
    for kname, kmod in kernels.items():
        mapped_mod = mapper.map_module(cmod=kmod, prove=False)
    c.run_passes(["wireclocks-clk"])
    c.run_passes(["wireclocks-arst"])
    c.run_passes(["markdirty"])
    output_file= f"examples/dse/{app}_mapped.json"
    c.save_to_file(output_file)
