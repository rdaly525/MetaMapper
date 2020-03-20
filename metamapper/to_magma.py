import magma as m
from .visitor import Visitor, Dag
from .node import Nodes
from .coreir_loader import parse_rtype
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
    elif et.kind is 'BitIn':
        return m.Out(m.Bit)
    assert 0

    #add00 = Alu_m(name="add00")
    #add01 = Alu_m(name="add01")
    #add1 = Alu_m(name="add1")
    #add00.ASYNCRESET @= io.RESET
    #add01.ASYNCRESET @= io.RESET
    #add1.ASYNCRESET @= io.RESET
    #add00.inst @= 2
    #add01.inst @= 2
    #add1.inst @= 2
    #add1.inst @= 2
    #m.wire(io.in0, add00.a)
    #m.wire(io.in1, add00.b)
    #m.wire(io.in2, add01.a)
    #m.wire(io.in3, add01.b)
    #m.wire(add00.O, add1.a)
    #m.wire(add01.O, add1.b)
    #m.wire(add1.O, io.out)


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

    #TODO make ALU name generic
    class ALU(m.Circuit): 
        io = m.IO(**mIO) + m.ClockIO(has_reset=True)
        ToMagma(io, dag, nodes)

    return ALU
