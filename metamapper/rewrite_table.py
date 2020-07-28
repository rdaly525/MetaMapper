from collections import OrderedDict

from .common_passes import CheckIfTree, VerifyNodes, print_dag
import typing as tp
from .node import Nodes, DagNode, Dag, Constant, Input, Output, Combine
from .peak_util import peak_to_dag
from peak.mapper import ArchMapper, Unbound
from peak.mapper import RewriteRule as PeakRule
from peak import family, family_closure

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
            print_dag(tile)
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
        from_node_name = self.from_.name_from_peak(rule.ir_fc)

        # Create to_dag by Wrapping _to_dag within ibinding and obinding
        # Get input/output names from peak_cls

        to_fc = rule.arch_fc
        to_node_name = self.to.name_from_peak(to_fc)
        to_node_t = self.to.dag_nodes[to_node_name]
        assert issubclass(to_node_t, DagNode)
        to_bv = to_fc(family.PyFamily())
        to_input = Input(iname="self")

        def sel_from(path, node: DagNode):
            assert isinstance(path, tuple)
            if len(path) == 0:
                return node
            return sel_from(path[1:], node.select(path[0]))

        #input -> ibinding node
        ibind_children = []
        ibind_paths = []

        for from_b, to_b in rule.ibinding:
            assert isinstance(to_b, tuple)
            if isinstance(from_b, tuple):
                child = sel_from(from_b, to_input)
            else:
                child = Constant(value=from_b)
            ibind_paths.append(to_b)
            ibind_children.append(child)

        ibind = Combine(*ibind_children, paths=ibind_paths, type=to_bv.input_t, iname="ibind")

        #ibinding node -> to_node
        to_children = [ibind.select(field) for field in to_bv.input_t.field_dict]
        to_node = to_node_t(*to_children)

        #to_node -> obinding_node
        obind_children = []
        obind_paths = []
        for from_b, to_b in rule.obinding:
            if from_b is Unbound:
                continue
            assert isinstance(from_b, tuple)
            obind_paths.append(from_b)
            if isinstance(to_b, tuple):
                child = sel_from(to_b, to_node)
            else:
                raise NotImplementedError()
            obind_children.append(child)
        obind = Combine(*obind_children, paths=obind_paths, type=from_bv.output_t, iname="obind")

        #obinidng_node -> output
        output_children = [obind.select(field) for field in from_bv.output_t.field_dict]
        to_output = Output(*output_children, iname="self")
        to_dag = Dag([to_input], [to_output])

        #Verify that the io matches
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
    def discover(self, from_name, to_name, path_constraints={}) -> tp.Union[None, RewriteRule]:
        if isinstance(from_name, str):
            from_fc = self.from_.peak_nodes[from_name]
        else:
            from_fc = from_name
            assert isinstance(from_name, family_closure)
        to_fc = self.to.peak_nodes[to_name]
        arch_mapper = ArchMapper(to_fc, path_constraints=path_constraints)
        ir_mapper = arch_mapper.process_ir_instruction(from_fc)
        peak_rr = ir_mapper.solve('z3', external_loop=True)
        if peak_rr is None:
            return None
        rr = self.add_peak_rule(peak_rr)
        return rr

