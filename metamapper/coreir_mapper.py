from metamapper.common_passes import VerifyNodes, print_dag, SimplifyCombines, RemoveSelects, prove_equal, Clone
import metamapper.coreir_util as cutil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering
from metamapper.delay_matching import DelayMatching
from peak.mapper import RewriteRule as PeakRule
import typing as tp
import coreir

class Mapper:
    def __init__(self, CoreIRNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None, conv=True):
        self.CoreIRNodes = CoreIRNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(CoreIRNodes, ArchNodes)
        conv_ops = (
            "corebit.const",
            "coreir.add",
            "coreir.mul",
            "coreir.const",
        )
        camera_ops = (
            "corebit.const",
            "corebit.or_",
            "corebit.and_",
            "coreir.add",
            "coreir.and_",
            "coreir.ashr",
            "coreir.const",
            "coreir.eq",
            "coreir.lshr",
            "coreir.mul",
            "coreir.mux",
            "coreir.slt",
            "coreir.sub",
            "coreir.ult",
            "commonlib.abs",
            "commonlib.smax",
            "commonlib.smin",
            "commonlib.umax",
            "commonlib.umin",
        )
        if peak_rules is None:
            for node_name in ArchNodes._node_names:
                #auto discover the rules for CoreIR
                if conv:
                    ops = conv_ops
                else:
                    ops = camera_ops
                for op in ops:
                    peak_rule = self.table.discover(op, node_name)
                    print(f"Searching for {op} -> {node_name}")
                    if peak_rule is None:
                        print(f"  Not Found :(")
                        pass
                    else:
                        print(f"  Found!")
        else:
            #load the rules
            for peak_rule in peak_rules:
                self.table.add_peak_rule(peak_rule)
        self.inst_sel = alg(self.table)
        self._history_ = []

    def do_mapping(self, pb_dags, convert_unbound=True, node_latencies=None) -> coreir.Module:
        #Preprocess isolates coreir primitive modules
        #inline inlines them back in
        if len(pb_dags) != 1:
            raise ValueError(f"Bad: {len(pb_dags)}")
        for inst, dag in pb_dags.items():
            #print("premapped")
            #print_dag(dag)
            original_dag = Clone().clone(dag, iname_prefix=f"original_")
            mapped_dag = self.inst_sel(dag)
            #print("postmapped")
            #print_dag(mapped_dag)
            SimplifyCombines().run(mapped_dag)
            #print("simplifyCombines")
            #print_dag(mapped_dag)
            RemoveSelects().run(mapped_dag)
            #print("RemovedSelects")
            #print_dag(mapped_dag)
            unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
            if unmapped is not None:
                raise ValueError(f"Following nodes were unmapped: {unmapped}")
            assert VerifyNodes(self.CoreIRNodes).verify(original_dag) is None
            # Run delay matching if specified (node latencies given).
            if node_latencies is not None:
                RegT = self.CoreIRNodes.dag_nodes["coreir.reg"]
                DelayMatching(RegT, node_latencies).run(mapped_dag)
            self._history_.append(mapped_dag)
            counter_example = prove_equal(original_dag, mapped_dag)
            if counter_example is not None:
                raise ValueError(f"Mapped is not the same {counter_example}")
            #Create a new module representing the mapped_dag
            mapped_mod = cutil.dag_to_coreir_def(self.ArchNodes, mapped_dag, inst.module, inst.module.name + "_mapped")
            #coreir.inline_instance(inst)
            return mapped_mod
        #cmod should now contain a mapped coreir module
