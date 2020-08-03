from metamapper.common_passes import VerifyNodes, print_dag, SimplifyCombines, RemoveSelects, prove_equal, Clone
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule
import typing as tp

class Compiler:
    def __init__(self, WasmNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None):
        self.WasmNodes = WasmNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(WasmNodes, ArchNodes)
        ops = (
            "i32.add",
        )
        if peak_rules is None:
            for node_name in ArchNodes._node_names:
                #auto discover the rules for CoreIR
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

    def compile(self, dag) -> tp.Any:
        print("premapped")
        print_dag(dag)
        original_dag = Clone().clone(dag, iname_prefix=f"original_")
        mapped_dag = self.inst_sel(dag)
        print("postmapped")
        print_dag(mapped_dag)
        SimplifyCombines().run(mapped_dag)
        print("simplifyCombines")
        print_dag(mapped_dag)
        RemoveSelects().run(mapped_dag)
        print("RemovedSelects")
        print_dag(mapped_dag)
        unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
        if unmapped is not None:
            raise ValueError(f"Following nodes were unmapped: {unmapped}")
        assert VerifyNodes(self.WasmNodes).verify(original_dag) is None
        #counter_example = prove_equal(original_dag, mapped_dag)
        #if counter_example is not None:
        #    raise ValueError(f"Mapped is not the same {counter_example}")
        return mapped_dag


