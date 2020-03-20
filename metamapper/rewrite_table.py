from .common_passes import CheckIfTree
import typing as tp
from .node import Nodes, Constant, Input
from .visitor import Dag
from peak.mapper import ArchMapper, pretty_print_binding

class RewriteRule:
    def __init__(self,
        tile: Dag,
        replace: tp.Callable,
        cost: tp.Callable,
        checker: tp.Callable = None
    ):

        pattern_is_tree = CheckIfTree(tile).is_tree
        if not pattern_is_tree:
            raise NotImplementedError("tile needs to be a tree")

        self.tile = tile
        self.replace = replace
        self.cost = cost
        self.checker = cost


def create_1to1_rewrite_from_solution(from_node, to_node, solution):
    tile_inputs = [None for _ in range(from_node.num_inputs())]
    rep_inputs = [None for _ in range(to_node.num_inputs())]
    rep_dag_inputs = []
    for ib, ab in solution.ibinding:
        assert isinstance(ab, tuple), "NYI"
        assert len(ab) == 1, "NYI"
        ab_idx = to_node.input_names().index(ab[0])
        if isinstance(ib, tuple):
            assert len(ib)==1, "NYI"
            ib_idx = from_node.input_names().index(ib[0])
            node = Input(idx=ib_idx)
            tile_inputs[ib_idx] = node
            rep_inputs[ab_idx] = node
        else:
            rep_inputs[ab_idx] = Constant(value=ib)

    assert all(node is not None and node.idx == i for (i, node) in enumerate(tile_inputs))
    assert all(node is not None for (i, node) in enumerate(rep_inputs))

    #create tile dag:
    tile_out = from_node(*tile_inputs, iname=0)
    tile_dag = Dag([tile_out], tile_inputs)
    rep_out = to_node(*rep_inputs)
    #the inputs are the same for both dags
    rep_dag = Dag([rep_out], tile_inputs)

    rr = RewriteRule(
        tile = tile_dag,
        replace = lambda _: rep_dag,
        cost = lambda _: 1,
        checker = lambda match: True
    )
    return rr


#This will verify that each ir and arch are only of the apporpriate type
class RewriteTable:
    def __init__(self, from_: Nodes, to: Nodes):
        self.from_ = from_
        self.to = to
        self.rules = []

    def add_rewrite(self, rr: RewriteRule):
        #TODO see if each node in pattern is of appropriate type
        self.rules.append(rr)

    def discover_1to1_rewrite(self, from_name, to_name):

        from_fc = self.from_.peak_nodes[from_name]
        to_fc = self.to.peak_nodes[to_name]
        #Create a rewrite rule for Add
        arch_mapper = ArchMapper(to_fc)
        ir_mapper = arch_mapper.process_ir_instruction(from_fc)
        solution = ir_mapper.solve('z3')
        if not solution.solved:
            return None

        from_dnode = self.from_.dag_nodes[from_name]
        to_dnode = self.to.dag_nodes[to_name]
        rr = create_1to1_rewrite_from_solution(from_dnode, to_dnode, solution)
        self.add_rewrite(rr)
        return rr

