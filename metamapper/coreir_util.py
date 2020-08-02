import coreir
from DagVisitor import Visitor, Transformer
from collections import OrderedDict
from .node import DagNode, Dag, Nodes, Input, Combine, Constant
from . import CoreIRContext
import typing as tp
from peak import family
from peak.mapper import Unbound
from peak.assembler import AssembledADT, Assembler, AssembledADTRecursor
from .common_passes import print_dag
from hwtypes.adt import Product, Enum
from peak.family import PyFamily
import os


#returns input objects and output objects
#removes clk and reset
def parse_rtype(rtype) -> tp.Mapping[str, coreir.Type]:
    assert isinstance(rtype, coreir.Record)
    inputs = OrderedDict()
    outputs = OrderedDict()
    for n, t in rtype.items():
        if t.kind not in ("Array", "Bit", "BitIn"):
            if t.kind == "Named":
                continue
            raise NotImplementedError(t.kind)
        if t.is_input():
            inputs[n] = t
        elif t.is_output():
            outputs[n] = t
        else:
            raise ValueError("Bad io type!")

    #Filter out "ASYNCRESET" and "CLK"
    for d in (inputs, outputs):
        for name in ("ASYNCRESET", "CLK"):
            if name in d:
                del d[name]
    return inputs, outputs


def ctype_to_adt(ctype: coreir.type):
    if ctype.kind in ("Bit", "BitIn"):
        return PyFamily().Bit
    elif ctype.kind == "Array":
        etype = ctype.element_type
        if etype.kind not in ("Bit", "BitIn"):
            raise NotImplementedError(f"Element type of array {etype.kind}")
        return PyFamily().BitVector[len(ctype)]
    else:
        raise NotImplementedError(ctype.kind)

def adt_to_ctype(adt):
    c = CoreIRContext()
    if issubclass(adt, PyFamily().BitVector):
        return c.Array(adt.size, c.Bit())
    elif issubclass(adt, PyFamily().Bit):
        return c.Bit()
    elif issubclass(adt, Enum):
        aadt_t = AssembledADT[adt, Assembler, PyFamily().BitVector]
        adt_t, assembler_t, _ = aadt_t.fields
        width = assembler_t(adt_t).width
        return c.Array(width, c.Bit())
    elif issubclass(adt, Product):
        fields = OrderedDict()
        for field, sub_adt in adt.field_dict.items():
            fields[field] = adt_to_ctype(sub_adt)
        return c.Record(fields)
    else:
        raise NotImplementedError(str(adt))

def fields_to_adt(inputs: dict, name):
    return Product.from_fields(name, {field:ctype_to_adt(CT) for field, CT in inputs.items()})

