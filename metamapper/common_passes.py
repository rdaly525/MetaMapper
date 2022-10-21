from collections import OrderedDict

from graphviz import Digraph
from DagVisitor import Visitor, Transformer
from .node import Nodes, Dag, Input, Common, Bind, Combine, Select, Constant, Output
from .family import fam
from peak.assembler import Assembler, AssembledADT
from hwtypes.modifiers import strip_modifiers
from peak.mapper.utils import Unbound
from peak import family, black_box
from peak.black_box import BlackBox
from .node import DagNode
import hwtypes as ht
from graphviz import Digraph




def is_unbound_const(node):
    return isinstance(node, Constant) and node.value is Unbound

class DagToPdf(Visitor):
    def __init__(self, no_unbound):
        self.no_unbound = no_unbound

    def doit(self, dag: Dag):
        AddID().run(dag)
        self.graph = Digraph()
        self.run(dag)
        return self.graph

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        def n2s(node):
            return f"{str(node)}_{node._id_}"
        if self.no_unbound and not is_unbound_const(node):
            self.graph.node(n2s(node))
        for i, child in enumerate(node.children()):
            if self.no_unbound and not is_unbound_const(child):
                self.graph.edge(n2s(child), n2s(node), label=str(i))

def gen_dag_img(dag, file, no_unbound=True):
    DagToPdf(no_unbound).doit(dag).render(filename=file)

class DagToPdfSimp(Visitor):
    def doit(self, dag: Dag):
        AddID().run(dag)
        self.plotted_nodes = {"global.PE", "Input", "Output","PipelineRegister"}
        self.child_list = []
        self.graph = Digraph()
        self.run(dag)
        return self.graph

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        def n2s(node):
            op = node.iname.split("_")[0]
            return f"{str(node)}_{node._id_}\n{op}"

        def find_child(node):
            if len(node.children()) == 0:
                return
            for child in node.children():
                if str(child) in self.plotted_nodes:      
                    self.child_list.append(child)
                else:
                    child_f = find_child(child)

        if str(node) in self.plotted_nodes:      
            find_child(node)
            for child in self.child_list:
                self.graph.edge(n2s(child), n2s(node))
            self.child_list = []


def gen_dag_img_simp(dag, file):
    DagToPdfSimp().doit(dag).render(filename=file)

#Translates DagNode
class Constant2CoreIRConstant(Transformer):
    def __init__(self, nodes: Nodes):
        self.nodes = nodes

    def visit_Constant(self, node: Constant):
        if node.type == ht.BitVector[16]:
            node_t = self.nodes.dag_nodes["coreir.const"]
        elif node.type == ht.Bit:
            node_t = self.nodes.dag_nodes["corebit.const"]
        else:
            return
        return node_t(node).select("out")


class Riscv2_Riscv(Transformer):
    def __init__(self, nodes, rv, Inst2):
        self.nodes = nodes
        self.rv = rv
        self.Inst2 = Inst2

    def visit_Riscv2(self, node):
        Transformer.generic_visit(self, node)
        assert node.num_children == 3
        inst2, rs1, rs2, = node.children()
        assert isinstance(inst2, Constant)
        riscv_node = self.nodes.dag_nodes["R32I_mappable"]
        BV= fam().PyFamily().BitVector
        Inst = self.rv.isa.ISA_fc.Py.Inst
        i0 = Constant(type=Inst, value=inst2.value[:30])
        i1 = Constant(type=Inst, value=inst2.value[30:])
        n0 = riscv_node(i0, Constant(type=BV[32],value=Unbound), rs1, rs2, Constant(type=BV[32],value=Unbound))
        n1 = riscv_node(i1, Constant(type=BV[32],value=Unbound), n0.select("rd"), n0.select("rd"), Constant(type=BV[32],value=Unbound))
        return n1

