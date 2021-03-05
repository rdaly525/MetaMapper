from DagVisitor import Transformer
from hwtypes import bit_vector 

class DelayMatching(Transformer):
    def __init__(self, RegT, BitRegT, node_latencies):
        self.RegT = RegT
        self.BitRegT = BitRegT
        self.node_latencies = node_latencies
        self.aggregate_latencies = {}

    def generic_visit(self, node):
        print(node.node_name, node.children())
        if len(node.children()) == 0:
            self.aggregate_latencies[node] = 0
            return
        Transformer.generic_visit(self, node)
        latencies = [self.aggregate_latencies[child]
                     for child in node.children()]
        max_latency = max(latencies)
        new_children = [child for child in node.children()]
        for i, child in enumerate(node.children()):
            if child.node_name == "Constant":
                continue
            latency = latencies[i]
            diff = max_latency - latency
            if diff == 0:
                continue
            new_child = child
            for reg_index in range(diff):  # diff = number of pipeline reg
                if new_child.type == bit_vector.Bit:
                    new_child = self.BitRegT(new_child).select('out')
                else:
                    new_child = self.RegT(new_child).select('out')
            new_children[i] = new_child
        node.set_children(*new_children)
        this_latency = self.node_latencies.get(node)
        self.aggregate_latencies[node] = max_latency + this_latency
        return node