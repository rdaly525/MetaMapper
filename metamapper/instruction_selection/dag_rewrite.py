from DagVisitor import Transformer
from ..rewrite_table import RewriteTable, RewriteRule
from ..node import Input, Dag
from ..common_passes import Clone, print_dag

class ReplaceInputs(Transformer):
    def __init__(self, replacements):
        self.reps = replacements

    def visit_Select(self, node):
        Transformer.generic_visit(self, node)
        if isinstance(node.children()[0], Input) and node.field in self.reps:
            return self.reps[node.field]

#Given a Dag, greedly apply the rewrite rule
class GreedyReplace(Transformer):
    def __init__(self, rr: RewriteRule, kernel_name_prefix=False):
        self.rr = rr
        #Match needs to match all output_selects up to but not including input_selects
        self.output_selects = rr.tile.output.children()
        self.input_selects = set(rr.tile.input.select(field) for field in rr.tile.input._selects)
        self.state_roots = rr.tile.sinks[1:]
        self.kernel_name_prefix = kernel_name_prefix
        if len(self.output_selects) > 1 or self.state_roots != []:
            raise NotImplementedError("TODO")

    def replace(self, dag: Dag):
        self.num_replace = 0
        self.run(dag)
        return self.num_replace

    def match_node(self, tile_node, dag_node, cur_matches):
        if tile_node in cur_matches:
            if cur_matches[tile_node] is not dag_node:
                return None
            else:
                return {}, {}

        if tile_node in self.input_selects:
            return {tile_node.field: dag_node}, {tile_node: dag_node}

        # Verify node types are identical
        if type(tile_node).node_name != type(dag_node).node_name:
            return None

        matched_inputs = {}
        matches = dict(cur_matches)
        for tile_child, dag_child in zip(tile_node.children(), dag_node.children()):
            matched = self.match_node(tile_child, dag_child, matches)
            if matched is None:
                return None
            child_inputs, child_matches = matched
            matched_inputs.update(child_inputs)
            matches.update(child_matches)
        return matched_inputs, matches

    def visit_Select(self, node):
        #visit all children first
        Transformer.generic_visit(self, node)


        matched = self.match_node(self.output_selects[0], node, {})
        if matched is None:
            return None
        self.num_replace += 1
        matched_inputs, _ = matched
        #What this is doing is pointing the matched inputs of the dag to the body of the tile.
        #Then replacing the body of the tile to this node
        #TODO verify and call with the matched dag
        rr_name = str(self.rr.name).replace(".", "_")
        if self.kernel_name_prefix:
            rr_name = f"{node.child.iname}${rr_name}"
        replace_dag_copy = Clone().clone(self.rr.replace(None), iname_prefix=f"{rr_name}_{node.iname}_")
        ReplaceInputs(matched_inputs).run(replace_dag_copy)
        return replace_dag_copy.output.children()[0]

class GreedyCovering:
    def __init__(self, rrt: RewriteTable, kernel_name_prefix=False):
        self.rrt = rrt
        self.kernel_name_prefix = kernel_name_prefix

    def __call__(self, dag: Dag):
        #Make a unique copy
        dag = Clone().clone(dag)
        for rr in self.rrt.rules:
            #Will update dag in place
            cnt = GreedyReplace(rr, self.kernel_name_prefix).replace(dag)
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
