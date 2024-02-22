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
        if kind == "Rom" or kind == "FPRom" or kind == "PipelineRegister":
            return 1
        elif kind == "global.PE":
            if "PIPELINED" in os.environ and os.environ["PIPELINED"].isnumeric():    
                pe_cycles = int(os.environ["PIPELINED"])
            else:
                pe_cycles = 1
            return pe_cycles
        return 0


lassen_location = os.path.join(Path(__file__).parent.parent.parent.resolve(), "lassen")
lassen_header = os.path.join(
    Path(__file__).parent.parent.resolve(), "libs/lassen_header.json"
)


def gen_rrules(pipelined=False):

    # c = CoreIRContext()
    # cmod = putil.peak_to_coreir(lassen_fc)
    # c.serialize_header(lassen_header, [cmod])
    # c.serialize_definitions(pe_def, [cmod])
    mapping_funcs = []
    rrules = []
    ops = []

    rrule_files = glob.glob(f"{lassen_location}/lassen/rewrite_rules/*.json")

    # Can't have a '.' in the name of the rule since they are files
    custom_rule_names = {
        "mult_middle": "commonlib.mult_middle",
        "abs": "commonlib.abs",
        "fp_exp": "float.exp",
        "fp_max": "float.max",
        "fp_div": "float.div",
        "fp_mux": "float.mux",
        "fp_mul": "float_DW.fp_mul",
        "fp_add": "float_DW.fp_add",
        "fp_sub": "float.sub",
        "fp_gt": "float.gt",
        "fp_lt": "float.lt",
        "fp_ge": "float.ge",
        "fp_le": "float.le",
        "fp_eq": "float.eq"
    }

    for idx, rrule in enumerate(rrule_files):
        rule_name = Path(rrule).stem
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

        if False:
            counter_example = rewrite_rule.verify()
            assert counter_example == None, f"{rule_name} failed"
        rrules.append(rewrite_rule)

    return rrules, ops


def map_design_top(app_name, nodes, dag):
    pe_reg_instrs = {}
    pe_reg_instrs["const"] = 0
    pe_reg_instrs["bypass"] = 2
    pe_reg_instrs["reg"] = 3

    pe_port_to_reg = {}
    pe_port_to_reg["data0"] = "rega"
    pe_port_to_reg["data1"] = "regb"
    pe_port_to_reg["data2"] = "regc"

    pe_port_to_reg["bit0"] = "regd"
    pe_port_to_reg["bit1"] = "rege"
    pe_port_to_reg["bit2"] = "regf"

    pe_reg_info = {}
    pe_reg_info['instrs'] = pe_reg_instrs
    pe_reg_info['port_to_reg'] = pe_port_to_reg

    pipelined = not ("PIPELINED" in os.environ and os.environ["PIPELINED"] == '0')

    CoreIRNodes = gen_CoreIRNodes(16)

    rrules, ops = gen_rrules()

    mapper = Mapper(CoreIRNodes, nodes, lazy=False, ops=ops, rrules=rrules, kernel_name_prefix=True)
 
    mapped_dag = mapper.do_mapping(dag, kname=app_name, node_cycles=None, convert_unbound=False, prove_mapping=False, pe_reg_info=pe_reg_info)

    return mapped_dag
