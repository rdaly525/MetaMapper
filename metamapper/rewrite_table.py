from .common_passes import CheckIfTree
import typing as tp
from .node import Nodes, Constant, Input
from .visitor import Dag
from peak.mapper import ArchMapper
from peak.mapper import RewriteRule as PeakRule

#debug
from peak.mapper.utils import pretty_print_binding

class RewriteRule:
    def __init__(self,
        tile: Dag,
        replace: tp.Callable,
        cost: tp.Callable,
        checker: tp.Callable = None
    ):

        pattern_is_tree = CheckIfTree(tile).is_tree
        if not pattern_is_tree:
            raise NotImplementedError("Tile not a tree")

        self.tile = tile
        self.replace = replace
        self.cost = cost
        self.checker = cost

#This will verify that each ir and arch are only of the apporpriate type
class RewriteTable:
    def __init__(self, from_: Nodes, to: Nodes):
        self.from_ = from_
        self.to = to
        self.rules = []

    def add_rule(self, rr: RewriteRule):
        if not isinstance(rr, RewriteRule):
            raise ValueError("rule is not a Rewrite Rule")
        raise NotImplementedError("see if each node in pattern is of appropriate type")
        self.rules.append(rr)

    def add_peak_rule(self, rule: PeakRule):
        if not isinstance(rule, PeakRule):
            raise ValueError("rule is not a Peak Rule")

        from_dag = peak_to_dag(self.from_, rule.ir_fc)

        #Idea! what if I wrap the arch_fc into another layer of hierarchy so that the interface is identical to the ir_fc
        # I should absolutely do this.
        #The input dag and the output dag should look identical.
        to_dag = peak_to_dag(self.to, rule.arch_fc, a=from_dag, b=rule.ibinding, c=rule.obinding)

        rr = RewriteRule(
            tile = from_dag,
            replace = lambda _: to_dag,
            cost = lambda _: 1,
            checker = lambda match: True
        )

        return rr

    #Discovers and returns a rule if possible
    def discover(self, from_name, to_name):

        from_fc = self.from_.peak_nodes[from_name]
        to_fc = self.to.peak_nodes[to_name]
        #Create a rewrite rule for Add
        arch_mapper = ArchMapper(to_fc)
        ir_mapper = arch_mapper.process_ir_instruction(from_fc)
        peak_rr = ir_mapper.solve('z3')
        if peak_rr is None:
            return None
        self.add_peak_rule(peak_rr)
        return rr