class Loader:
    def __init__(self, cmod: coreir.Module, nodes: Nodes):
        self.cmod = cmod
        self.nodes = nodes
        self.c = cmod.context
        self.node_map: tp.Mapping[coreir.Instance, str] = {}

        #Verify all instances are from particular nodes
        #TODO Find all stateful instances
        for inst in cmod.definition.instances:
            node_name = self.nodes.name_from_coreir(inst.module)
            if node_name is None:
                raise ValueError(f"{inst.module.name} was never loaded into {self.nodes}")
            if self.nodes.is_stateful(node_name):
                raise NotImplementedError("TODO")

        inputs, outputs = parse_rtype(cmod.type)
        input_adt = fields_to_adt(inputs, "Input")
        output_adt = fields_to_adt(outputs, "Output")

        source_nodes = [Input(iname="self", type=input_adt)]
        stateful_instances = [cmod.definition.interface]
        # load up node_map with source nodes
        for source, inst in zip(source_nodes, stateful_instances):
            self.node_map[inst] = source

        #create all the sinks
        sink_nodes = []
        for i, (source, inst) in enumerate(zip(source_nodes, stateful_instances)):
            sink_t = type(source).sink_t
            sink_adt = output_adt if i == 0 else None
            sink_node = self.add_node(inst, sink_t=sink_t, sink_adt=sink_adt)
            assert isinstance(sink_node, DagNode)
            sink_nodes.append(sink_node)
        self.dag = Dag(source_nodes, sink_nodes)

    def add_node(self, inst: coreir.Instance, sink_t=None, sink_adt=None):
        if sink_t is None and inst in self.node_map:
            return self.node_map[inst]
        if sink_t is None:
            node_name = self.nodes.name_from_coreir(inst.module)
            node_t = self.nodes.dag_nodes[node_name]
            assert issubclass(node_t, DagNode)
        else:
            node_t = sink_t
        children = []
        for child_inst, port in self.get_drivers(inst):
            child_node = self.add_node(child_inst)
            children.append(child_node.select(port))

        if inst is self.cmod.definition.interface:
            iname = "self"
        else:
            def get_adt(inst, k):
                vtype = inst.module.params[k]
                if vtype.kind is bool:
                    return PyFamily().Bit
                elif vtype.kind is PyFamily().BitVector:
                    #TODO HACK assuming 16 bit constants always
                    return PyFamily().BitVector[16]
                else:
                    raise NotImplementedError()

            modargs = [Constant(value=v.value, type=get_adt(inst, k)) for k, v in inst.config.items()]
            #TODO unsafe. Assumes that modargs are specified at the end.
            children += modargs
            iname = inst.name
        if sink_t is None:
            node = node_t(*children, iname=iname)
            self.node_map[inst] = node
        elif sink_adt is None:
            node = node_t(*children, iname=iname)
        else:
            node = node_t(*children, iname=iname, type=sink_adt)
        return node

    def inst_from_name(self, iname):
        if iname == "self":
            return self.cmod.definition.interface
        else:
            return self.cmod.definition.get_instance(iname)

    def inst_to_type(self, inst: coreir.Instance) -> coreir.Record:
        if inst is self.cmod.definition.interface:
            T = self.c.Flip(self.cmod.type)
        else:
            T = inst.module.type
        return T

    def get_drivers(self, inst: tp.Union[coreir.Instance, coreir.Interface]) -> tp.List[tp.Tuple[coreir.Instance, str]]:

        if inst is self.cmod.definition.interface:
            outputs, inputs = parse_rtype(self.cmod.type)
        else:
            inputs, outputs = parse_rtype(inst.module.type)
        drivers = []
        for port_name, t in inputs.items():
            port = inst.select(port_name)
            conns = port.connected_wireables
            assert len(conns) == 1, f"{len(conns)}, {port}"
            driver = conns[0]
            dpath = driver.selectpath
            assert len(dpath) == 2
            driver_iname, driver_port = dpath[0], dpath[1]
            driver_inst = self.inst_from_name(driver_iname)
            drivers.append((driver_inst, driver_port))
        return drivers

def coreir_to_dag(nodes: Nodes, cmod):
    return Loader(cmod, nodes).dag

#returns module, and map from instances to dags

def load_libs(libraries=[]):
    c = CoreIRContext()
    for lib in libraries:
        c.load_library(lib)

def load_from_json(file, libraries=[]):
    if not os.path.isfile(file):
        raise ValueError(f"{file} does not exist")
    c = CoreIRContext()
    for lib in libraries:
        c.load_library(lib)
    cmod = c.load_from_file(file)
    return cmod

def preprocess(CoreIRNodes: Nodes, cmod: coreir.Module) -> tp.Mapping[coreir.Instance, Dag]:

    c = cmod.context
    assert cmod.definition

    #Simple optimizations
    c.run_passes(["rungenerators", "deletedeadinstances"])

    #First inline all non-findable instances
    #TODO better mechanism for this
    to_inline = []
    for inst in cmod.definition.instances:
        mod_name = inst.module.name
        if mod_name in ("counter", "reshape", "absd"):
            to_inline.append(inst)
    for inst in to_inline:
        print("inlining", inst.name, inst.module.name)
        coreir.inline_instance(inst)

    c.run_passes(["isolate_primitives"])

    #Find all instances of modules which need to be mapped (All the *___primitives) modules
    primitive_blocks = []
    assert cmod.definition
    for inst in cmod.definition.instances:
        mod_name = inst.module.name
        if "___primitives" in mod_name:
            primitive_blocks.append(inst)
    assert len(primitive_blocks)==1
    #dagify all the primitive_blocks
    pb_dags = {inst:coreir_to_dag(CoreIRNodes, inst.module) for inst in primitive_blocks}
    return pb_dags

