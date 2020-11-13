import coreir
from DagVisitor import Visitor, Transformer
from collections import OrderedDict
from .node import DagNode, Dag, Nodes, Source, Sink, Input, InstanceInput, Combine, Constant, Select
from . import CoreIRContext
import typing as tp
from .family import fam
from peak.mapper import Unbound
from peak.assembler import AssembledADT, Assembler, AssembledADTRecursor
from .common_passes import print_dag
from hwtypes.adt import Product, Enum, Tuple
import os
import keyword
from hwtypes.adt import Product
from hwtypes.modifiers import strip_modifiers, is_modified

#There is a hack where names aliasing with python keywords need to get remapped
#Use this function to select into coreir instances
def select(inst, name):
    if isinstance(name, int):
        name = str(name)
    if len(name) > 3 and name[-3:]=="___":
        name = name[:-3]
    return inst.select(name)

#returns input objects and output objects
#removes clk and reset

def fix_keyword(val:str):
    if val.isdigit():
        return int(val)
    if val in keyword.kwlist:
        return val + "___"
    return val

def parse_rtype(rtype) -> tp.Mapping[str, coreir.Type]:
    assert isinstance(rtype, coreir.Record)
    inputs = OrderedDict()
    outputs = OrderedDict()
    for n, t in rtype.items():
        n = fix_keyword(n)
        if t.kind == "Named":
            continue
        if t.kind not in ("Array", "Bit", "BitIn", "Record"):
            if t.kind == "Named":
                continue
            raise NotImplementedError(t.kind)
        if t.is_input():
            inputs[n] = t
        elif t.is_output():
            outputs[n] = t
        else:
            raise NotImplementedError("mixed io type not supported!")

    #Filter out "ASYNCRESET" and "CLK"
    for d in (inputs, outputs):
        for name in ("ASYNCRESET", "CLK"):
            if name in d:
                del d[name]
    return inputs, outputs

_PRODUCT_CNT = 0
def ctype_to_adt(ctype: coreir.type):
    if ctype.kind in ("Bit", "BitIn"):
        return fam().PyFamily().Bit
    elif ctype.kind == "Array":
        etype = ctype.element_type
        if etype.kind in ("Bit", "BitIn"):
            return fam().PyFamily().BitVector[len(ctype)]
        else:
            elem_adt = ctype_to_adt(etype)
            return Tuple[(elem_adt for _ in range(len(ctype)))]
    elif ctype.kind == "Record":
        assert isinstance(ctype, coreir.Record)
        field_dict = OrderedDict()
        for n, t in ctype.items():
            field_dict[n] = ctype_to_adt(t)
        global _PRODUCT_CNT
        pt = Product.from_fields(f"T{_PRODUCT_CNT}", field_dict)
        _PRODUCT_CNT += 1
        return pt

def adt_to_ctype(adt):
    c = CoreIRContext()
    if issubclass(adt, fam().PyFamily().BitVector):
        return c.Array(adt.size, c.Bit())
    elif issubclass(adt, fam().PyFamily().Bit):
        return c.Bit()
    elif issubclass(adt, Enum):
        aadt_t = AssembledADT[adt, Assembler, fam().PyFamily().BitVector]
        adt_t, assembler_t, _ = aadt_t.fields
        width = assembler_t(adt_t).width
        return c.Array(width, c.Bit())
    elif issubclass(adt, Product):
        fields = OrderedDict()
        for field, sub_adt in adt.field_dict.items():
            if field == "__fake__":
                continue
            fields[field] = adt_to_ctype(sub_adt)
        return c.Record(fields)
    elif issubclass(adt, Tuple):
        sub_adts = []
        for i, sub_adt in adt.field_dict.items():
            sub_adts.append(adt_to_ctype(sub_adt))
        if not all(sub_adt==sub_adts[0] for sub_adt in sub_adts):
            raise ValueError("Cannot handle tuple of different types")
        return c.Array(len(sub_adts), sub_adts[0])
    else:
        raise NotImplementedError(str(adt))

