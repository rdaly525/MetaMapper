import coreir
from .visitor import Visited, Dag
from functools import wraps
import abc
from enum import Enum
from collections import OrderedDict


#def is_bitvector(ctype):
#    return issubclass(ctype, (BitVector, Bit))
##Node, Select, Expr = gen_multi_output_visited(is_bitvector)

class Node(Visited):
    def __init__(self, *children):
        assert len(children) == self.num_inputs
        self._children = children

    def children(self):
        yield from self._children

    def inputs(self):
        return self._children

    @property
    def num_inputs(self):
        return len(self.input_names())

    @property
    def num_outputs(self):
        return len(self.output_names())

    @abc.abstractmethod
    def input_names(self):
        pass

    @abc.abstractmethod
    def output_names(self):
        pass

    #def __getitem__(self, key : tp.Union[str,int]):
    #    if isinstance(key, int):
    #        assert key in range(self.num_outputs)
    #        key = tuple(self.Ts.keys())[0]
    #        return self.__getitem__(key)
    #    elif isinstance(key, str):
    #        return Select(self, key)

class Expr(Dag):
    def __init__(self, outputs, inputs):
        self.inputs = inputs
        self.outputs = outputs
        super().__init__(outputs)

    def outputs(self):
        return self._parents

    @property
    def num_outputs(self):
        return self.num_parents

    @property
    def num_inputs(self):
        return len(self.inputs)

class Op(Enum):
    Add=0
    Mul=1
    And=2
    Or=3
    Xor=4

class Input(Node):
    def __init__(self, port_name):
        self.port_name = port_name
        super().__init__()

    def input_names(self):
        return []

    def output_names(self):
        return [self.port_name]

class Output(Node):
    def __init__(self, port_name, child):
        self.port_name = port_name
        super().__init__(child)

    def input_names(self):
        return [self.port_name]

    def output_names(self):
        return []

class Add(Node):
    def __init__(self, iname, in0, in1):
        self.iname = iname
        super().__init__(in0, in1)

    def input_names(self):
        return ["in0", "in1"]

    def output_names(self):
        return ["out"]

#class Const(Node):
#    def __init__(self, value : BitVector):
#        self.value = value
#        super().__init__(type(value))


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
            inode = Input(n)
            self.nodes[("self", n)] = inode
            input_nodes.append(inode)

        output_nodes = []
        for n, t in outputs.items():
            onode = self.add_output(n)
            self.nodes[("self", n)] = onode
            output_nodes.append(onode)

        self.expr = Expr(output_nodes, input_nodes)

    def add_output(self, port_name):
        io = self.mod.definition.interface
        iname, iport = self.get_driver(io.select(port_name))
        driver = self.add_node(iname, iport)
        return Output(port_name, driver)

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
        if mkind == "add":
            node = Add(iname, *children)
        else:
            assert 0
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
    return Loader(mod).expr