class TypeLegalize(Transformer):
    def __init__(self, WasmNodes:Nodes):
        self.WasmNodes = WasmNodes
        self.BV = fam().PyFamily().BitVector

    def const0(self, value):
        if value == self.BV[32](0):
            const0 = self.WasmNodes.dag_nodes["const0"]
            return const0(Constant(value=Unbound, type=self.BV[32])).select("out")

    def const1(self, value):
        if value == self.BV[32](1):
            const1 = self.WasmNodes.dag_nodes["const1"]
            return const1(Constant(value=Unbound, type=self.BV[32])).select("out")

    def constn1(self, value):
        if value == self.BV[32](-1):
            constn1 = self.WasmNodes.dag_nodes["constn1"]
            return constn1(Constant(value=Unbound,type=self.BV[32])).select("out")

    def const12(self, value):
        if value[:12].sext(20) == value:
            const12 = self.WasmNodes.dag_nodes["const12"]
            c = Constant(value=value[:12], type=self.BV[12])
            return const12(c).select("out")

    def const20(self, value):
        if value[:20].zext(12) == value:
            const20 = self.WasmNodes.dag_nodes["const20"]
            c = Constant(value=value[:20], type=self.BV[20])
            return const20(c).select("out")
        

    def constOther(self, value):
        lsb = self.const20(value[:16].zext(16))
        msb = self.const20(value[16:].zext(16))
        assert lsb is not None
        assert msb is not None
        shl = self.WasmNodes.dag_nodes["i32.shl"]
        or_ = self.WasmNodes.dag_nodes["i32.or_"]
        msb_shift = shl(msb, self.const12(value=self.BV[32](16))).select("out")
        return or_(lsb, msb_shift).select("out")

    def visit_Constant(self, node):
        value = node.value
        assert isinstance(value, self.BV[32])
        for f in (
            self.const0,
            self.const1,
            self.constn1,
            self.const12,
            self.const20,
            self.constOther
        ):
            new = f(value)
            if new is not None:
                return new
        raise NotImplementedError()

class Unbound2Const(Visitor):
    def visit_Constant(self, node):
        if node.value is Unbound:
            node.value = node.type(0)


class ExtractNames(Visitor):
    def __init__(self, nodes):
        self.nodes = nodes

    def extract(self, dag: Dag):
        self.ops = {}
        self.run(dag)
        return self.ops

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        if node.nodes == self.nodes:
            self.ops.setdefault(node.node_name, 0)
            self.ops[node.node_name] +=1

class DagNumNodes(Visitor):
    def __init__(self):
        self.num_nodes = 0

    def doit(self, dag: Dag):
        self.run(dag)
        return self.num_nodes

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        self.num_nodes += 1


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
        if hasattr(node, "node_name"):
            if node.node_name != "coreir.reg" and node.node_name != "memory.rom2" and node.node_name != "memory.fprom2":
                nodes = type(node).nodes
                if nodes != self.nodes and nodes != Common:
                    self.wrong_nodes.add(node)
        Visitor.generic_visit(self, node)

from peak.mapper.utils import rebind_type, solved_to_bv
import pysmt.shortcuts as smt
from pysmt.logics import QF_BV

def prove_formula(formula, solver, i1):
    with smt.Solver(solver, logic=QF_BV) as solver:
        solver.add_assertion(formula)
        print("Calling solver")
        verified = not solver.solve()
        if verified:
            return None
        else:
            for op in list(BlackBox.black_boxes.values()):
                print("New op")
                for i,o in op:
                    if not isinstance(i, tuple):
                        i = (i,)
                    print("inputs")
                    for ii in i:
                        print(solved_to_bv(ii, solver))
                    print("outputs")
                    if not isinstance(o, tuple):
                        o = (o,)
                    for oo in o:
                        print(solved_to_bv(oo, solver))
            return solved_to_bv(i1._value_, solver)

