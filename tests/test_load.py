import coreir
from metamapper import load_coreir_module
from dtf import Visitor

def test_load():
    c = coreir.Context()
    mod = c.load_from_file("examples/Add4.json")
    mod.print_()
    expr = load_coreir_module(mod) 

    class AddID(Visitor):
        def __init__(self,dag):
            self.curid = 0
            super().__init__(dag)

        def generic_visit(self,node):
            node._id_ = self.curid
            self.curid +=1
            Visitor.generic_visit(self,node)

    class Printer(Visitor):
        def generic_visit(self,node):
            child_ids = ", ".join([str(child._id_) for child in node.children()])
            print(f"{node._id_}<{node.iname}>({child_ids})")
            Visitor.generic_visit(self,node)

        def visit_Select(self,node):
            child_ids = ", ".join([str(child._id_) for child in node.children()])
            print(f"{node._id_}<select>({child_ids})")
            Visitor.generic_visit(self,node)

    AddID(expr)
    Printer(expr)
