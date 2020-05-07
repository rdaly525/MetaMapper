import coreir
from metamapper.coreir_util import coreir_to_dag
from metamapper.visitor import Visitor
from metamapper.irs.coreir import gen_CoreIRNodes
from metamapper import CoreIRContext

def test_visitor():
    c = CoreIRContext(reset=True)
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = c.load_from_file("examples/add4.json")
    dag = coreir_to_dag(CoreIRNodes, cmod)
    print(dag)
    print(list(dag.parents()))
    class AddID(Visitor):
        def __init__(self):
            self.curid = 0

        def generic_visit(self, node):
            node._id_ = self.curid
            self.curid +=1
            Visitor.generic_visit(self, node)

    class Printer(Visitor):
        def __init__(self):
            self.res = "\n"

        def generic_visit(self, node):
            child_ids = ", ".join([str(child._id_) for child in node.children()])
            self.res += f"{node._id_}<{node.kind()[0]}:{node.iname}>({child_ids})\n"
            Visitor.generic_visit(self, node)

        def visit_Select(self, node):
            self.res += f"{node._id_}<Select:{node.field}>({node.children()[0]._id_})\n"
            Visitor.generic_visit(self, node)

        def visit_Input(self, node):
            self.res += f"{node._id_}<Input:{node.iname}>\n"
            Visitor.generic_visit(self, node)

        def visit_Output(self, node):
            child_ids = ", ".join([str(child._id_) for child in node.children()])
            self.res += f"{node._id_}<Output:{node.iname}>({child_ids})\n"
            Visitor.generic_visit(self, node)

    AddID().run(dag)
    p = Printer()
    p.run(dag)
    assert p.res == '''
0<Output:out>(1)
1<add:a1>(2, 5)
2<add:a00>(3, 4)
3<Input:in0>
4<Input:in1>
5<add:a01>(6, 7)
6<Input:in2>
7<Input:in3>
'''