def make_black_box_condition(black_boxes):
    black_box_conditions = []
    for op in list(black_boxes.values()):
        op_conditions = []
        for i in range(len(op)-1):
            for j in range(i+1, len(op)):
                in0, out0 = op[i]
                in1, out1 = op[j]
                if not isinstance(in0, tuple):
                    in0 = (in0,)
                if not isinstance(in1, tuple):
                    in1 = (in1,)
                if not isinstance(out0, tuple):
                    out0 = (out0,)
                if not isinstance(out1, tuple):
                    out1 = (out1,)

                in_equals = []
                out_equals = []

                for i0,i1 in zip(in0, in1):
                    in_equals.append(smt.Equals(i0._value, i1._value))
                for o0,o1 in zip(out0, out1):
                    out_equals.append(smt.Equals(o0._value, o1._value))

                in_equal = smt.And(in_equals)           
                out_equal = smt.And(out_equals)           
                
                op_conditions.append(smt.Implies(in_equal, out_equal))
        op_condition = smt.And(op_conditions)
        black_box_conditions.append(op_condition)
    black_box_condition = smt.And(black_box_conditions)
    return black_box_condition


#Returns None if equal, counter example for one input otherwise
def prove_equal(dag0: Dag, dag1: Dag, solver_name="z3"):
    BlackBox.rst_black_boxes()
    if dag0.input.type != dag1.input.type:
        raise ValueError("Input types are not the same")
    if dag0.output.type != dag1.output.type:
        raise ValueError("Output types are not the same")
    i0, o0 = SMT().get(dag0)
    i1, o1 = SMT().get(dag1)

    black_box_condition = make_black_box_condition(BlackBox.black_boxes)
    same_in_different_out = o0._value_.substitute((i0._value_, i1._value_)) != o1._value_
    formula = smt.And(black_box_condition, same_in_different_out.value)
    return prove_formula(formula, solver_name, i1)

def eval_dag(dag, inputs):
    o = PY().get(dag, inputs)
    return o

class PY(Visitor):
    def __init__(self):
        pass

    def get(self, dag: Dag, inputs):
        self.values = {}
        if not isinstance(inputs, tuple):
            inputs = (inputs,)
        self.inputs = inputs

        #ensure inputs type is correct
        aadt = _get_aadt_py(dag.input.type)
        for exp, act in zip(aadt._fields_, inputs):
            assert exp == type(act)

        if len(dag.sources) !=1:
            raise NotImplementedError
        self.run(dag)
        return self.values[dag.output]

    def visit_Input(self, node : Input):
        aadt = _get_aadt_py(node.type)
        self.values[node] = aadt(*self.inputs)

    def visit_Constant(self, node: Constant):
        val = node.assemble(fam().PyFamily())
        print(val)
        self.values[node] = val

    def visit_Select(self, node: Select):
        Visitor.generic_visit(self, node)
        val =self.values[node.children()[0]]
        self.values[node] = val.value_dict[node.field]

    def visit_Combine(self, node: Combine):
        Visitor.generic_visit(self, node)
        vals = {field: self.values[child] for field, child in zip(node.type.field_dict.keys(), node.children())}
        aadt = _get_aadt_py(node.type)
        self.values[node] = aadt.from_fields(**vals)

    def visit_Output(self, node: Output):
        Visitor.generic_visit(self, node)
        vals = {field: self.values[child] for field, child in zip(node.type.field_dict.keys(), node.children())}
        aadt = _get_aadt_py(node.type)
        assert len(vals) == 1
        self.values[node] = aadt(*vals.values())

    def generic_visit(self, node: DagNode):
        Visitor.generic_visit(self, node)
        peak_fc = node.nodes.peak_nodes[node.node_name]
        vals = {field: self.values[child] for field, child in zip(peak_fc.Py.input_t.field_dict.keys(), node.children())}
        py = peak_fc.Py()
        outputs = py(**vals)
        if not isinstance(outputs, tuple):
            outputs = (outputs,)

        aadt = _get_aadt_py(peak_fc.Py.output_t)
        output_val = aadt(*outputs)
        self.values[node] = output_val

