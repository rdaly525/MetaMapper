from .common_passes import CheckIfTree, VerifyNodes, Printer
import typing as tp
from .node import Nodes, DagNode, Dag, Constant, Input, Output
from .peak_util import peak_to_dag
from peak.mapper import ArchMapper
from peak.mapper import RewriteRule as PeakRule
from peak import family

#debug
from peak.mapper.utils import pretty_print_binding

#TODO possibly make from peak_rule directly 
class RewriteRule:
    def __init__(self,
        tile: Dag,
        replace: tp.Callable,
        cost: tp.Callable,
        checker: tp.Callable = None
    ):

        pattern_is_tree = CheckIfTree().is_tree(tile)
        if not pattern_is_tree:
            print(Printer().run(tile).res)
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
        #Verify from from rule
        VerifyNodes(self.from_).run(rr.tile)
        self.rules.append(rr)

    def add_peak_rule(self, rule: PeakRule):
        if not isinstance(rule, PeakRule):
            raise ValueError("rule is not a Peak Rule")

        from_dag = peak_to_dag(self.from_, rule.ir_fc)
        from_bv = rule.ir_fc(family.PyFamily())
        # Create to_dag by Wrapping _to_dag within ibinding and obinding
        # Get input/output names from peak_cls

        to_fc = rule.arch_fc
        to_node_name = self.to.name_from_peak(to_fc)
        to_node_t = self.to.dag_nodes[to_node_name]
        assert issubclass(to_node_t, DagNode)
        to_bv = to_fc(family.PyFamily())
        to_input = Input(iname="self")
        to_children = [None for _ in to_bv.input_t.field_dict]
        for from_b, to_b in rule.ibinding:
            assert isinstance(to_b, tuple), "NYI"
            assert len(to_b) == 1, "NYI"
            to_sel = to_b[0]
            to_idx = list(to_bv.input_t.field_dict.keys()).index(to_sel)
            if isinstance(from_b, tuple):
                assert len(from_b)==1, "NYI"
                from_sel = from_b[0]
                child = to_input.select(from_sel)
            else:
                child = Constant(value=from_b)
                print("child_iname", child.iname)

            to_children[to_idx] = child
        assert all(node is not None for node in to_children)
        to_node = to_node_t(*to_children)

        to_output_children = [None for _ in to_bv.output_t.field_dict]
        for from_b, to_b in rule.obinding:
            assert isinstance(to_b, tuple), "NYI"
            assert len(to_b) == 1, "NYI"
            to_sel = to_b[0]
            assert isinstance(from_b, tuple)
            assert len(from_b)==1, "NYI"
            from_sel = from_b[0]
            from_idx = list(from_bv.output_t.field_dict.keys()).index(from_sel)
            child = to_node.select(to_sel)
            to_output_children[from_idx] = child
        assert all(node is not None for node in to_output_children)
        to_output = Output(*to_output_children, iname="self")
        to_dag = Dag([to_input], [to_output])

        #Verify that the io matches
        assert from_dag.sources[0]._selects == to_dag.sources[0]._selects
        #TODO verify outputs match
        rr = RewriteRule(
            tile = from_dag,
            replace = lambda _: to_dag,
            cost = lambda _: 1,
            checker = lambda match: True
        )
        self.add_rule(rr)
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
        rr = self.add_peak_rule(peak_rr)
        return rr

