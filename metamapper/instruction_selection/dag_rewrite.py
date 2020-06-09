from DagVisitor import Visitor, Transformer
from ..rewrite_table import RewriteTable, RewriteRule
from ..node import Input, Dag
from ..common_passes import VerifyNodes, print_dag

class Clone(Visitor):
    def clone(self, dag: Dag, iname_prefix: str = ""):
        assert dag is not None
        self.node_map = {}
        self.iname_prefix = iname_prefix
        self.run(dag)
        dag_copy = Dag(
            sources=[self.node_map[node] for node in dag.sources],
            sinks=[self.node_map[node] for node in dag.sinks]
        )
        return dag_copy

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        new_node = node.copy()
        children = (self.node_map[child] for child in node.children())
        new_node.set_children(*children)
        new_node.iname = self.iname_prefix + new_node.iname
        self.node_map[node] = new_node

class ReplaceInputs(Transformer):
    def __init__(self, replacements):
        self.reps = replacements

    def visit_Select(self, node):
        Transformer.generic_visit(self, node)
        if isinstance(node.children()[0], Input) and node.field in self.reps:
            return self.reps[node.field]

#Given a Dag, greedly apply the rewrite rule
class GreedyReplace(Transformer):
    def __init__(self, rr: RewriteRule):
        self.rr = rr

        #Match needs to match all output_selects up to but not including input_selects
        self.output_selects = rr.tile.output.children()
        self.input_selects = set(rr.tile.input.select(field) for field in rr.tile.input._selects)
        self.state_roots = rr.tile.sinks[1:]
        if len(self.output_selects) > 1 or self.state_roots != []:
            raise NotImplementedError("TODO")

    def match_node(self, tile_node, dag_node):
        if tile_node in self.input_selects:
            return {tile_node.field:dag_node}

        # Verify p_node is a_node
        if type(tile_node) != type(dag_node):
            return None

        matches = {}
        for tile_child, dag_child in zip(tile_node.children(), dag_node.children()):
            child_matched = self.match_node(tile_child, dag_child)
            if child_matched is None:
                return None
            matches.update(child_matched)
        return matches

    def visit_Select(self, node):
        #visit all children first
        Transformer.generic_visit(self, node)

        matches = self.match_node(self.output_selects[0], node)
        if matches is None:
            return None
        #What this is doing is pointing the matched inputs of the dag to the body of the tile.
        #Then replacing the body of the tile to this node
        #TODO verify and call with the matched dag
        replace_dag_copy = Clone().clone(self.rr.replace(None), iname_prefix=f"{node.iname}_")
        ReplaceInputs(matches).run(replace_dag_copy)
        return replace_dag_copy.output.children()[0]

class GreedyCovering:
    def __init__(self, rrt: RewriteTable):
        self.rrt = rrt

    def __call__(self, dag: Dag):
        #Make a unique copy
        dag = Clone().clone(dag)
        for rr in self.rrt.rules:
            #Will update dag in place
            GreedyReplace(rr).run(dag)
        print_dag(dag)
        VerifyNodes(self.rrt.to).run(dag)
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