class ToCoreir(Visitor):
    def __init__(self, nodes: Nodes, def_: coreir.ModuleDef):
        self.coreir_const = CoreIRContext().get_namespace("coreir").generators["const"]
        self.coreir_pt = CoreIRContext().get_namespace("_").generators["passthrough"]
        self.nodes = nodes
        self.def_ = def_
        self.node_to_inst: tp.Mapping[DagNode, coreir.Wireable] = {}  # inst is really the output port of the instance

    def visit_Select(self, node):
        Visitor.generic_visit(self, node)
        child_inst = self.node_to_inst[node.children()[0]]
        self.node_to_inst[node] = child_inst.select(node.field)

    def visit_Input(self, node):
        self.node_to_inst[node] = self.def_.interface

    def visit_Constant(self, node):
        bv_val = node.value
        if bv_val is Unbound:
            self.node_to_inst[node] = None
            return
        iname ="c"+str(id(node))
        const_mod = self.coreir_const(width=bv_val.size)
        config = CoreIRContext().new_values(fields=dict(value=bv_val))
        inst = self.def_.add_module_instance(iname, const_mod, config=config)
        self.node_to_inst[node] = inst.select("out")

    def visit_Combine(self, node: Combine):
        raise NotImplementedError("TODO")
        #Visitor.generic_visit(self, node)
        #def create_pt(cinputs):
        #    rtype = CoreIRContext().Record(cinputs)
        #    assert isinstance(rtype, coreir.Record)
        #    pt_mod = self.coreir_pt(type=rtype)
        #    return pt_mod

        #pt_mod = create_pt(node.cinputs)
        #pt_inst = self.def_.add_module_instance(node.iname, pt_mod)
        #for path, child in zip(node.selects, node.children()):
        #    child_inst = self.node_to_inst[child]
        #    pt_sel = pt_inst.select("in")
        #    for field in path:
        #        pt_sel = pt_sel.select(field)
        #    self.def_.connect(child_inst, pt_sel)
        #self.node_to_inst[node] = pt_inst.select("out")

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        cmod_t = self.nodes.coreir_modules[type(node).node_name]

        # create new instance
        #TODO what if this has modparams?
        inst = self.def_.add_module_instance(node.iname, cmod_t)
        input_t = self.nodes.peak_nodes[node.node_name](family.PyFamily()).input_t
        inst_inputs = list(input_t.field_dict.keys())
        # Wire all the children (inputs)
        for port, child in zip(inst_inputs, node.children()):
            child_inst = self.node_to_inst[child]
            if child_inst is not None:
                self.def_.connect(child_inst, inst.select(port))
            else:
                coreir.connect_const(inst.select(port), 0)

        self.node_to_inst[node] = inst

        # CLK and ASYNC?
        #inst.ASYNCRESET @= self.io.RESET

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)

        _, outputs = parse_rtype(self.def_.module.type)
        io = self.def_.interface
        # Wire all the children (inputs)
        for port, child in zip(outputs.keys(), node.children()):
            child_inst = self.node_to_inst[child]
            if child_inst is not None:
                self.def_.connect(child_inst, io.select(port))


class VerifyUniqueIname(Visitor):
    def __init__(self):
        self.inames = {}

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        if node.iname in self.inames:
            raise ValueError(f"{node.iname} for {node} already used by {self.inames[node.iname]}")
        self.inames[node.iname] = node

    def visit_Input(self, node):
        pass

# Magma compiles output ports into either "O" for single outputs or "O0", "O1" etc for multi-output
# This pass replaces non-input selects to the better name
class FixSelects(Transformer):
    def __init__(self, nodes):
        self.field_map = {}
        for node_name in nodes._node_names:
            peak_fc = nodes.peak_nodes[node_name]
            dag_node = nodes.dag_nodes[node_name]
            assert issubclass(dag_node, DagNode), f"{dag_node}"
            peak_outputs = list(peak_fc(family.PyFamily()).output_t.field_dict.keys())
            if len(peak_outputs) == 1:
                self.field_map[dag_node] = {peak_outputs[0]: "O"}
            else:
                self.field_map[dag_node] = {name: f"O{i}" for i, name in enumerate(peak_outputs)}

    def visit_Select(self, node):
        Transformer.generic_visit(self, node)
        child = node.children()[0]
        if isinstance(child, (Input, Combine)):
            return None
        assert type(child) in self.field_map
        replace_field = self.field_map[type(child)][node.field]
        return child.select(replace_field)

        # Create a map from field to coreir field

#This will construct a coreir module from the dag with ref_type
def dag_to_coreir_def(nodes: Nodes, dag: Dag, ref_mod: coreir.Module) -> coreir.ModuleDef:
    VerifyUniqueIname().run(dag)
    FixSelects(nodes).run(dag)
    def_ = ref_mod.new_definition()
    ToCoreir(nodes, def_).run(dag)
    return def_
