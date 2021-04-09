from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
from metamapper.common_passes import  print_dag

from peak_gen.arch import read_arch
from peak_gen.peak_wrapper import wrapped_peak_class

from peak.mapper import read_serialized_bindings

import delegator
import pytest
import glob
import importlib
import jsonpickle


def gen_rrules(app):

    DSE_PE_location = f"examples/dse_pes/{app}"
    arch = read_arch(f"{DSE_PE_location}/PE.json")
    PE_fc = wrapped_peak_class(arch)

    mapping_funcs = []
    rrules = []

    num_rrules = len(glob.glob(f'{DSE_PE_location}/rewrite_rules/*.json'))

    for ind in range(num_rrules):

        with open(f"{DSE_PE_location}/peak_eqs/peak_eq_" + str(ind) + ".py", "r") as file:
            with open(f"{DSE_PE_location}/peak_eqs_mod/peak_eq_" + str(ind) + ".py", "w") as outfile:
                for line in file:
                    outfile.write(line.replace('mapping_function', 'mapping_function_'+str(ind)))

        peak_eq = importlib.import_module(f"examples.dse_pes.{app}.peak_eqs_mod.peak_eq_{ind}")

        ir_fc = getattr(peak_eq, "mapping_function_" + str(ind) + "_fc")
        mapping_funcs.append(ir_fc)

        with open(f"{DSE_PE_location}/rewrite_rules/rewrite_rule_" + str(ind) + ".json", "r") as json_file:
            rewrite_rule_in = jsonpickle.decode(json_file.read())

        rewrite_rule = read_serialized_bindings(rewrite_rule_in, ir_fc, PE_fc)

        counter_example = rewrite_rule.verify()


        rrules.append(rewrite_rule)
    return PE_fc, rrules

# @pytest.mark.parametrize("app", ["harris_compute", "camera_pipeline_compute", "gaussian_compute", "laplacian_pyramid_compute", "cascade_compute",
                                # "resnet_block_compute", "resnet_compute", "stereo_compute"])
# @pytest.mark.parametrize("app", ["gaussian_compute", "camera_pipeline_compute"])
@pytest.mark.skip
@pytest.mark.parametrize("app", ["gaussian_compute"])
def test_app(app):
    verilog = False
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    file_name = f"examples/clockwork/{app}.json"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cutil.load_from_json(file_name, libraries=["cgralib"]) #libraries=["lakelib"])
    kernels = dict(c.global_namespace.modules)

    arch_fc, rrules = gen_rrules(app)

    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mr = "memory.rom2"
    ArchNodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rrules=rrules)

    c.run_passes(["rungenerators", "deletedeadinstances"])


    for kname, kmod in kernels.items():
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
        mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mapped", convert_unbounds=verilog)

    #  Without these lines the last kernel will not be created in the output coreir file
    dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
    mapped_dag = mapper.do_mapping(dag, convert_unbound=False, prove_mapping=False)
    mod = cutil.dag_to_coreir(ArchNodes, mapped_dag, f"{kname}_mappedd", convert_unbounds=verilog)

    print(f"Num PEs used: {mapper.num_pes}")
    output_file = f"build/{app}_mapped.json"
    print(f"saving to {output_file}")
    c.save_to_file(output_file)

    if verilog:
        c.run_passes(["wireclocks-clk"])
        c.run_passes(["wireclocks-arst"])
        c.run_passes(["markdirty"])


        #Test syntax of serialized json
        res = delegator.run(f"coreir -i {output_file} -l commonlib")
        assert not res.return_code, res.out + res.err

        #Test serializing to verilog
        res = delegator.run(f'coreir -i {output_file} -l commonlib -p "wireclocks-clk; wireclocks-arst" -o build/{app}_mapped.v --inline')
        assert not res.return_code, res.out + res.err
