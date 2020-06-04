from DagVisitor import Visitor
from .node import Nodes, Dag, Input

class VerifyNodes(Visitor):
    def __init__(self, nodes: Nodes):
        self.nodes = nodes

    def visit_Input(self, node):
        Visitor.generic_visit(self, node)

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)

    def visit_Constant(self, node):
        Visitor.generic_visit(self, node)

    def visit_Select(self, node):
        Visitor.generic_visit(self, node)

    def generic_visit(self, node):
        if type(node).nodes != self.nodes:
            raise ValueError(f"{node} is not of type {self.nodes}")
        Visitor.generic_visit(self, node)

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
        self.res += f"{node._id_}<{node.kind()[0]}:{node._id_}>({child_ids})\n"
        Visitor.generic_visit(self, node)

    def visit_Select(self, node):
        self.res += f"{node._id_}<Select:{node.field}>({node.children()[0]._id_})\n"
        Visitor.generic_visit(self, node)

    def visit_Input(self, node):
        self.res += f"{node._id_}<Input>\n"
        Visitor.generic_visit(self, node)

    def visit_Constant(self, node):
        self.res += f"{node._id_}<Constant>({node.value})>\n"

    def visit_Output(self, node):
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<Output>({child_ids})\n"
        Visitor.generic_visit(self, node)

class Printer2(Visitor):
    def __init__(self):
        self.res = "\n"

    def generic_visit(self, node):
        child_ids = ", ".join([str(child.iname) for child in node.children()])
        self.res += f"{node.iname}<{node.kind()[0]}:{node.iname}>({child_ids})\n"
        Visitor.generic_visit(self, node)

    def visit_Select(self, node):
        self.res += f"{node.iname}<Select:{node.field}>({node.children()[0].iname})\n"
        Visitor.generic_visit(self, node)

    def visit_Input(self, node):
        self.res += f"{node.iname}<Input>\n"
        Visitor.generic_visit(self, node)

    def visit_Constant(self, node):
        self.res += f"{node.iname}<Constant>({node.value})>\n"

    def visit_Output(self, node):
        child_ids = ", ".join([str(child.iname) for child in node.children()])
        self.res += f"{node.iname}<Output>({child_ids})\n"
        Visitor.generic_visit(self, node)

def print_dag(dag: Dag):
    AddID().run(dag)
    print(Printer().run(dag).res)
    #print(Printer2().run(dag).res)

class CheckIfTree(Visitor):
    def __init__(self):
        self.parent_cnt = {}

    def is_tree(self, dag: Dag):
        not_tree = len(dag.sinks)!=1
        not_tree |= len(dag.output.children())!=1
        if not_tree:
            return False
        self.run(dag)
        return all(cnt <2 for cnt in self.parent_cnt.values())

    def generic_visit(self, node):
        for child in node.children():
            if isinstance(child, Input):
                continue
            self.parent_cnt.setdefault(child, 0)
            self.parent_cnt[child] += 1
        Visitor.generic_visit(self, node)

