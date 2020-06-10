from DagVisitor import Visitor, Transformer
from .node import Nodes, Dag, Input, Common, Combine, Select, Constant
from peak.mapper import SimplifyBinding, strip_aadt
from peak.family import PyFamily
from peak.assembler import Assembler, AssembledADT
from hwtypes.modifiers import strip_modifiers
from peak.mapper.utils import Unbound, pretty_print_binding
from .node import DagNode

class VerifyNodes(Visitor):
    def __init__(self, nodes: Nodes):
        self.nodes = nodes

    def generic_visit(self, node):
        nodes = type(node).nodes
        if nodes != self.nodes and nodes != Common:
            raise ValueError(f"{node} is not of type {self.nodes}")
        Visitor.generic_visit(self, node)

class AddID(Visitor):
    def __init__(self):
        self.curid = 0

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        node._id_ = self.curid
        self.curid += 1

class Printer(Visitor):
    def __init__(self):
        self.res = "\n"

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<{node.kind()[0]}:{node._id_}>({child_ids})\n"

    def visit_Select(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<Select:{node.field}>({node.children()[0]._id_})\n"

    def visit_Input(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<Input>\n"

    def visit_Constant(self, node):
        self.res += f"{node._id_}<Constant>({node.value})>\n"

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<Output>({child_ids})\n"

    def visit_Combine(self, node: Combine):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<Combine:{node.paths}>({child_ids})\n"


# Consolidates constants into a simpler Combine node
class SimplifyCombines(Transformer):
    def visit_Combine(self, node: Combine):
        Transformer.generic_visit(self, node)
        #create the binding
        binding = []
        for child, path in zip(node.children(), node.paths):
            if isinstance(child, Constant):
                from_ = child.value
            else:
                from_ = (child,)
            binding.append((from_, path))

        aadt = AssembledADT[strip_modifiers(node.type), Assembler, PyFamily().BitVector]
        new_binding = strip_aadt(SimplifyBinding()(aadt, binding))
        if len(new_binding) == len(binding):
            return
        new_children = []
        new_paths = []
        for from_, to_ in new_binding:
            if isinstance(from_, tuple):
                assert len(from_) == 1
                child = from_[0]
                assert isinstance(child, DagNode)
            else:
                child = Constant(value=from_)
            new_paths.append(to_)
            new_children.append(child)
        new_combine = Combine(*new_children, paths=new_paths, type=node.type, iname=node.iname)
        return new_combine

#Finds Opportunities to skip selecting from a Combine node
class RemoveSelects(Transformer):
    def visit_Select(self, node: Select):
        Transformer.generic_visit(self, node)
        child = node.children()[0]
        if not isinstance(child, Combine):
            return
        if (node.field,) in child.paths:
            idx = child.paths.index((node.field,))
            return child.children()[idx]


def print_dag(dag: Dag):
    AddID().run(dag)
    print(Printer().run(dag).res)

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