def _get_aadt_py(T):
    T = rebind_type(T, fam().PyFamily())
    return fam().PyFamily().get_adt_t(T)
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
        if dag.input not in self.values:
            aadt = _get_aadt(dag.input.type)
            val = fam().SMTFamily().BitVector[1]()
            self.values[dag.input] = aadt(val)
        return self.values[dag.input], self.values[dag.output]

    def visit_Input(self, node : Input):
        aadt = _get_aadt(node.type)
        val = fam().SMTFamily().BitVector[aadt._assembler_.width]()
        print(aadt._assembler_.width)
        self.values[node] = aadt(val)

    def visit_Constant(self, node: Constant):
        val = node.assemble(fam().SMTFamily())
        #aadt = _get_aadt(node.type)
        #if node.value is Unbound:
        #    value = 0
        #else:
        #    value = node.value
        #from hwtypes import AbstractBitVector, AbstractBit
        #if issubclass(aadt, (AbstractBit, AbstractBitVector)):
        #    val = aadt(value)
        #else:
        #    val = aadt(fam().SMTFamily().BitVector[aadt._assembler_.width](value))
        self.values[node] = val

    def visit_Select(self, node: Select):
        Visitor.generic_visit(self, node)
        val =self.values[node.children()[0]]
        self.values[node] = val[node.field]

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
        #outputs = peak_fc.SMT()(**vals)
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

class CountPEs(Visitor):
    def __init__(self):
        self.res = 0

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        if hasattr(node, "node_name"):
            if node.node_name == "global.PE":
                self.res += 1
        

    def visit_PE(self, node):
        Visitor.generic_visit(self, node)
        self.res += 1

    def visit_PE_wrapped(self, node):
        Visitor.generic_visit(self, node)
        self.res += 1

