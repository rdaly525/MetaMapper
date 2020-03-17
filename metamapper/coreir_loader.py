import coreir
from .visitor import Visited, Dag
from functools import wraps
import abc
from enum import Enum
from collections import OrderedDict
from .node import create_node, Node, Input, Output
from .irs.coreir import gen_CoreIR

width = 16 #Assumption for now
CoreIR = gen_CoreIR(width)

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

#def ctype_to_hwtype(ct):
#    if ct.kind is 'Array':
#        et = ct.element_type
#        assert et.kind is 'Bit' or et.kind is 'BitIn'
#        return BitVector[ct.size]
#    elif ct.kind is 'Bit' or et.kind is 'BitIn':
#        return Bit

#def cache_node(f):
#    @wraps(f)
#    def create_node(self,iname,sink=False):
#        key = (iname,sink)
#        if key in self.nodes:
#            return self.nodes[key]
#        node = f(self,iname,sink)
#        self.nodes[key] = node
#        return node
#    return create_node

class Loader:
    def __init__(self, mod):
        self.mod = mod
        self.c = mod.context
        self.nodes = {}
        inputs, outputs = parse_rtype(mod.type)

        #Create all input nodes first
        input_nodes = []
        for n, t in inputs.items():
            #TODO verify t is a good type
            inode = Input(port_name=n)
            self.nodes[("self", n)] = inode
            input_nodes.append(inode)

        output_nodes = []
        for n, t in outputs.items():
            onode = self.add_output(n)
            self.nodes[("self", n)] = onode
            output_nodes.append(onode)

        self.dag = Dag(output_nodes, input_nodes)

    def add_output(self, port_name):
        io = self.mod.definition.interface
        iname, iport = self.get_driver(io.select(port_name))
        driver = self.add_node(iname, iport)
        return Output(driver, port_name=port_name)

    def add_node(self, iname, iport):
        if iname == "self":
            key = (iname, iport)
            assert key in self.nodes
            return self.nodes[key]
        if iname in self.nodes:
            return self.nodes[iname]
        inst = self.mod.definition.get_instance(iname)
        inputs, outputs = parse_rtype(inst.module.type)
        #iport should be the first and only output (for now)
        assert len(outputs)==1
        assert iport in outputs
        children = []
        for port, t in inputs.items():
            dname, dport = self.get_driver(inst.select(port))
            driver = self.add_node(dname, dport)
            children.append(driver)

        assert inst.module.namespace.name == 'coreir'
        mkind = inst.module.name
        if mkind in CoreIR.dag_nodes:
            NodeKind = CoreIR.dag_nodes[mkind]
            node = NodeKind(*children, iname=iname)
        else:
            raise Exception(f"Missing {mkind}")

        self.nodes[iname] = node
        return node

    def get_driver(self, port) -> ("iname", "port"):
        conns = port.connected_wireables
        assert len(conns) == 1
        driver = conns[0]
        dpath = driver.selectpath
        assert len(dpath) == 2
        return dpath[0], dpath[1]

def load_coreir_module(mod):
    return Loader(mod).dag