def fields_to_adt(inputs: dict, name):
    if len(inputs)==0:
        return Product.from_fields(name, {"__fake__": fam().PyFamily().Bit})
    return Product.from_fields(name, {field:ctype_to_adt(CT) for field, CT in inputs.items()})

class Loader:
    def __init__(self, cmod: coreir.Module, nodes: Nodes):
        self.cmod = cmod
        self.nodes = nodes
        self.c = cmod.context
        self.node_map: tp.Mapping[coreir.Instance, str] = {}

        inputs, outputs = parse_rtype(cmod.type)
        input_adt = fields_to_adt(inputs, "Input")
        output_adt = fields_to_adt(outputs, "Output")

        source_nodes = [Input(iname="self", type=input_adt)]
        stateful_instances = {cmod.definition.interface: output_adt}
        for inst in cmod.definition.instances:
            node_name = self.nodes.name_from_coreir(inst.module)
            #print("node_name: ", node_name, inst.module.name)
            source_node_t = None
            if node_name is None:
                source_node_t = InstanceInput
            elif self.nodes.is_stateful(node_name):
                source_node_t, _ = self.nodes.dag_nodes[node_name]
            if source_node_t is not None:
                inputs, outputs = parse_rtype(inst.module.type)
                sink_adt = fields_to_adt(inputs, f"{inst.name}_sink")
                source_adt = fields_to_adt(outputs, f"{inst.name}_source")
                node = source_node_t(iname=inst.name, type=source_adt)
                source_nodes.append(node)
                stateful_instances[inst] = sink_adt

        # load up node_map with source nodes
        for source, inst in zip(source_nodes, stateful_instances.keys()):
            self.node_map[inst] = source

        #create all the sinks
        sink_nodes = []
        for source, (inst, sink_adt) in zip(source_nodes, stateful_instances.items()):
            sink_t = type(source).sink_t
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
        for i, (child_inst, sel_path) in enumerate(self.get_drivers(inst)):
            if (child_inst, sel_path) == (None, None):
                children.append(Constant(value=Unbound, type=None))
            else:
                child_node = self.add_node(child_inst)
                child = child_node
                for sel in sel_path:
                    sel = fix_keyword(sel)
                    child = child.select(sel)
                children.append(child)

        if inst is self.cmod.definition.interface:
            iname = "self"
        else:
            def get_adt(inst, k):
                vtype = inst.module.params[k]
                if vtype.kind is bool:
                    return fam().PyFamily().Bit
                elif vtype.kind is fam().PyFamily().BitVector:
                    #TODO HACK assuming 16 bit constants always
                    return fam().PyFamily().BitVector[16]
                else:
                    raise NotImplementedError()

            if inst.module.name != "rom2":
                modargs = [Constant(value=v.value, type=get_adt(inst, k)) for k, v in inst.config.items()]
                #TODO unsafe. Assumes that modargs are specified at the end.
                children += modargs
            iname = inst.name

            
        if inst.module.name == "rom2":
            node = node_t(*children, init=inst.config["init"], iname=iname)
        elif sink_t is None:
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
            port = select(inst, port_name)
            conns = port.connected_wireables
            if len(conns) == 0:
                drivers.append((None, None))
            else:
                assert len(conns) == 1, f"{len(conns)}, {port}"
                driver = conns[0]
                dpath = driver.selectpath
                driver_iname, driver_ports = dpath[0], dpath[1:]
                driver_inst = self.inst_from_name(driver_iname)
                drivers.append((driver_inst, driver_ports))
        return drivers

#Takes in a coreir module and translates it into a dag
def coreir_to_dag(nodes: Nodes, cmod: coreir.Module) -> Dag:

    c = cmod.context
    assert cmod.definition

    #Simple optimizations
    c.run_passes(["rungenerators", "deletedeadinstances"])
    # c.run_passes(["flatten", "removebulkconnections", "flattentypes"])

    #First inline all non-findable instances
    #TODO better mechanism for this
    for _ in range(3):
        to_inline = []
        for inst in cmod.definition.instances:
            mod_name = inst.module.name
            if mod_name in ("counter", "reshape", "absd", "umax", "umin", "smax", "smin", "abs", "sle"):
                to_inline.append(inst)
        for inst in to_inline:
            print("inlining", inst.name, inst.module.name)
            coreir.inline_instance(inst)
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