class Printer(Visitor):
    def __init__(self):
        self.res = "\n"

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        T = node.nodes.peak_nodes[node.node_name].Py.input_t
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<{node.kind()[0]}:{node._id_}, {list(T.field_dict.keys())}>({child_ids})\n"

    def visit_PipelineRegister(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<PipelineRegister>({node.child._id_})"

    def visit_RegisterSource(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<Register>"

    def visit_RegisterSink(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<Register>({node.child._id_})"

    def visit_Bind(self, node):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<{node.kind()[0]}:{node._id_}>({child_ids})\n"

    def visit_Select(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<Select:{node.field}>({node.children()[0]._id_})\n"

    def visit_Input(self, node):
        Visitor.generic_visit(self, node)
        self.res += f"{node._id_}<Input>{hex(id(node))}\n"

    def visit_InstanceInput(self, node):
        self.res += f"{node._id_}<InstanceInput>\n"

    def visit_Constant(self, node):
        self.res += f"{node._id_}<Constant>({node.value}{type(node.value)}, {node.type})>\n"

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<Output>({child_ids})\n"

    def visit_InstanceOutput(self, node):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<InstanceOutput>({child_ids})\n"

    def visit_Combine(self, node: Bind):
        Visitor.generic_visit(self, node)
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node._id_}<Combine:{list(node.type.field_dict.keys())}>({child_ids})\n"

class BindsToCombines(Transformer):
    def gen_combine(self, node: Bind):
        if len(node.paths) == 1 and len(node.paths[0]) == 0:
            return node.children()[0]
        #print("Trying to Bind {")
        #print(f"  type={list(node.type.field_dict.items())}")
        #print(f"  paths={node.paths}")
        #assert len(node.type.field_dict) <= len(node.paths)
        #sort paths based off of first field
        field_info = {}
        for path, child in zip(node.paths, node.children()):
            assert len(path) > 0
            field = path[0]
            assert field in node.type.field_dict
            field_info.setdefault(field, {"paths":[], "children":[]})
            field_info[field]["paths"].append(path[1:])
            field_info[field]["children"].append(child)
        #assert field_info.keys() == node.type.field_dict.keys()
        children = []
        tu_field = None
        for field, T in node.type.field_dict.items():
            if field not in field_info:
                continue
            if issubclass(node.type, (TaggedUnion, Sum)):
                tu_field = field
            sub_paths = field_info[field]["paths"]
            sub_children = field_info[field]["children"]
            sub_bind = Bind(*sub_children, paths=sub_paths, type=T, iname=node.iname + str(field))
            new_child = self.gen_combine(sub_bind)
            children.append(new_child)
        #print(f"  children={children}")
        #print("}")
        return Combine(*children, type=node.type, iname= node.iname, tu_field=tu_field)
    def visit_Bind(self, node: Bind):
        Transformer.generic_visit(self, node)
        return self.gen_combine(node)

from hwtypes.adt import Sum, TaggedUnion, Tuple, Product
# Consolidates constants into a simpler Bind node
class SimplifyCombines(Transformer):
    def visit_Combine(self, node: Combine):
        Transformer.generic_visit(self, node)

        aadt = AssembledADT[strip_modifiers(node.type), Assembler, fam().PyFamily().BitVector]
        if issubclass(node.type, (Product, Tuple)):
            const_dict = OrderedDict()
            for child, field in zip(node.children(), node.type.field_dict.keys()):
                if not isinstance(child, Constant):
                    return
                if child.value is Unbound:
                    return
                const_dict[field] = child.value
            if issubclass(node.type, Product):

                val = aadt.from_fields(**const_dict)
            else:
                val = aadt.from_fields(*const_dict.values())
        elif issubclass(node.type, (Sum, TaggedUnion)):
            child = node.children()[0]
            if not isinstance(child, Constant):
                return
            if child.value is Unbound:
                return
            if issubclass(node.type, TaggedUnion):
                val = aadt.from_fields(**{node.tu_field: child.value})
            else:
                val = aadt.from_fields(node.tu_field, child.value)
        else:
            raise NotImplementedError()
        return Constant(value=val._value_, type=node.type)

class CloneInline(Visitor):
    def clone(self, dag: Dag, input_nodes, iname_prefix: str = ""):
        assert dag is not None
        self.node_map = {node: node.copy() for node in dag.sources}
        self.iname_prefix = iname_prefix
        self.run(dag)

        input_nodes_copy = [self.node_map[node] for node in input_nodes]

        dag_copy = Dag(
            sources=[self.node_map[node] for node in dag.sources],
            sinks=[self.node_map[node] for node in dag.sinks]
        )
        return dag_copy, input_nodes_copy

    def visit_Input(self, node):
        pass

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        new_node = node.copy()
        children = (self.node_map[child] for child in node.children())
        new_node.set_children(*children)
        new_node.iname = self.iname_prefix + new_node.iname
        self.node_map[node] = new_node

class CustomInline(Transformer): 
    def __init__(self, rewrite_rules):
        self.rrs = rewrite_rules

    def visit_Select(self, node: Select):
        Transformer.generic_visit(self, node)
        if node.child.node_name in self.rrs:
            replace_dag, input_nodes = CloneInline().clone(*self.rrs[node.child.node_name], iname_prefix=node.iname)
            for in_node in input_nodes:
                new_children = list(in_node.children())
                for child_idx, child_node in enumerate(in_node.children()):
                    if child_node.node_name == "Select" and child_node.field == "in0":
                        new_children[child_idx] = node.child.children()[0]
                    elif child_node.node_name == "Select" and child_node.field == "in1":
                        new_children[child_idx] = node.child.children()[1]
                in_node.set_children(*new_children)
            return replace_dag.output.child

        return node 



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

def count_pes(dag: Dag):
    return CountPEs().run(dag).res

def dag_to_pdf(dag: Dag, filename):
    AddID().run(dag)
    DagToPdf().run(dag).graph.render(filename, view=False)

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
        self.node_map = {node: node.copy() for node in dag.sources}
        self.iname_prefix = iname_prefix
        self.run(dag)

        dag_copy = Dag(
            sources=[self.node_map[node] for node in dag.sources],
            sinks=[self.node_map[node] for node in dag.sinks]
        )
        return dag_copy

    def visit_Input(self, node):
        pass

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        new_node = node.copy()
        children = (self.node_map[child] for child in node.children())
        new_node.set_children(*children)
        new_node.iname = self.iname_prefix + new_node.iname
        self.node_map[node] = new_node

class Uses(Visitor):
    def uses(self, dag: Dag):
        self.uses = {}
        self.inputs = set()
        self.outputs = set()
        self.insts = {}
        self.run(dag)
        return self.uses, self.inputs, self.outputs, self.insts

    def generic_visit(self, node: DagNode):
        Visitor.generic_visit(self, node)
        assert node.num_children == 5
        inst, _, rs1, rs2, _ = node.children()
        assert isinstance(inst, Constant)
        self.uses.setdefault(node, {})
        for rs, idx in ((rs1,'rs1'), (rs2,'rs2')):
            if isinstance(rs, Constant):
                #if rs.value is not Unbound:
                #    raise ValueError(f"expected Unbound, not {rs.value}")
                continue
            self.uses[node][idx] = self.uses[rs]
        self.insts[node] = inst.assemble(fam().PyFamily())

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)
        for child in node.children():
            self.outputs.add(self.uses[child])

    def visit_Select(self, node: Select):
        Visitor.generic_visit(self, node)
        child = node.children()[0]
        if isinstance(child, Input):
            self.inputs.add(node.field)
            self.uses[node] = node.field
            self.uses[node.field] = {}
        else:
            if node.field != "rd":
                raise ValueError(f"{node.field} is not rd")
            assert node.field == "rd"
            self.uses[node] = child

    def visit_Constant(self, node):
        pass

    def visit_Combine(self, node: DagNode):
        raise NotImplementedError()

    def visit_Input(self, node):
        pass

#This will naively linearize the code
class Schedule(Visitor):
    def schedule(self, dag: Dag):
        self.insts = []
        self.run(dag)
        return self.insts

    def visit_R32I_mappable(self, node):
        Visitor.generic_visit(self, node)
        self.insts.append(node)


class ConstantPacking(Transformer):
    def __init__(self, pe_reg_info):
        self.pe_reg_info = pe_reg_info

    def pack_constant(self, node, value, port):
        if not hasattr(node, "assemble"):
            return False
        instr = node.assemble(family.PyFamily())
        aadt = AssembledADT[strip_modifiers(node.type), Assembler, family.PyFamily().BitVector]
        reg = self.pe_reg_info["port_to_reg"][port]
        reg_instr = getattr(instr, reg)
        const_instr = getattr(instr, port)

        if reg_instr._value_.value == self.pe_reg_info['instrs']['bypass'] or \
           reg_instr._value_.value == self.pe_reg_info['instrs']['reg']:
            # Can constant pack

            # Change register mode to const
            instr_size = reg_instr._to_bitvector_().size
            new_reg_instr = reg_instr.from_fields(ht.BitVector[instr_size](self.pe_reg_info['instrs']['const']))
            setattr(instr, reg, new_reg_instr)

            # Set value of const
            setattr(instr, port, value)
            
            const_dict = OrderedDict()
            for field in node.type.field_dict.keys():
                const_dict[field] = getattr(instr, field)

            node.value = aadt(**const_dict)._value_
            
            return True
        return False
        

    def generic_visit(self, node):
        Transformer.generic_visit(self, node)
        if node.node_name == "global.PE":
            ports = node._metadata_
            new_children = [child for child in node.children()]
            for port_idx, child in enumerate(node.children()):
                if child.node_name == "Select":
                    for child_ in child.children():
                        if child_.node_name == "coreir.const":
                            if self.pack_constant(new_children[0], child_.child.value, ports[port_idx][0]):
                                new_children[port_idx] = Constant(type=ht.BitVector[16],value=Unbound)
            node.set_children(*new_children)
        return node
