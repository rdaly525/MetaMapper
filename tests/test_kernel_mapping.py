import pytest
import glob
import sys
import importlib
import os
import json
from pathlib import Path
import delegator

from lassen import PE_fc as lassen_fc
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, gen_dag_img, Constant2CoreIRConstant
from peak.mapper import read_serialized_bindings

class _ArchCycles:
    def get(self, node):
        kind = node.kind()[0]
        if kind == "Rom":
            return 1
        elif kind == "global.PE":
            return 0
        return 0

class _ArchCyclesPipelined:
    def get(self, node):
        kind = node.kind()[0]
        if kind == "Rom":
            return 1
        elif kind == "global.PE":
            return 1
        return 1

lassen_location = "src/lassen"
lassen_header = "libs/lassen_header.json"

def gen_rrules(pipelined=False):

    c = CoreIRContext(reset=True)
    cmod = putil.peak_to_coreir(lassen_fc)
    c.serialize_header(lassen_header, [cmod])
    mapping_funcs = []
    rrules = []
    ops = []

    if pipelined:
        rrule_files = glob.glob(f'{lassen_location}/lassen/rewrite_rules/*_pipelined.json')
    else:
        rrule_files = glob.glob(f'{lassen_location}/lassen/rewrite_rules/*.json')
        rrule_files = [rrule_file for rrule_file in rrule_files if "pipelined" not in rrule_file]

    custom_rule_names = {"mult_middle":"commonlib.mult_middle","fp_exp": "float.exp", "fp_div": "float.div", "fp_mux": "float.mux", "fp_mul":"float_DW.fp_mul", "fp_add":"float_DW.fp_add", "fp_sub":"float.sub"}

    for idx, rrule in enumerate(rrule_files):
        rule_name = Path(rrule).stem
        if ("fp" in rule_name and "pipelined" in rule_name) or rule_name.split("_pipelined")[0] in custom_rule_names:
            rule_name = rule_name.split("_pipelined")[0]
        if rule_name in custom_rule_names:
            ops.append(custom_rule_names[rule_name])
        else:
            ops.append(rule_name)
        peak_eq = importlib.import_module(f"lassen.rewrite_rules.{rule_name}")
        ir_fc = getattr(peak_eq, rule_name + "_fc")
        mapping_funcs.append(ir_fc)

        with open(rrule, "r") as json_file:
            rewrite_rule_in = json.load(json_file)

        rewrite_rule = read_serialized_bindings(rewrite_rule_in, ir_fc, lassen_fc)

        rrules.append(rewrite_rule)

    return rrules, ops


@pytest.mark.parametrize("pipelined", [
    True,
    False
])
@pytest.mark.parametrize("app", [
    "camera_pipeline",
    "gaussian",
    "harris",
])
def test_kernel_mapping(pipelined, app):

    verilog = False
    base = "examples/clockwork"
    app_file = f"{base}/{app}_compute.json"
    if pipelined:
        mapped_file = f"tests/build/{app}_mapped.json"
        archcycles = _ArchCycles()
    else:
        mapped_file = f"tests/build/{app}_delay_mapped.json"
        archcycles = _ArchCyclesPipelined()

    rrules, ops = gen_rrules(pipelined = pipelined)

    c = CoreIRContext(reset=True)
    cutil.load_libs(["commonlib", "float_DW"])
    CoreIRNodes = gen_CoreIRNodes(16)

    cutil.load_from_json(app_file)
    c.run_passes(["rungenerators", "deletedeadinstances"])
    kernels = dict(c.global_namespace.modules)

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(
        ArchNodes,
        lassen_header,
        {"global.PE": arch_fc}
    )

    mr = "memory.fprom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])

    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=False, ops = ops, rrules=rrules)

    c.run_passes(["rungenerators", "deletedeadinstances"])
    mods = []

    for kname, kmod in kernels.items():
        print(f"Mapping kernel {kname}")
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod, archnodes=ArchNodes)
        Constant2CoreIRConstant(CoreIRNodes).run(dag)

        mapped_dag = mapper.do_mapping(dag, kname=kname, node_cycles=archcycles, convert_unbound=False, prove_mapping=False)

        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)
        mods.append(mod)
    print(f"saving to {mapped_file}")
    c.serialize_definitions(mapped_file, mods)
