import glob
import jsonpickle
import sys
import importlib
import os
import json
from pathlib import Path
import delegator
import pytest
from lassen import PE_fc as lassen_fc
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import print_dag, gen_dag_img_simp, Constant2CoreIRConstant
from metamapper.delay_matching import STA
from peak.mapper import read_serialized_bindings

class _ArchCycles:
    def get(self, node):
        kind = node.kind()[0]
        if kind == "Rom":
            return 1
        elif kind == "global.PE":
            return 0
        return 0

lassen_header = "./libs/lassen_header.json"

def gen_rrules():

    c = CoreIRContext()
    cmod = putil.peak_to_coreir(lassen_fc)
    c.serialize_header(lassen_header, [cmod])
    # c.serialize_definitions(pe_def, [cmod])
    mapping_funcs = []
    rrules = []
    ops = []

    rrule_files = glob.glob(f'examples/lassen/rewrite_rules/*.json')

    for idx, rrule in enumerate(rrule_files):
        rule_name = Path(rrule).stem
        print(idx, rule_name)
        ops.append(rule_name)

        peak_eq = importlib.import_module(f"examples.lassen.rewrite_rules.{rule_name}")

        ir_fc = getattr(peak_eq, rule_name + "_fc")
        mapping_funcs.append(ir_fc)

        with open(rrule, "r") as json_file:
            rewrite_rule_in = jsonpickle.decode(json_file.read())

        rewrite_rule = read_serialized_bindings(rewrite_rule_in, ir_fc, lassen_fc)
        counter_example = rewrite_rule.verify()
        assert counter_example == None, f"{rule_name} failed"
        print(rule_name, "passed")
        rrules.append(rewrite_rule)

    return rrules, ops

@pytest.mark.parametrize("lat", [
    None,
    #_ArchLatency
])
@pytest.mark.parametrize("app", [
    "pointwise",
    "camera_pipeline"
])
def test_kernel_mapping(lat, app):

    base = "examples/clockwork"
    file_name = f"{base}/{app}_compute.json"

    rrules, ops = gen_rrules()

    c = CoreIRContext(reset=True)
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)

    cutil.load_from_json(file_name)
    kernels = dict(c.global_namespace.modules)

    arch_fc = lassen_fc
    ArchNodes = Nodes("Arch")
    putil.load_and_link_peak(
        ArchNodes,
        lassen_header,
        {"global.PE": arch_fc}
    )
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])

    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=False, ops = ops, rrules=rrules)

    c.run_passes(["rungenerators", "deletedeadinstances"])
    mods = []

    for kname, kmod in kernels.items():
        print(f"Mapping kernel {kname}")
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        Constant2CoreIRConstant(CoreIRNodes).run(dag)

        mapped_dag = mapper.do_mapping(dag, kname=kname, node_cycles=_ArchCycles(), convert_unbound=False, prove_mapping=False)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=False)
        mods.append(mod)