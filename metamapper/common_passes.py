from DagVisitor import Visitor, Transformer
from .node import Nodes, Dag, Input, Common, Bind, Combine, Select, Constant, Output
from .family import fam
from peak.assembler import Assembler, AssembledADT
from hwtypes.modifiers import strip_modifiers
from peak.mapper.utils import Unbound
from .node import DagNode

class VerifyNodes(Visitor):
    def __init__(self, nodes: Nodes):
        self.nodes = nodes
        self.wrong_nodes = set()

    def verify(self, dag: Dag):
        self.run(dag)
        if len(self.wrong_nodes) > 0:
            return self.wrong_nodes
        return None

    def generic_visit(self, node):
        nodes = type(node).nodes
        if nodes != self.nodes and nodes != Common:
            self.wrong_nodes.add(node)
        Visitor.generic_visit(self, node)

from peak.mapper.utils import rebind_type, solved_to_bv
import pysmt.shortcuts as smt
from pysmt.logics import BV


#Returns None if equal, counter example for one input otherwise
def prove_equal(dag0: Dag, dag1: Dag, solver_name="z3"):
    if dag0.input.type != dag1.input.type:
        raise ValueError("Input types are not the same")
    if dag0.output.type != dag1.output.type:
        raise ValueError("Output types are not the same")
    i0, o0 = SMT().get(dag0)
    i1, o1 = SMT().get(dag1)

    formula = o0.substitute((i0, i1)) != o1

    with smt.Solver(solver_name, logic=BV) as solver:
        solver.add_assertion(formula.value)
        verified = not solver.solve()
        if verified:
            return None
        else:
            return solved_to_bv(i1, solver)

def _get_aadt(T):
    T = rebind_type(T, fam().SMTFamily())
    return fam().SMTFamily().get_adt_t(T)

class SMT(Visitor):
    def __init__(self):
        pass

    def get(self, dag: Dag):
        self.values = {}
        if len(dag.sources) !=1:
            raise NotImplementedError
        self.run(dag)
        return self.values[dag.input]._value_, self.values[dag.output]._value_

    def visit_Input(self, node : Input):
        aadt = _get_aadt(node.type)
        val = fam().SMTFamily().BitVector[aadt._assembler_.width]()
        self.values[node] = aadt(val)

    def visit_Constant(self, node: Constant):
        aadt = _get_aadt(node.type)
        if node.value is Unbound:
            value = 0
        else:
            value = node.value
        from hwtypes import AbstractBitVector, AbstractBit
        if issubclass(aadt, (AbstractBit, AbstractBitVector)):
            val = aadt(value)
        else:
            val = aadt(fam().SMTFamily().BitVector[aadt._assembler_.width](value))
        self.values[node] = val

    def visit_Select(self, node: Select):
        Visitor.generic_visit(self, node)
        self.values[node] = self.values[node.children()[0]][node.field]

    def visit_Combine(self, node: Combine):
        Visitor.generic_visit(self, node)
        vals = {field: self.values[child] for field, child in zip(node.type.field_dict.keys(), node.children())}
        aadt = _get_aadt(node.type)
        self.values[node] = aadt.from_fields(**vals)

    def visit_Output(self, node: Output):
        Visitor.generic_visit(self, node)
        vals = {field: self.values[child] for field, child in zip(node.type.field_dict.keys(), node.children())}
        aadt = _get_aadt(node.type)
        self.values[node] = aadt.from_fields(**vals)

    def generic_visit(self, node: DagNode):
        Visitor.generic_visit(self, node)
        peak_fc = node.nodes.peak_nodes[node.node_name]
        vals = {field: self.values[child] for field, child in zip(peak_fc.Py.input_t.field_dict.keys(), node.children())}
        outputs = peak_fc.SMT()(**vals)
        if not isinstance(outputs, tuple):
            outputs = (outputs,)

        aadt = _get_aadt(peak_fc.Py.output_t)
        output_val = aadt.from_fields(*outputs)
        self.values[node] = output_val



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

    def visit_Bind(self, node: Bind):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<Bind:{node.paths}>({child_ids})\n"