def preprocess(CoreIRNodes: Nodes, cmod: coreir.Module) -> Dag:

    c = cmod.context
    assert cmod.definition

    #Simple optimizations
    # c.run_passes(["rungenerators", "deletedeadinstances"])
    # c.run_passes(["flatten", "removebulkconnections"])

    #First inline all non-findable instances
    #TODO better mechanism for this
    to_inline = []
    for inst in cmod.definition.instances:
        mod_name = inst.module.name
        if mod_name in ("absd", "umax", "umin", "smax", "smin", "abs", "sle"):
            to_inline.append(inst)
    for inst in to_inline:
        print("inlining", inst.name, inst.module.name)
        coreir.inline_instance(inst)

    return coreir_to_dag(CoreIRNodes, cmod)

class ToCoreir(Visitor):
    def __init__(self, nodes: Nodes, def_: coreir.ModuleDef):
        self.coreir_const = CoreIRContext().get_namespace("coreir").generators["const"]
        self.coreir_bit_const = CoreIRContext().get_namespace("corebit").modules["const"]
        self.coreir_pt = CoreIRContext().get_namespace("_").generators["passthrough"]
        self.nodes = nodes
        self.def_ = def_
        self.node_to_inst: tp.Mapping[DagNode, coreir.Wireable] = {}  # inst is really the output port of the instance

    def doit(self, dag: Dag):
        #Create all the instances for the Source/Sinks first
        for sink in list(dag.roots())[1:]:
            inst = self.create_instance(sink)
            self.node_to_inst[sink] = inst
            self.node_to_inst[sink.source] = inst
        self.run(dag)

    def visit_Select(self, node):
        Visitor.generic_visit(self, node)
        child_inst = self.node_to_inst[node.children()[0]]
        self.node_to_inst[node] = select(child_inst, node.field)

    def visit_Input(self, node):
        self.node_to_inst[node] = self.def_.interface

    def visit_Source(self, node):
        assert node.sink in self.node_to_inst
        self.node_to_inst[node] = self.node_to_inst[node.sink]

    def visit_Constant(self, node):
        assert isinstance(node, Constant)
        bv_val = node.value
        if bv_val is Unbound:
            self.node_to_inst[node] = None
            return
        is_bool = type(bv_val) is fam().PyFamily().Bit
        if is_bool:
            const_mod = self.coreir_bit_const
            bv_val = bool(bv_val)
        else:
            const_mod = self.coreir_const(width=bv_val.size)
        config = CoreIRContext().new_values(fields=dict(value=bv_val))
        iname = "c" + str(id(node))
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

    def create_instance(self, node):
        if node in self.node_to_inst:
            return self.node_to_inst[node]
        cmod_t = self.nodes.coreir_modules[type(node).node_name]
        # create new instance
        #create modparams
        children = list(node.children())
        config_fields = {}
        for param in reversed(type(node).modparams):
            child = children.pop(-1)
            assert isinstance(child, Constant)
            bv_val = child.value
            if bv_val is Unbound:
                continue
            config_fields[param] = bv_val
        if len(config_fields) > 0:
            config = CoreIRContext().new_values(fields=config_fields)
            inst = self.def_.add_module_instance(node.iname, cmod_t, config=config)
        else:
            inst = self.def_.add_module_instance(node.iname, cmod_t)
        return inst

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        
        if type(node).node_name == "memory.rom2":
            rom_mod = self.nodes.coreir_modules["memory.rom2"]
            config = CoreIRContext().new_values(dict(init=node.init))
            inst = self.def_.add_module_instance(node.iname, rom_mod, config=config)
        else:
            inst = self.create_instance(node)
        inst_inputs = list(self.nodes.peak_nodes[node.node_name].Py.input_t.field_dict.keys())
        # Wire all the children (inputs)
        #Get only the non-modparam children
        children = node.children() if len(node.modparams)==0 else list(node.children())[:-len(node.modparams)]
        for port, child in zip(inst_inputs, children):
            if type(node).node_name == "coreir_reg" and port == "in0":
                port = "in"
            child_inst = self.node_to_inst[child]
            if child_inst is not None:
                self.def_.connect(child_inst, select(inst, port))
            else:
                coreir.connect_const(select(inst, port), 0)

        self.node_to_inst[node] = inst

    #The issue is that output is visited first then the source, then the sink. Depth first vs breadth first.

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)

        _, outputs = parse_rtype(self.def_.module.type)
        io = self.def_.interface
        # Wire all the children (inputs)
        for port, child in zip(outputs.keys(), node.children()):
            child_inst = self.node_to_inst[child]
            if child_inst is not None:
                self.def_.connect(child_inst, select(io, port))

    #I want to solve this for a generic Source/Sink Pair and not special case to registers
    #CoreIR Registers have modparams. These are gotten from the Sink part of the pair.



