from DagVisitor import Transformer, Visitor
from metamapper.node import Constant, PipelineRegister


class DelayMatching(Transformer):
    def __init__(self, node_latencies):
        self.node_latencies = node_latencies
        self.aggregate_latencies = {}

    def visit_Constant(self, node):
        self.aggregate_latencies[node] = None

    def visit_Source(self, node):
        self.aggregate_latencies[node] = 0

    def generic_visit(self, node):
        Transformer.generic_visit(self, node)
        assert len(node.children()) > 0
        latencies = [self.aggregate_latencies[child]
                     for child in node.children()]
        if all([late is None for late in latencies]):
            self.aggregate_latencies[node] = None
            return node
        else:
            max_latency = max([late for late in latencies if late is not None])    
            new_children = [child for child in node.children()]
            for i, child in enumerate(node.children()):
                latency = latencies[i]
                if latency is None:
                    continue
                diff = max_latency - latency
                if diff == 0:
                    continue
                new_child = child
                pipeline_type = child.type
                for reg_index in range(diff):  # diff = number of pipeline reg
                    new_child = PipelineRegister(new_child, type=pipeline_type)
                new_children[i] = new_child
            node.set_children(*new_children)
            this_latency = self.node_latencies.get(node)
            self.aggregate_latencies[node] = max_latency + this_latency
            return node

#Verifies that a kernel is branch-delay matched
class KernelDelay(Visitor):
    def __init__(self, node_latencies):
        self.node_latencies = node_latencies

    def doit(self, dag):
        self.aggregate_latencies = {}
        self.run(dag)
        output_latencies = [self.aggregate_latencies[root] if self.aggregate_latencies[root] != None else 0 for root in dag.roots()]
        if not all(output_latencies[0] == l for l in output_latencies):
            raise ValueError("Mismatched output latencies")
        return output_latencies[0]

    def visit_Constant(self, node):
        self.aggregate_latencies[node] = None

    def visit_Source(self, node):
        self.aggregate_latencies[node] = 0

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        latencies = [self.aggregate_latencies[child]
                     for child in node.children()]
        if len(latencies) == 0:
            return
        unique_latencies = set(latencies)
        if None in unique_latencies:
            unique_latencies.remove(None)
        if len(unique_latencies)==0:
            self.aggregate_latencies[node] = None
        elif len(unique_latencies) == 1:
            child_latency = unique_latencies.pop()
            this_latency = self.node_latencies.get(node)
            self.aggregate_latencies[node] = child_latency + this_latency
        else:
            raise ValueError("Dag is not delay matched", unique_latencies)

    def visit_PipelineRegister(self, node):
        Visitor.generic_visit(self, node)
        child = list(node.children())[0]
        if self.aggregate_latencies[child] is None:
            raise ValueError("Child of pipe register is constant")
        self.aggregate_latencies[node] = self.aggregate_latencies[child] + 1

