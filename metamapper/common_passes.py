from .visitor import Visitor, Dag
from .node import Nodes

class VerifyNodes(Visitor):
    def __init__(self, nodes: Nodes, dag: Dag):
        self.nodes = nodes
        super().__init__(dag)

    def visit_Input(self, node):
        Visitor.generic_visit(self, node)

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)

    def visit_Constant(self, node):
        Visitor.generic_visit(self, node)

    def generic_visit(self, node):
        if not isinstance(node, ArchNodes.dag_node_cls):
            print(f"{node} is not of type {ArchNodes.dag_node_cls}")
            assert 0
        Visitor.generic_visit(self, node)

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

class CheckIfTree(Visitor):
    def __init__(self, dag):
        self.parent_cnt = {}
        super().__init__(dag)
        self.is_tree = dag.num_outputs==1 and all(cnt <2 for cnt in self.parent_cnt.values())

    def generic_visit(self, node):
        for child in node.children():
            self.parent_cnt.setdefault(child, 0)
            self.parent_cnt[child] += 1
        Visitor.generic_visit(self, node)

class VerifyMapping(Visitor):
    def __init__(self, ArchNodes):
        self.ArchNodes = ArchNodes

    def visit_Input(self, node):
        Visitor.generic_visit(self, node)

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)

    def visit_Constant(self, node):
        Visitor.generic_visit(self, node)

    def generic_visit(self, node):
        if not isinstance(node, self.ArchNodes.dag_node_cls):
            raise ValueError(f"{node} is not of type {ArchNodes.dag_node_cls}")
        Visitor.generic_visit(self, node)
