import coreir
from .visitor import Visited, Dag
from .node import DagNode
from functools import wraps
import abc
from enum import Enum
from collections import OrderedDict
from .irs.coreir import gen_CoreIRNodes

width = 16 #Assumption for now
CoreIRNodes = gen_CoreIRNodes(width)
Input = CoreIRNodes.dag_nodes["Input"]
Output = CoreIRNodes.dag_nodes["Output"]

#returns input objects and output objects
def parse_rtype(rtype):
    assert isinstance(rtype, coreir.Record)
    inputs = OrderedDict()
    outputs = OrderedDict()
    for n, t in rtype.items():
        if t.is_input():
            inputs[n] = t
        elif t.is_output():
            outputs[n] = t
        else:
            raise ValueError("Bad io type!")

    return inputs, outputs


def get_driver(port) -> ("iname", "port"):
    conns = port.connected_wireables
    assert len(conns) == 1
    driver = conns[0]
    dpath = driver.selectpath
    assert len(dpath) == 2
    return dpath[0], dpath[1]


#TODO this is really just coreir module to a dag where the instances in the coreir are nodes in nodes
class Loader:
    def __init__(self, mod, nodes: Nodes):
        raise NotImplementedError("Verify all instances are in nodes")
        self.mod = mod
        self.nodes = nodes
        self.c = mod.context
        self.node_map: tp.Mapping["inst", DagNode] = {}
        inputs, outputs = parse_rtype(mod.type)

        #Create all input nodes first
        input_nodes = []
        for n, t in inputs.items():
            #TODO verify t is a good type
            inode = Input(port_name=n)
            self.node_map[("self", n)] = inode
            input_nodes.append(inode)

        output_nodes = []
        for n, t in outputs.items():
            onode = self.add_output(n)
            self.node_map[("self", n)] = onode
            output_nodes.append(onode)
        self.dag = Dag(output_nodes, input_nodes)

    def add_output(self, port_name):
        io = self.mod.definition.interface
        iname, iport = get_driver(io.select(port_name))
        driver = self.add_node(iname, iport)
        return Output(driver, port_name=port_name)

    def add_node(self, iname, iport):
        if iname == "self":
            key = (iname, iport)
            assert key in self.node_map
            return self.node_map[key]
        if iname in self.node_map:
            return self.node_map[iname]
        inst = self.mod.definition.get_instance(iname)
        inputs, outputs = parse_rtype(inst.module.type)
        #iport should be the first and only output (for now)
        assert len(outputs)==1
        assert iport in outputs
        children = []
        for port, t in inputs.items():
            dname, dport = get_driver(inst.select(port))
            driver = self.add_node(dname, dport)
            children.append(driver)

        assert inst.module.namespace.name == 'coreir'
        mkind = inst.module.name
        node_name = self.nodes.from_coreir(mkind)
        NodeKind = self.dag_nodes[dag_node_name]
        node = NodeKind(*children, iname=iname)

        self.node_map[iname] = node
        return node

def coreir_to_dag(nodes: Nodes, cmod):
    return Loader(cmod, nodes).dag

#returns module, and map from instances to dags
def load_from_json(c, file):
    c.load_library("commonlib")
    c.load_library("lakelib")
    cmod = c.load_from_file(file)
    return cmod

# Hack
# custom inline the modules I care about (in Python)
# Run (isolate_coreir, removebulkconnections, flattentypes, 

#  What this needs to do
#  -Inline all modules that are commonlib but not lakelib
#    -Ideally mark commonlib generators to be inlined, then call inline pass
#    -Alternatively, 
#  Convert module into BitvectorForm:
#    -Flatten types of only that module (Unneeded for most things)
#    -removebulkconnections, use_slices/concats/muxes for BV<->Bool interactions
def preprocess(cmod):
    #First inline all commonlib instances (rungenerators for commonlbi first)
    raise NotImplementedError("TODO")

    #Run isolate_primitives pass
    c.run_passes("isolate_primtiives")

    #Find all instances of modules which need to be mapped (All the _.*primitives) modules
    primitive_blocks = []
    raise NotImplementedError("TODO")

    #dagify all the primitive_blocks
    pb_dags = {inst:coreir_module_to_dag(inst.module) for inst in primitive_blocks}
    return pb_dags
