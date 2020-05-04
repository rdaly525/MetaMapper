from ..visitor import Dag, Visitor, Transformer
from ..rewrite_table import RewriteTable
from ..node import Input

class Clone(Visitor):
    def __init__(self, dag):
        assert dag is not None
        self.node_map = {}
        super().__init__(dag)
        dag_copy = Dag(
            inputs=[self.node_map[node] for node in dag.inputs],
            outputs=[self.node_map[node] for node in dag.outputs]
        )
        self.dag_copy = dag_copy

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        new_node = node.copy()
        children = (self.node_map[child] for child in node.children())
        new_node.set_children(*children)
        self.node_map[node] = new_node

#It will match a tree pattern to a tree (program)
def match_node(p_node, a_node):
    if isinstance(p_node, Input):
        return ((p_node.idx, a_node),)

    #Verify p_node is a_node
    if type(p_node) != type(a_node):
        return None

    matched = ()
    for p_child, a_child in zip(p_node.children(), a_node.children()):
        child_matched = match_node(p_child, a_child)
        if child_matched is None:
            return None
        matched = (*matched, *child_matched)
    return matched

class ReplaceInputs(Transformer):
    def __init__(self, dag, input_replacements):
        assert len(dag.inputs) == len(input_replacements)
        self.ireps = input_replacements
        super().__init__(dag)

    def visit_Input(self, node):
        return self.ireps[node.idx]

#Given a Dag, greedly apply each rewrite rule
class GreedyReplace(Transformer):
    def __init__(self, rr, dag):
        self.rr = rr
        self.root = rr.tile.outputs[0]
        super().__init__(dag)

    def generic_visit(self, node):
        #visit all children first
        Transformer.generic_visit(self, node)

        matched = match_node(self.root, node)
        if matched is None:
            return node

        #Replace current node with a clone of the replacement pattern
        new_children = [None for _ in range(self.rr.tile.num_inputs)]
        for (i, child) in matched:
            new_children[i] = child
        assert all(child is not None for child in new_children)
        replace_dag_copy = Clone(self.rr.replace(None)).dag_copy
        ReplaceInputs(replace_dag_copy, new_children)
        node_copy = replace_dag_copy.outputs[0]
        return node_copy

class GreedyCovering:
    def __init__(self, rrt: RewriteTable):
        self.rrt = rrt

    def __call__(self, dag: Dag):
        #Make a unique copy
        dag = Clone(dag).dag_copy
        for rr in self.rrt.rules:
            #Will update dag in place
            GreedyReplace(rr, dag)
        return dag


#What I want this to do:
#Given a list of rewrite rules, for each rewrite rule, do a covering to find a full covering
#class BinateCovering:
#    def __init__(self, rrt: RewriteTable):
#        self.rrt = rrt
#
#    def __call__(self, dag: Dag):
#        dag = Clone(dag).dag_copy
#        #Apply all the rewrite rules eagerly
#        for ri, rr in enumerate(self.rrt.rrs):
#            #mark each node if the pattern matches
#            MarkPattern(rr.pattern, ri, dag)
#            cover_sol = solve_cover(dag)
