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
#                                 "resnet_block_compute", "resnet_compute", "stereo_compute"])
# @pytest.mark.parametrize("app", ["gaussian_compute", "camera_pipeline_compute"])
@pytest.mark.parametrize("app", ["camera_pipeline_compute"])
def test_app(app):
    print("STARTING TEST")
    c = CoreIRContext(reset=True)
    file_name = f"examples/clockwork/{app}.json"
    cutil.load_libs(["commonlib"])
    CoreIRNodes = gen_CoreIRNodes(16)
    cutil.load_from_json(file_name) #libraries=["lakelib"])
    kernels = dict(c.global_namespace.modules)

    arch_fc, rrules = gen_rrules(app)

    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    
    mapper = Mapper(CoreIRNodes, ArchNodes, lazy=True, rrules=rrules)

    for kname, kmod in kernels.items():
    # kname = "hcompute_blur_unnormalized_stencil"
    # kmod = kernels[kname]
        print(kname)
        dag = cutil.coreir_to_dag(CoreIRNodes, kmod)
        print_dag(dag)
        mapped_dag = mapper.do_mapping(dag, prove_mapping=False)    


    print(f"Num PEs used: {mapper.num_pes}")
    return
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

#test_app(("PE_lut", gen_PE_lut(16), {}),"add2")
