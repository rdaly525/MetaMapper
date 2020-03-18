from metamapper.visitor import Visitor


class AddID(Visitor):
    def __init__(self, dag):
        self.curid = 0
        super().__init__(dag)

    def generic_visit(self, node):
        node._id_ = self.curid
        self.curid +=1
        Visitor.generic_visit(self, node)

class Printer(Visitor):
    def generic_visit(self, node):
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        print(f"{node._id_}<{type(node).__name__}>({child_ids})")
        Visitor.generic_visit(self, node)

    def visit_Input(self, node):
        print(f"{node._id_}<Input:{node.port_name}>")
        Visitor.generic_visit(self, node)

    def visit_Output(self, node):
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        print(f"Output:{node.port_name}({child_ids})")
        Visitor.generic_visit(self, node)

