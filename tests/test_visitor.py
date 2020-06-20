import coreir
from metamapper.coreir_util import coreir_to_dag
from DagVisitor import Visitor
from metamapper.irs.coreir import gen_CoreIRNodes
from metamapper import CoreIRContext

def test_visitor():
    c = CoreIRContext(reset=True)
    CoreIRNodes = gen_CoreIRNodes(16)
    cmod = c.load_from_file("examples/add4.json")
    dag = coreir_to_dag(CoreIRNodes, cmod)
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
    print(p.res)
    assert p.res == '''
0<Output:self>(1)
1<Select:out>(2)
2<coreir.add:a1>(3, 8)
3<Select:out>(4)
4<coreir.add:a00>(5, 7)
5<Select:in0>(6)
6<Input:self>
7<Select:in1>(6)
8<Select:out>(9)
9<coreir.add:a01>(10, 11)
10<Select:in2>(6)
11<Select:in3>(6)
'''
