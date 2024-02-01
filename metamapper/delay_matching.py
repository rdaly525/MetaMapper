from DagVisitor import Transformer, Visitor
from metamapper.node import Constant, PipelineRegister
from metamapper.common_passes import print_dag, GetSinks

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
    fields = []
    curr_node = node

    while True:
        if curr_node.node_name == "Select":
            fields.append(str(curr_node.field))
        else:
            if curr_node.node_name == "Input":
                return fields
            else:
                return None
        assert len(curr_node.children()) == 1
        curr_node = curr_node.child

def get_connected_pe_name(ret_list, source, node, sinks):  
    if len(sinks[node]) == 0:
        return 
    elif node.node_name == "global.PE":
        ret_list.append((node.iname, node._metadata_[node.children().index(source)][0]))
        return 
    elif node.node_name == "PipelineRegister":
       ret_list.append((node.iname, "reg"))
       return 
    else:
        for sink in sinks[node]:
            get_connected_pe_name(ret_list, node, sink, sinks)
        

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
        
        sinks = GetSinks().doit(dag)

        fields = is_input_sel(node)
        if fields is not None:
            if len(cycles) > 0:
                fields.reverse()

                latenciy_dict_key = "_".join(fields)

                connected_pes = []
                get_connected_pe_name(connected_pes, node, node, sinks)
                input_latencies[latenciy_dict_key] = {"latency": node_cycles[node], "pe_port": connected_pes}
            node_cycles[node] = None

    return input_latencies, added_regs
        
