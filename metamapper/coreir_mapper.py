from metamapper.common_passes import VerifyNodes, print_dag, count_pes, SimplifyCombines, RemoveSelects, prove_equal, \
    Clone, ExtractNames, Unbound2Const
import metamapper.coreir_util as cutil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes, Dag
from metamapper.delay_matching import DelayMatching
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule, read_serialized_bindings
import typing as tp
import coreir
import json


class Mapper:
    # Lazy # Discover at mapping time
    # ops (if lazy=False, search for these)
    # rule_file #pointer to serialized rule file
    def __init__(self, CoreIRNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, lazy=True, ops=[], rule_file=None, rrules=None):

        self.CoreIRNodes = CoreIRNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(CoreIRNodes, ArchNodes)
        self.num_pes = 0
        self._history_ = []

        if not lazy and rule_file is None and len(ops) == 0:
            raise ValueError("If not lazy, need ops specified!")
        if lazy and len(ops) > 0:
            raise ValueError("if lazy, needs no ops specified!")

        if not lazy:
            self.gen_rules(ops, rule_file, rrules)
            self.compile_time_rule_gen = lambda dag : None
        else:
            def lazy_rule_gen(dag: Dag):
                op_dict = ExtractNames(self.CoreIRNodes).extract(dag)
                ops = list(op_dict.keys())
                self.gen_rules(ops, rule_file, rrules)
            self.compile_time_rule_gen = lazy_rule_gen

        self.inst_sel = alg(self.table)

    def gen_rules(self, ops, rule_file=None, rrules=None):
        if rule_file is None and rrules is None:
            for node_name in self.ArchNodes._node_names:
                # auto discover the rules for CoreIR
                for op in ops:
                    peak_rule = self.table.discover(op, node_name)
                    print(f"Searching for {op} -> {node_name}")
                    if peak_rule is None:
                        print(f"  Not Found :(")
                        pass
                    else:
                        print(f"  Found!")
        elif rrules is None:
            
            for arch_name in self.ArchNodes._node_names:
                if arch_name != "PE":
                    continue
                arch_fc = self.ArchNodes.peak_nodes[arch_name]
                with open(rule_file, "r") as read_file:
                    rrs = json.loads(read_file.read())
                    for op, rr in rrs.items():
                        ir_fc = self.CoreIRNodes.peak_nodes[op]
                        new_rewrite_rule = read_serialized_bindings(rr, ir_fc, arch_fc)
                        counter_example = new_rewrite_rule.verify()

                        if counter_example is not None:
                            print(counter_example)
                            raise ValueError(f"RR for {op} fails with ^ Counter Example")
                        self.table.add_peak_rule(new_rewrite_rule)
        else:
            for ind, peak_rule in enumerate(rrules):
                self.table.add_peak_rule(peak_rule, name="test_name_" + str(ind))

    def do_mapping(self, dag, convert_unbound=True, prove_mapping=True, node_latencies=None) -> coreir.Module:
        #Preprocess isolates coreir primitive modules
        #inline inlines them back in
        #print("premapped")
        #print_dag(dag)
        self.compile_time_rule_gen(dag)
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
        self.num_pes += count_pes(mapped_dag)
        unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
        if unmapped is not None:
            raise ValueError(f"Following nodes were unmapped: {unmapped}")
        assert VerifyNodes(self.CoreIRNodes).verify(original_dag) is None
        
        if node_latencies is not None:
            RegT = self.CoreIRNodes.dag_nodes["coreir.pipeline_reg"]
            DelayMatching(RegT, node_latencies).run(mapped_dag)
        self._history_.append(mapped_dag)

        if prove_mapping:
            counter_example = prove_equal(original_dag, mapped_dag)
            if counter_example is not None:
                raise ValueError(f"Mapped is not the same {counter_example}")
        #Create a new module representing the mapped_dag

        if convert_unbound:
            Unbound2Const().run(mapped_dag)
        return mapped_dag
