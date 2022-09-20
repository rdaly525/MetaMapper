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

from peak_gen.arch import read_arch
from peak_gen.peak_wrapper import wrapped_peak_class


class _ArchCycles:
    def get(self, node):
        kind = node.kind()[0]
        if kind == "Rom" or kind == "FPRom":
            return 1
        elif kind == "global.PE":
            return pe_cycles
        return 0


pe_location = os.path.join(
    Path(__file__).parent.parent.parent.resolve(), "DSEGraphAnalysis/outputs"
)
pe_header = os.path.join(Path(__file__).parent.parent.resolve(), "libs/pe_header.json")
metamapper_location = os.path.join(
    Path(__file__).parent.parent.resolve(), "examples/peak_gen"
)


def gen_rrules():

    arch = read_arch(f"{pe_location}/PE.json")
    PE_fc = wrapped_peak_class(arch, debug=True)
    c = CoreIRContext()
    cmod = putil.peak_to_coreir(PE_fc)
    c.serialize_header(pe_header, [cmod])
    mapping_funcs = []
    rrules = []

    num_rrules = len(glob.glob(f"{pe_location}/rewrite_rules/*.json"))

    if not os.path.exists(f"{metamapper_location}"):
        os.makedirs(f"{metamapper_location}")

    for ind in range(num_rrules):

        with open(f"{pe_location}/peak_eqs/peak_eq_" + str(ind) + ".py", "r") as file:
            with open(
                f"{metamapper_location}/peak_eq_" + str(ind) + ".py", "w"
            ) as outfile:
                for line in file:
                    outfile.write(
                        line.replace("mapping_function", "mapping_function_" + str(ind))
                    )
        peak_eq = importlib.import_module("examples.peak_gen.peak_eq_" + str(ind))

        ir_fc = getattr(peak_eq, "mapping_function_" + str(ind) + "_fc")
        mapping_funcs.append(ir_fc)

        with open(
            f"{pe_location}/rewrite_rules/rewrite_rule_" + str(ind) + ".json", "r"
        ) as json_file:
            rewrite_rule_in = json.load(json_file)

        rewrite_rule = read_serialized_bindings(rewrite_rule_in, ir_fc, PE_fc)
        counter_example = rewrite_rule.verify()

        rrules.append(rewrite_rule)
    return PE_fc, rrules


file_name = str(sys.argv[1])
if "PIPELINED" in os.environ and os.environ["PIPELINED"].isnumeric():
    pe_cycles = int(os.environ["PIPELINED"])
else:
    pe_cycles = 1

arch_fc, rrules = gen_rrules()
verilog = False

app = os.path.basename(file_name).split(".json")[0]
output_dir = os.path.dirname(file_name)

c = CoreIRContext(reset=True)
cutil.load_libs(["commonlib", "float_DW"])
CoreIRNodes = gen_CoreIRNodes(16)
cutil.load_from_json(file_name)  # libraries=["lakelib"])
kernels = dict(c.global_namespace.modules)

ArchNodes = Nodes("Arch")
putil.load_and_link_peak(ArchNodes, pe_header, {"global.PE": arch_fc})

mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rrules=rrules)

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
        convert_unbound=False,
        prove_mapping=False,
    )
    mod = cutil.dag_to_coreir(
        ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog
    )
    mods.append(mod)

print(f"Num PEs used: {mapper.num_pes}")
output_file = f"{output_dir}/{app}_mapped.json"
print(f"saving to {output_file}")
c.serialize_definitions(output_file, mods)


with open(f"{output_dir}/{app}_kernel_latencies.json", "w") as outfile:
    json.dump(mapper.kernel_cycles, outfile)
