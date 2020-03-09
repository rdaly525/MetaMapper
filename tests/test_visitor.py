import coreir
from metamapper import load_coreir_module
from metamapper.visitor import Visitor

def test_visitor():
    c = coreir.Context()
    mod = c.load_from_file("examples/add4.json")
    expr = load_coreir_module(mod)

    class AddID(Visitor):
        def __init__(self, dag):
            self.curid = 0
            super().__init__(dag)

        def generic_visit(self, node):
            node._id_ = self.curid
            self.curid +=1
            Visitor.generic_visit(self, node)

    class Printer(Visitor):
        def __init__(self, dag):
            self.res = "\n"
            super().__init__(dag)

        def generic_visit(self, node):
            child_ids = ", ".join([str(child._id_) for child in node.children()])
            self.res += f"{node._id_}<{node.kind()[0]}:{node.iname}>({child_ids})\n"
            Visitor.generic_visit(self, node)

        def visit_Input(self, node):
            self.res += f"{node._id_}<Input:{node.port_name}>\n"
            Visitor.generic_visit(self, node)

        def visit_Output(self, node):
            child_ids = ", ".join([str(child._id_) for child in node.children()])
            self.res += f"{node._id_}<Output:{node.port_name}>({child_ids})\n"
            Visitor.generic_visit(self, node)

    AddID(expr)
    p = Printer(expr)
    print(p.res)
    assert p.res == '''
0<Output:out>(1)
1<Add:a1>(2, 5)
2<Add:a00>(3, 4)
3<Input:in0>
4<Input:in1>
5<Add:a01>(6, 7)
6<Input:in2>
7<Input:in3>
'''

