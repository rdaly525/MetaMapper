from metamapper.common_passes import VerifyNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule
import typing as tp
import coreir



class Mapper:
    def __init__(self, CoreIRNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None):
        self.CoreIRNodes = CoreIRNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(CoreIRNodes, ArchNodes)
        if peak_rules is None:
            #auto discover the rules for CoreIR
            peak_rule = self.table.discover("add", "ALU")
            assert peak_rule is not None
        else:
            #load the rules
            for peak_rule in peak_rules:
                self.table.add_peak_rule(peak_rule)
        self.inst_sel = alg(self.table)

    def do_mapping(self, cmod) -> coreir.Module:
        #Preprocess isolates coreir primitive modules
        #inline inlines them back in
        pb_dags = cutil.preprocess(self.CoreIRNodes, cmod)
        for inst, dag in pb_dags.items():
            #TODO
            #pre_mapped_fc = putil.dag_to_peak(dag, self.CoreIRNodes)
            mapped_dag = self.inst_sel(dag)
            VerifyNodes(self.ArchNodes, mapped_dag)

            #mapped_fc = dag_to_peak(dag, ArchNodes)
            #counter_example = PeakRule(
            #    pre_mapped_fc,
            #    mapped_fc,
            #    ibinding=[((),())],
            #    obinding=[((), ())]
            #).verify()
            #assert counter_example is None

            #Create a new module representing the mapped_dag
            mapped_def = cutil.dag_to_coreir_def(self.ArchNodes, mapped_dag, inst.module)
            inst.module.definition = mapped_def
            coreir.inline_instance(inst)
        #cmod should now contain a mapped coreir module
        return cmod
