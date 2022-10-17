from DagVisitor import Transformer, Visitor
from metamapper.node import Constant, PipelineRegister
from metamapper.common_passes import print_dag

class DelayMatching(Transformer):
    def __init__(self, node_latencies):
        self.node_latencies = node_latencies
        self.aggregate_latencies = {}
        self.inserted_regs = 0

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
                    self.inserted_regs += 1
                new_children[i] = new_child
            node.set_children(*new_children)
            this_latency = self.node_latencies.get(node)
            self.aggregate_latencies[node] = max_latency + this_latency
            return node

def topological_sort_helper(dag, node, stack, visited):
    visited.add(node)
    for ns in node.children():
        if ns not in visited:
            topological_sort_helper(dag, ns, stack, visited)
    stack.append(node)

def topological_sort(dag):
    visited = set()
    stack = []
    for n in dag.roots():
        if n not in visited:
            topological_sort_helper(dag, n, stack, visited)
    return stack[::-1]

def is_input_sel(node):
    curr_node = node

    while True:
        if curr_node.node_name != "Select":
            return curr_node.node_name == "Input"
        assert len(curr_node.children()) == 1
        curr_node = curr_node.child

def get_connected_pe_name(node, sinks):
    curr_node = node
    while True:
        if curr_node.node_name == "global.PE":
            return curr_node.iname

        if len(sinks[curr_node]) != 1:
            return ""
        curr_node = sinks[curr_node][0]

def branch_delay_match(dag, node_latencies, sinks):

    sorted_nodes = topological_sort(dag)

    added_regs = 0
    node_cycles = {}
    input_latencies = {}

    for node in sorted_nodes:
        cycles = set()

        if len(sinks[node]) == 0:
            cycles = {0}

        for sink in sinks[node]:
            if sink not in node_cycles:
                c = 0
            else:
                c = node_cycles[sink]

            if c != None:
                c += node_latencies.get(node)

            cycles.add(c)

        if None in cycles:
            cycles.remove(None)

        if len(cycles) > 1:
            print(f"\t\tIncorrect node delay: {node} {cycles}")

            max_cycles = max(cycles)
            for sink in sinks[node]:
                new_child = node
                pipeline_type = node.type
                new_children = [child for child in sink.children()]
                for idx, c in enumerate(new_children):
                    if c == new_child:
                        for _ in range(max_cycles - node_cycles[sink]):
                            print("\t\tbreak", node, sink)
                            new_child = PipelineRegister(new_child, type=pipeline_type)
                            added_regs += 1

                        new_children[idx] = new_child
                sink.set_children(*new_children)
                
            node_cycles[node] = max_cycles
        elif len(cycles) == 1:
            node_cycles[node] = max(cycles)
        else:
            node_cycles[node] = None
        
        if is_input_sel(node):
            if len(cycles) > 0:
                if node.child.field not in input_latencies:
                    input_latencies[node.child.field] = {}
                input_latencies[node.child.field][str(node.field)] = {}
                input_latencies[node.child.field][str(node.field)]["latency"] = node_cycles[node]
                input_latencies[node.child.field][str(node.field)]["pe_port"] = get_connected_pe_name(node, sinks)
            node_cycles[node] = None

    return input_latencies, added_regs
        
