from functools import lru_cache

from hwtypes.modifiers import strip_modifiers
from .common_passes import CheckIfTree, VerifyNodes, print_dag, BindsToCombines, SimplifyCombines, RemoveSelects, gen_dag_img, Constant2CoreIRConstant, DagNumNodes
import typing as tp
from .node import Nodes, DagNode, Dag, Constant, Input, Output, Bind
from .peak_util import peak_to_dag
from peak.mapper import ArchMapper, Unbound
from peak.mapper import RewriteRule as PeakRule
from peak import family_closure
from .family import fam

#debug
from peak.mapper.utils import pretty_print_binding

#Rewrite Rule for i32.const


#TODO possibly make from peak_rule directly 
class RewriteRule:
    def __init__(self,
        tile: Dag,
        replace: tp.Callable,
        cost: tp.Callable,
        checker: tp.Callable = None,
        name = None
    ):

        # pattern_is_tree = CheckIfTree().is_tree(tile)
        # if not pattern_is_tree:
        #     print_dag(tile)
        #     raise NotImplementedError("Tile not a tree")

        self.tile = tile
        self.replace = replace
        self.cost = cost
        self.checker = cost
        if name is None:
            name = "Unnamed"
        self.name = name


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
        Constant2CoreIRConstant(self.from_).run(rr.tile)
        self.rules.append(rr)

    def add_peak_rule(self, rule: PeakRule, name=None):
        if not isinstance(rule, PeakRule):
            raise ValueError("rule is not a Peak Rule")

        
        from_dag = peak_to_dag(self.from_, rule.ir_fc, name=name)
        from_bv = rule.ir_fc(fam().PyFamily())
        from_node_name = self.from_.name_from_peak(rule.ir_fc)
        # Create to_dag by Wrapping _to_dag within ibinding and obinding
        # Get input/output names from peak_cls

        to_fc = rule.arch_fc
        to_node_name = self.to.name_from_peak(to_fc, name)

        to_node_t = self.to.dag_nodes[to_node_name]
        assert issubclass(to_node_t, DagNode)
        to_bv = to_fc(fam().PyFamily())
        to_input = Input(iname="self", type=strip_modifiers(from_bv.input_t))

        def sel_from(path, node: DagNode):
            assert isinstance(path, tuple)
            if len(path) == 0:
                return node
            return sel_from(path[1:], node.select(path[0]))

        #input -> ibinding node
        ibind_children = []
        ibind_paths = []
        port_names = ["inst"]
        #pretty_print_binding(rule.ibinding)
        #pretty_print_binding(rule.obinding)
        for from_b, to_b in rule.ibinding:
            assert isinstance(to_b, tuple)
            if isinstance(from_b, tuple):
                child = sel_from(from_b, to_input)
            else:
                path, T = to_b, strip_modifiers(to_bv.input_t)
                while len(path) > 0:
                    T = T.field_dict[path[0]]
                    path = path[1:]
                child = Constant(value=from_b, type=T)
            if to_b[0] != "inst":
                port_names.append(to_b)
            ibind_paths.append(to_b)
            ibind_children.append(child)

        ibind = Bind(*ibind_children, paths=ibind_paths, type=strip_modifiers(to_bv.input_t), iname="ibind")

        #ibinding node -> to_node
        to_children = [ibind.select(field) for field in to_bv.input_t.field_dict]
        to_node = to_node_t(*to_children)
        to_node.add_metadata(port_names)

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
        obind = Bind(*obind_children, paths=obind_paths, type=from_bv.output_t, iname="obind")

        #obinidng_node -> output
        output_children = [obind.select(field) for field in from_bv.output_t.field_dict]
        to_output = Output(*output_children, iname="self", type=from_bv.output_t)
        to_dag = Dag([to_input], [to_output])


        # print("Before combine")
        # print_dag(to_dag)
        BindsToCombines().run(to_dag)
        # print("After combine")
        # print_dag(to_dag)
        SimplifyCombines().run(to_dag)
        # print("After Simplify")
        # print_dag(to_dag)
        RemoveSelects().run(to_dag)
        #print("After rmSelects")
        #print_dag(to_dag)
        # print("to_dag")


        #Verify that the io matches
        #TODO verify outputs match
        rr = RewriteRule(
            tile = from_dag,
            replace = lambda _: to_dag,
            cost = lambda _: 1,
            checker = lambda match: True,
            name = name
        )
        rr._rule = rule
        self.add_rule(rr)
        return rr

    #Discovers and returns a rule if possible
    def discover(self, from_name, to_name, path_constraints={}, rr_name=None, solver="z3") -> tp.Union[None, RewriteRule]:
        if rr_name is None:
            rr_name = from_name
        if isinstance(from_name, str):
            from_fc = self.from_.peak_nodes[from_name]
        else:
            from_fc = from_name
            assert isinstance(from_name, family_closure)
        to_fc = self.to.peak_nodes[to_name]
        arch_mapper = ArchMapper(to_fc, path_constraints=path_constraints, family=fam())
        ir_mapper = arch_mapper.process_ir_instruction(from_fc)
        peak_rr = ir_mapper.solve(solver, external_loop=True)
        print("rr", peak_rr)
        if peak_rr is None:
            return None
        print(peak_rr, rr_name)
        rr = self.add_peak_rule(peak_rr, name=rr_name)
        return rr


    def sort_rules(self):
        self.rules.sort(key=lambda x: x.name)
        rule_nodes = []
        for rule in self.rules:
            dag = rule.tile
            num_nodes = DagNumNodes().doit(dag)
            rule_nodes.append(num_nodes)

        keydict = dict(zip(self.rules, rule_nodes))
        self.rules.sort(key=keydict.get, reverse=True)

        mul_add_rules = []
        for idx,rule in enumerate(self.rules):
            if "mac" in rule.name or "muladd" in rule.name:
                mul_add_rules.append(idx)

        for idx in mul_add_rules:
            self.rules.insert(0, self.rules.pop(idx))