class VerifyUniqueIname(Visitor):
    def __init__(self):
        self.inames = {}

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        if node.iname in self.inames:
            raise ValueError(f"{node.iname} for {node} already used by {self.inames[node.iname]}")
        self.inames[node.iname] = node

    def visit_Source(self, node):
        pass

# Magma compiles output ports into either "O" for single outputs or "O0", "O1" etc for multi-output
# This pass replaces non-input selects to the better name
class FixSelects(Transformer):
    def __init__(self, nodes):
        self.field_map = {}
        self.nodes = nodes
        for node_name in nodes._node_names:
            peak_fc = nodes.peak_nodes[node_name]
            dag_node = nodes.dag_nodes[node_name]
            cmod = nodes.coreir_modules[node_name]
            _, c_outputs = parse_rtype(cmod.type)
            c_output_keys = list(c_outputs.keys())
            if nodes.is_stateful(node_name):
                dag_node = dag_node[0] #Use the source
            assert issubclass(dag_node, DagNode), f"{dag_node}"
            peak_outputs = list(peak_fc(fam().PyFamily()).output_t.field_dict.keys())
            #print("p",peak_outputs)
            #print("c", c_outputs)
            assert len(peak_outputs) == len(c_output_keys)
            self.field_map[dag_node] = {name: c_output_keys[i] for i, name in enumerate(peak_outputs)}
            #if len(peak_outputs) == 1:
            #    self.field_map[dag_node] = {peak_outputs[0]: }
            #else:
            #    self.field_map[dag_node] = {name: f"O{i}" for i, name in enumerate(peak_outputs)}

    def visit_Select(self, node):
        Transformer.generic_visit(self, node)
        child : DagNode = node.children()[0]
        if isinstance(child, (Source, Combine, Select)):
            return None
        assert type(child) in self.field_map, str(child)
        replace_field = fix_keyword(self.field_map[type(child)][node.field])
        return child.select(replace_field, original=node.field)

        # Create a map from field to coreir field

#This will construct a new coreir module from the dag with ref_type
def dag_to_coreir_def(nodes: Nodes, dag: Dag, ref_mod: coreir.Module, name: str) -> coreir.ModuleDef:
    VerifyUniqueIname().run(dag)
    FixSelects(nodes).run(dag)
    #remove everything from old definition
    mod = CoreIRContext(False).global_namespace.new_module(name, ref_mod.type)
    def_ = mod.new_definition()
    ToCoreir(nodes, def_).run(dag)
    mod.definition = def_
    return mod

#This will construct a new coreir module from the dag with ref_type
def dag_to_coreir(nodes: Nodes, dag: Dag, name: str) -> coreir.ModuleDef:
    VerifyUniqueIname().run(dag)
    FixSelects(nodes).run(dag)
    c = CoreIRContext()
    #construct coreir type
    inputs = {field:c.Flip(adt_to_ctype(T)) for field, T in dag.input.type.field_dict.items() if field != "__fake__"}
    outputs = {field:adt_to_ctype(T) for field, T in dag.output.type.field_dict.items()}
    type = CoreIRContext().Record({**inputs, **outputs})
    mod = CoreIRContext().global_namespace.new_module(name, type)
    def_ = mod.new_definition()
    ToCoreir(nodes, def_).run(dag)
    mod.definition = def_
    return mod
