import magma as m
from DagVisitor import Visitor
from .node import Nodes, Dag
from .coreir_util import parse_rtype
from collections import OrderedDict

def ctype_to_mtype(ct):
    if ct.kind is 'Array':
        et = ct.element_type
        if et.kind is 'Bit':
            return m.Out(m.Bits[ct.size])
        elif et.kind is 'BitIn':
            return m.In(m.Bits[ct.size])
        assert 0
    elif ct.kind is 'Bit':
        return m.In(m.Bit)
    elif ct.kind is 'BitIn':
        return m.Out(m.Bit)
    assert 0

class ToMagma(Visitor):
    def __init__(self, io, dag, nodes):
        self.nodes = nodes
        self.io = io
        self.node_to_inst = {} #inst is really the output port of the instance
        super().__init__(dag)

    def visit_Input(self, node):
        self.node_to_inst[node] = getattr(self.io, node.port_name)

    def visit_Constant(self, node):
        #TODO bit of a hack
        self.node_to_inst[node] = int(node.value) 

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        #create new instance
        node_kind = type(node).__name__
        NodeCircuit = self.nodes.modules[node_kind]
        inst = NodeCircuit()
        #Wire all the children (inputs)
        for port, child in zip(node.input_names(), node.children()):
            print(port, getattr(inst, port))
            print(self.node_to_inst[child])
            m.wire(getattr(inst, port), self.node_to_inst[child])

        #TODO assuming single output
        oport = node.output_names()[0]
        self.node_to_inst[node] = getattr(inst, oport)

        #TODO assuming there is a reset
        inst.ASYNCRESET @= self.io.RESET

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)
        output_port = getattr(self.io, node.port_name)
        child_inst = self.node_to_inst[node.inputs()[0]]
        m.wire(output_port, child_inst)

def dag_to_magma(cmod: "CoreIR.circuit", dag: Dag, nodes: Nodes):
    inputs, outputs = parse_rtype(cmod.type)

    mIO = OrderedDict()
    for pname, ct in {**inputs, **outputs}.items():
        mIO[pname] = ctype_to_mtype(ct)

    #TODO make ALU name be cmod.name
    class PE(m.Circuit):
        io = m.IO(**mIO) + m.ClockIO(has_reset=True)
        ToMagma(io, dag, nodes)

    return PE


