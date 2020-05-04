from .common_passes import CheckIfTree, VerifyNodes, AddID, Printer
import typing as tp
from .node import Nodes, Constant, Input
from .visitor import Dag
from .peak_util import peak_to_dag
from peak.mapper import ArchMapper
from peak.mapper import RewriteRule as PeakRule

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
        #Verify from from rule
        VerifyNodes(self.from_, rr.tile)
        self.rules.append(rr)

    def add_peak_rule(self, rule: PeakRule):
        if not isinstance(rule, PeakRule):
            raise ValueError("rule is not a Peak Rule")

        from_dag = peak_to_dag(self.from_, rule.ir_fc)

        _to_dag = peak_to_dag(self.to, rule.arch_fc)

        #TODO generalize the following code on a Dag Visitor pass in case to_dag is actually a complicated Dag
        #TODO also make the Select node general in that instead of just selecting index, it uses the ADT fields as selects ??
        assert all([isinstance(child, Input) for child in _to_dag.outputs[0].inputs()])
        from_node = from_dag.outputs[0] #HACK
        to_node = _to_dag.outputs[0] #HACK

        to_inputs = [input.copy() for input in from_dag.inputs]
        arch_to_ir = {}
        for ib, ab in rule.ibinding:
            assert isinstance(ab, tuple), "NYI"
            assert len(ab) == 1, "NYI"
            ab_idx = to_node.input_names().index(ab[0])
            if isinstance(ib, tuple):
                assert len(ib)==1, "NYI"
                ib_idx = from_node.input_names().index(ib[0])
                arch_to_ir[ab_idx] = to_inputs[ib_idx]
            else:
                arch_to_ir[ab_idx] = Constant(value=ib)

        #create to_dag
        to_children = []
        for ab_idx, child in enumerate(to_node.children()):
            to_children.append(arch_to_ir[ab_idx])
        to_output = to_node.copy()
        to_output.set_children(*to_children)
        to_dag = Dag([to_output], to_inputs)

    #    tile_inputs = [None for _ in range(from_node.num_inputs())]
    #    rep_inputs = [None for _ in range(to_node.num_inputs())]
    #    rep_dag_inputs = []
    #    for ib, ab in peak_rr.ibinding:
    #        assert isinstance(ab, tuple), "NYI"
    #        assert len(ab) == 1, "NYI"
    #        ab_idx = to_node.input_names().index(ab[0])
    #        if isinstance(ib, tuple):
    #            assert len(ib)==1, "NYI"
    #            ib_idx = from_node.input_names().index(ib[0])
    #            node = Input(idx=ib_idx)
    #            tile_inputs[ib_idx] = node
    #            rep_inputs[ab_idx] = node
    #        else:
    #            rep_inputs[ab_idx] = Constant(value=ib)

    #assert all(node is not None and node.idx == i for (i, node) in enumerate(tile_inputs))
    #assert all(node is not None for (i, node) in enumerate(rep_inputs))

    ##create tile dag:
    #tile_out = from_node(*tile_inputs, iname=0)
    #tile_dag = Dag([tile_out], tile_inputs)
    #rep_out = to_node(*rep_inputs)
    ##the inputs are the same for both dags
    #rep_dag = Dag([rep_out], tile_inputs)


        #, a=from_dag, b=rule.ibinding, c=rule.obinding)

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

