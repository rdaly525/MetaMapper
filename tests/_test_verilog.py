from examples.PEs.alu_basic import gen_ALU
from examples.PEs.PE_lut import gen_PE as gen_PE_lut
from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.coreir_mapper import Mapper
import pytest

from peak_gen.sim import wrapped_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Bit
import sys
import peak
from peak.mapper import RewriteRule

import jsonpickle
import shutil

import importlib.util as util

def load_rrs(name, tot: int):
    dir_path = f"darpa/darpa_exps/{name}"
    arch = read_arch(dir_path + "/subgraph_arch_merged.json")
    arch_fc = pe_arch_closure(arch)
    mappable_arch_fc = wrapped_pe_arch_closure(arch)
    print(mappable_arch_fc.Magma)
    for n in range(tot):
        rr_json_file = dir_path + f"/rewrite_rules/subgraph_rr_{n}.json"
        rr_ir_name = f"peak_eq_{n}"
        rr_ir_file = dir_path + f"/peak_eqs/{rr_ir_name}.py"
        with open(rr_json_file) as json_file:
            rewrite_rule_in = jsonpickle.decode(json_file.read())
        input_binding = []

        input_binding_tmp = rewrite_rule_in["ibinding"]

        for i in input_binding_tmp:

            if isinstance(i[0], dict):
                u = i[0]
                v = i[1]
                if u['type'] == "BitVector":
                    u = (BitVector[u['width']](u['value']))
                elif u['type'] == "Bit":
                    u = (Bit(u['value']))

                input_binding.append(tuple([u, tuple(v)]))
            elif i[0] == "unbound":
                if i[1][0] == "fp_vals":
                    continue
                input_binding.append(tuple([peak.mapper.utils.Unbound, tuple(i[1])]))
            else:
                input_binding.append(tuple([tuple(i[0]), tuple(i[1])]))

        pretty_print_binding(input_binding)

        output_binding_tmp = rewrite_rule_in["obinding"]
        output_binding = []

        for o in output_binding_tmp:
            output_binding.append(tuple([tuple(o[0]), tuple(o[1])]))
        pretty_print_binding(output_binding)

        spec = util.spec_from_file_location(rr_ir_name, rr_ir_file)
        foo = util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        ir_fc = foo.mapping_function_fc

        print(ir_fc.Magma)

        rr = RewriteRule(input_binding, output_binding, ir_fc, arch_fc)

def test_load():
    load_rrs("Conv_3_3", 3)


lassen_constraints = {
    ("clk_en",): 1,
    ("config_addr",): 0,
    ("config_data",): 0,
    ("config_en",): 0,
}

@pytest.mark.parametrize("arch", [
    #("PE_lut", gen_PE_lut(16), {}),
    ("Lassen", lassen_fc, lassen_constraints),
    #("ALU", gen_ALU(16), {}),
])
@pytest.mark.parametrize("app", [
    #add_or",
    "conv_3_3",
])
def test_app(arch, app):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{app}.json"
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = cutil.load_from_json(file_name, ["commonlib", "lakelib"])
    pb_dags = cutil.preprocess(CoreIRNodes, cmod)
    name, arch_fc, constraints = arch
    if name == "ALU" and app == "add_or":
        pytest.skip()
    ArchNodes = Nodes("Arch")
    putil.load_from_peak(ArchNodes, arch_fc)
    mapper = Mapper(CoreIRNodes, ArchNodes)
    mod = mapper.do_mapping(pb_dags)
    mapper.do_mapping(pb_dags)
    c.run_passes(["cullgraph"])
    mod.save_to_file(f"tests/build/{name}_no_fp_{app}_mapped.json")
