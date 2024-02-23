from metamapper.common_passes import VerifyNodes, print_dag, count_pes, CustomInline, SimplifyCombines, RemoveSelects, prove_equal, \
    Clone, ExtractNames, Unbound2Const, gen_dag_img, ConstantPacking, GetSinks, PipelinePEs
import metamapper.coreir_util as cutil
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes, Dag
from metamapper.delay_matching import DelayMatching, branch_delay_match, KernelDelay
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule, read_serialized_bindings
import typing as tp
import coreir
import json

class DefaultLatency:

    @staticmethod
    def get(node):
        return 0

class Mapper:
    # Lazy # Discover at mapping time
    # ops (if lazy=False, search for these)
    def __init__(self, CoreIRNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, lazy=True, ops=None, rrules=None, kernel_name_prefix=False):
    
        self.CoreIRNodes = CoreIRNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(CoreIRNodes, ArchNodes)
        self.num_pes = 0
        self.num_regs = 0
        self.kernel_cycles = {}
        self.const_rr = None
        self.bit_const_rr = None        
        self.gen_rules(ops, rrules)
        self.compile_time_rule_gen = lambda dag : None
        
        self.inst_sel = alg(self.table, kernel_name_prefix)

    def gen_rules(self, ops, rrules=None):

        if rrules is None:
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
        else:
            for ind, peak_rule in enumerate(rrules):
                if ops != None:
                    op = ops[ind]
                    print(f"Loading {op} ", end=" ", flush=True)
                    if "fp" in op and "pipelined" in op:
                        op = op.split("_pipelined")[0]
                    self.table.add_peak_rule(peak_rule, op)
                else:
                    self.table.add_peak_rule(peak_rule, None)
            self.table.sort_rules()

    def do_mapping(self, dag, kname="", convert_unbound=True, match_branch_delay=True, prove_mapping=True, node_cycles=None, pe_reg_info=None, pipelined=True) -> coreir.Module:
        self.compile_time_rule_gen(dag)
        use_constant_packing = pe_reg_info != None
        
        if use_constant_packing:
            rule_names = [rule.name for rule in self.table.rules]
            assert "const" in rule_names
            const_rule = self.table.rules.pop(rule_names.index("const"))
           
            rule_names = [rule.name for rule in self.table.rules]

            assert "bit_const" in rule_names
            bit_const_rule = self.table.rules.pop(rule_names.index("bit_const"))
          
        CustomInline(self.CoreIRNodes.custom_inline).run(dag)
        original_dag = Clone().clone(dag, iname_prefix=f"original_")
        pre_packing = self.inst_sel(dag)

        if use_constant_packing:
            ConstantPacking(pe_reg_info).run(pre_packing)
        
            self.table.rules.append(const_rule)
            self.table.rules.append(bit_const_rule)

        mapped_dag = self.inst_sel(pre_packing)

        SimplifyCombines().run(mapped_dag)
        RemoveSelects().run(mapped_dag)

        if pipelined:
            PipelinePEs(pe_reg_info).run(mapped_dag)

        self.num_pes += count_pes(mapped_dag)
        print("\tUsed", count_pes(mapped_dag), "PEs")
        unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
        
        if unmapped is not None:
            raise ValueError(f"Following nodes were unmapped: {unmapped}")

        if node_cycles is not None and match_branch_delay:
            sinks = GetSinks().doit(mapped_dag)
            self.kernel_cycles[kname], added_regs = branch_delay_match(mapped_dag, node_cycles, sinks)
            print("\tAdded", added_regs, "during branch delay matching")
            self.num_regs += added_regs

        if prove_mapping and count_pes(mapped_dag) != 0:
            verify_dag = Clone().clone(mapped_dag, iname_prefix=f"verification_")
            DelayMatching(node_cycles).run(verify_dag)
            counter_example = prove_equal(original_dag, verify_dag, KernelDelay(node_cycles).doit(verify_dag))
            if counter_example is not None:
                raise ValueError(f"Mapped dag is not the same {counter_example}")

        if convert_unbound:
            Unbound2Const().run(mapped_dag)
        return mapped_dag