class BindsToCombines(Transformer):
    def gen_combine(self, node: Bind):
        if len(node.paths) == 1 and len(node.paths[0]) == 0:
            return node.children()[0]
        #print("Trying to Bind {")
        #print(node.type)
        #print(node.paths)
        assert len(node.type.field_dict) <= len(node.paths)
        #sort paths based off of first field
        field_info = {}
        for path, child in zip(node.paths, node.children()):
            assert len(path) > 0
            field = path[0]
            field_info.setdefault(field, {"paths":[], "children":[]})
            field_info[field]["paths"].append(path[1:])
            field_info[field]["children"].append(child)
        assert field_info.keys() == node.type.field_dict.keys()
        children = []
        for field, T in node.type.field_dict.items():
            sub_paths = field_info[field]["paths"]
            sub_children = field_info[field]["children"]
            sub_bind = Bind(*sub_children, paths=sub_paths, type=T, iname=node.iname + str(field))
            new_child = self.gen_combine(sub_bind)
            children.append(new_child)
        #print(children)
        #print(list(node.type.field_dict.items()))
        #print("}")
        return Combine(*children, type=node.type, iname= node.iname)
    def visit_Bind(self, node: Bind):
        Transformer.generic_visit(self, node)
        return self.gen_combine(node)


# Consolidates constants into a simpler Bind node
class SimplifyCombines(Transformer):
    def visit_Combine(self, node: Combine):
        Transformer.generic_visit(self, node)
        #create the binding
        const_dict = {}
        for child, field in zip(node.children(), node.type.field_dict.keys()):
            if not isinstance(child, Constant):
                return
            if child.value is Unbound:
                return
            const_dict[field] = child.value
        aadt = AssembledADT[strip_modifiers(node.type), Assembler, fam().PyFamily().BitVector]
        val = aadt.from_fields(**const_dict)
        return Constant(value=val._value_, type=node.type)


#Finds Opportunities to skip selecting from a Combine node
class RemoveSelects(Transformer):
    def visit_Select(self, node: Select):
        Transformer.generic_visit(self, node)
        child = node.children()[0]
        if not isinstance(child, Combine):
            return
        idx = -1
        for i, field in enumerate(child.type.field_dict):
            if node.field == field:
                idx = i
        assert idx != -1
        return child.children()[idx]


def print_dag(dag: Dag):
    AddID().run(dag)
    print(Printer().run(dag).res)

class CheckIfTree(Visitor):
    def __init__(self):
        self.parent_cnt = {}

    def is_tree(self, dag: Dag):
        not_tree = len(dag.sinks) != 1
        not_tree |= len(dag.output.children()) != 1
        if not_tree:
            return False
        self.run(dag)
        return all(cnt < 2 for cnt in self.parent_cnt.values())

    #If it is an input or a select of an input
    def is_input(self, node: DagNode):
        if isinstance(node, Input):
            return True
        elif isinstance(node, Select):
            return self.is_input(node.children()[0])
        else:
            return False
    def generic_visit(self, node):
        for child in node.children():
            if self.is_input(child):
                continue
            self.parent_cnt.setdefault(child, 0)
            self.parent_cnt[child] += 1
        Visitor.generic_visit(self, node)


class Clone(Visitor):
    def clone(self, dag: Dag, iname_prefix: str = ""):
        assert dag is not None
        self.node_map = {}
        self.iname_prefix = iname_prefix
        self.run(dag)
        dag_copy = Dag(
            sources=[self.node_map[node] for node in dag.sources],
            sinks=[self.node_map[node] for node in dag.sinks]
        )
        return dag_copy

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        new_node = node.copy()
        children = (self.node_map[child] for child in node.children())
        new_node.set_children(*children)
        new_node.iname = self.iname_prefix + new_node.iname
        self.node_map[node] = new_node