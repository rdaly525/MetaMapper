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
            return 1 if pipelined else 0
        return 0


lassen_location = os.path.join(Path(__file__).parent.parent.parent.resolve(), "lassen")
lassen_header = os.path.join(
    Path(__file__).parent.parent.resolve(), "libs/lassen_header.json"
)


def gen_rrules(pipelined=False):

    c = CoreIRContext()
    cmod = putil.peak_to_coreir(lassen_fc)
    c.serialize_header(lassen_header, [cmod])
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

        counter_example = rewrite_rule.verify()
        assert counter_example == None, f"{rule_name} failed"
        rrules.append(rewrite_rule)

    return rrules, ops


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
pe_reg_info["instrs"] = pe_reg_instrs
pe_reg_info["port_to_reg"] = pe_port_to_reg

file_name = str(sys.argv[1])

if "MATCH_BRANCH_DELAY" in os.environ and os.environ["MATCH_BRANCH_DELAY"] in ["0", "1"]:
    match_branch_delay = bool(int(os.environ["MATCH_BRANCH_DELAY"]))
else:
    match_branch_delay = True 

pipelined = not ("PIPELINED" in os.environ and os.environ["PIPELINED"] == '0')

rrules, ops = gen_rrules()
app = os.path.basename(file_name).split(".json")[0]
output_dir = os.path.dirname(file_name)

c = CoreIRContext(reset=True)
cutil.load_libs(["commonlib", "float_DW"])
CoreIRNodes = gen_CoreIRNodes(16)
cutil.load_from_json(file_name) 
kernels = dict(c.global_namespace.modules)

arch_fc = lassen_fc
ArchNodes = Nodes("Arch")

putil.load_and_link_peak(ArchNodes, lassen_header, {"global.PE": arch_fc})

mr = "memory.fprom2"
ArchNodes.add(
    mr,
    CoreIRNodes.peak_nodes[mr],
    CoreIRNodes.coreir_modules[mr],
    CoreIRNodes.dag_nodes[mr],
)

mapper = Mapper(CoreIRNodes, ArchNodes, lazy=False, ops=ops, rrules=rrules)

c.run_passes(["rungenerators", "deletedeadinstances"])
mods = []

for kname, kmod in kernels.items():
    print(f"Mapping kernel {kname}")
    dag = cutil.coreir_to_dag(CoreIRNodes, kmod, archnodes=ArchNodes)
    Constant2CoreIRConstant(CoreIRNodes).run(dag)

    mapped_dag = mapper.do_mapping(
        dag,
        kname=kname,
        node_cycles=_ArchCycles(),
        match_branch_delay = match_branch_delay,
        convert_unbound=False,
        prove_mapping=True,
        pe_reg_info=pe_reg_info,
        pipelined=pipelined
    )

    mod = cutil.dag_to_coreir(
        ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=False
    )
    mods.append(mod)

print('\n\033[92m' + "All compute kernels passed formal checks" + '\033[0m')
print(f"Total num PEs used: {mapper.num_pes}\n")
print(f"Total num regs inserted: {mapper.num_regs}")

output_file = f"{output_dir}/{app}_mapped.json"
print(f"saving to {output_file}")
c.serialize_definitions(output_file, mods)

with open(f'{output_dir}/{app}_kernel_latencies.json', 'w') as outfile:
    json.dump(mapper.kernel_cycles, outfile, indent=4)


