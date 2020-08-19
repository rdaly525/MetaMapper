from metamapper.common_passes import VerifyNodes, print_dag, SimplifyCombines, RemoveSelects, prove_equal, Clone, count_pes, UnboundTo0
import metamapper.coreir_util as cutil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes, Dag
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule
import typing as tp
import coreir

class Mapper:
    def __init__(self, CoreIRNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None, conv=True):
        self.CoreIRNodes = CoreIRNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(CoreIRNodes, ArchNodes)
        self.num_pes = 0
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

        camera_harris_conv_ops = (
"commonlib.umax",
"commonlib.umin",
"commonlib.smin",
"commonlib.smax",
"commonlib.abs",
"coreir.const",
"corebit.and_",
"coreir.add",
"coreir.sub",
"coreir.mux",
"coreir.ashr",
"coreir.and_",
"coreir.eq",
"coreir.mul",
"coreir.sle",
"corebit.const",
"coreir.ult",
"coreir.lshr",
"coreir.slt",
"coreir.sge",
"coreir.ule",
"coreir.uge",

        )
        if peak_rules is None:
            for node_name in ArchNodes._node_names:
                #auto discover the rules for CoreIR
                peak_rule = self.table.discover(CoreIRNodes._peakir_.instructions["other.const_mul0"], node_name, rr_name="const_mul0")
                peak_rule = self.table.discover(CoreIRNodes._peakir_.instructions["other.const_mul1"], node_name, rr_name="const_mul1")
                if conv:
                    ops = conv_ops
                else:
                    ops = camera_harris_conv_ops
                for op in ops:
                    peak_rule = self.table.discover(op, node_name, rr_name=op)
                    print(f"Searching for {op} -> {node_name}")
                    if peak_rule is None:
                        print(f"  Not Found :(")
                        pass
                    else:
                        print(f"  Found!")

        else:
            #load the rules
            for ind, peak_rule in enumerate(peak_rules):
                print(str(ind))
                self.table.add_peak_rule(peak_rule, name="test_name_" + str(ind))
        self.inst_sel = alg(self.table)


    def map_dag(self, dag: Dag, prove=True) -> Dag:
        original_dag = Clone().clone(dag, iname_prefix=f"original_")
        #print_dag(original_dag)
        mapped_dag = self.inst_sel(dag)

        UnboundTo0().run(mapped_dag)
        # print("postmapped")
        # print_dag(mapped_dag)
        SimplifyCombines().run(mapped_dag)
        # print("simplifyCombines")
        # print_dag(mapped_dag)
        RemoveSelects().run(mapped_dag)
        # print("RemovedSelects")
        #print_dag(mapped_dag)
        unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
        if unmapped is not None:
            unmapped = set(filter(lambda v: not isinstance(v, self.CoreIRNodes.dag_nodes["memory.rom2"]), unmapped))
            if len(unmapped) > 0:
                raise ValueError(f"Following nodes were unmapped: {unmapped}")
        assert VerifyNodes(self.CoreIRNodes).verify(original_dag) is None
        if prove:
            counter_example = prove_equal(original_dag, mapped_dag)
            if counter_example is not None:
                raise ValueError(f"Mapped is not the same {counter_example}")
        
        return mapped_dag

    def map_module(self, cmod: coreir.Module, prove=True) -> coreir.Module:
        premapped_dag = cutil.preprocess(self.CoreIRNodes, cmod)
        mapped_dag = self.map_dag(premapped_dag, prove=prove)
        self.num_pes += count_pes(mapped_dag)
        #Create a new module representing the mapped_dag
        mapped_mod = cutil.dag_to_coreir_def(self.ArchNodes, mapped_dag, cmod, cmod.name + "_mapped")
        return mapped_mod
