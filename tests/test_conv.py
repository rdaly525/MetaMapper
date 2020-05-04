from metamapper.irs.coreir import gen_CoreIRNodes
from examples.alu import gen_ALU, Inst, OP

import metamapper.coreir_util as cutil

import metamapper.peak_util as putil

from metamapper.rewrite_table import RewriteTable

from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering

import coreir

from peak.mapper import RewriteRule as PeakRule

import typing as tp

#This is going to write out the full flow

#This is from coreir -> ArchNodes
def create_instruction_selector(IRNodes, ArchNodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None):
    table = RewriteTable(IRNodes, ArchNodes)
    if peak_rules is None:
        #auto discover the rules for CoreIR
        peak_rule = table.discover("add", "ALU")
        table.add_peak_rule(peak_rule)
    else:
        #load the rules
        for peak_rule in peak_rules:
            table.add_peak_rule(peak_rule)

    inst_sel = alg(table)
    return inst_sel

def do_mapping(cmod, instruction_selector):
    pb_dags = preprocess(cmod)
    print(pb_dags)
    raise NotImplementedError("Half way there ross!")
    for inst, dag in pb_dags.items():
        pre_mapped_fc = dag_to_peak(dag, CoreIRNodes)
        mapped_dag = instruction_selector(dag)
        verify_mapped(mapped_dag, ArchNodes)
        mapped_fc = dag_to_peak(dag, ArchNodes)

        counter_example = PeakRule(
            pre_mapped_fc,
            mapped_fc,
            ibinding=[((),())],
            obinding=[((), ())]
        ).verify()
        assert counter_example is None

        #Create a new module representing the mapped_dag
        mapped_module = dag_to_coreir(mapped_dag)

        #TODO this might have an issue that the inst.type is not idenetical (but is isomorphic to mapped module)
        replace_instance(inst, mapped_module)
        inline(inst)
    #cmod should now contain a mapped coreir module
    return cmod

def test_conv():
    ArchNodes = Nodes("Arch")
    arch_fc = gen_ALU(16)
    putil.peak_to_node(ArchNodes, arch_fc)
    CoreIRNodes = gen_CoreIRNodes(16)

    instruction_selector = create_instruction_selector(CoreIRNodes, ArchNodes)

    c = coreir.Context()
    cmod = cutil.load_from_json(c, "examples/conv_3_3.json")
    mapped_mod = do_mapping(cmod, instruction_selector)










