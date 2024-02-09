import coreir
from DagVisitor import Visitor, Transformer
from collections import OrderedDict
from .node import DagNode, Dag, Nodes, Source, Sink, Input, InstanceInput, Combine, Constant, Select, RegisterSource, RegisterSink
from . import CoreIRContext
import typing as tp
from .family import fam
from peak.mapper import Unbound
from peak.assembler import AssembledADT, Assembler, AssembledADTRecursor
from .common_passes import print_dag, Clone
from hwtypes.adt import Product, Enum, Tuple
import os
import keyword
from hwtypes.adt import Product
import hwtypes as ht
from hwtypes import BitVector, Bit
from hwtypes.modifiers import strip_modifiers, is_modified
from peak import Peak, name_outputs, family_closure, Const
from peak.family import AbstractFamily

def create_bv_const(width, value):
    bv = ht.BitVector[width]
    return Constant(type=bv, value=bv(value))

def create_bit_const(value):
    return Constant(type=ht.Bit, value=ht.Bit(value))

def is_const(cmod: coreir.Module):
    namespace, name = cmod.ref_name.split(".")

    return namespace in ["coreir", "corebit"] and name == "const"

def is_reg(cmod: coreir.Module):
    return cmod.ref_name.split(".")[1] =="reg"


#There is a hack where names aliasing with python keywords need to get remapped
#Use this function to select into coreir instances
def select(inst, name):
    if isinstance(name, int):
        name = str(name)
    if len(name) > 3 and name[-3:]=="___":
        name = name[:-3]
    return inst.select(name)




def fix_keyword_from_coreir(val:str):
    if val.isdigit():
        return int(val)
    if val in keyword.kwlist:
        return val + "___"
    return val

def fix_keyword_to_coreir(val:str):
    if val[-3:] == "___":
        return val[:-3]
    return val

#returns input objects and output objects
#removes clk and reset
def parse_rtype(rtype) -> tp.Mapping[str, coreir.Type]:
    assert isinstance(rtype, coreir.Record)
    inputs = OrderedDict()
    outputs = OrderedDict()
    for n, t in rtype.items():
        n = fix_keyword_from_coreir(n)
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


#coreir.const/corebit.const translates to a Constant node
#coreir.reg/corebit.reg translates to a Registers

class Loader:
    def __init__(self, cmod: coreir.Module, nodes: Nodes, allow_unknown_instances=False):
        if allow_unknown_instances:
            raise NotImplementedError()
        self.cmod = cmod
        self.nodes = nodes
        self.c = cmod.context
        self.node_map: tp.Mapping[coreir.Instance, str] = {}
        self.const_cache = {}
        self.unqiue = 0

        inputs, outputs = parse_rtype(cmod.type)
        input_adt = fields_to_adt(inputs, "Input")
        output_adt = fields_to_adt(outputs, "Output")

        source_nodes = [Input(iname="self", type=input_adt)]
        self.node_map[cmod.definition.interface] = source_nodes[0]

        #reg_nodes = []
        stateful_instances = {cmod.definition.interface: output_adt}
        #Sort into non-stateful nodes (Do nothing), stateful nodes, and registers
        for inst in cmod.definition.instances:

            if is_const(inst.module):
                continue
            if is_reg(inst.module):
                adt = fields_to_adt(parse_rtype(inst.module.type)[1], "_sink")
                in_type = adt["out"]
                assert issubclass(in_type, (ht.BitVector, ht.Bit))
                node = RegisterSource(iname=inst.name, type=in_type)
                source_nodes.append(node)
                stateful_instances[inst] = in_type
                self.node_map[inst] = node
                continue

            node_name = self.nodes.name_from_coreir(inst.module)
            if node_name is None:
                print(self.nodes.coreir_modules[f'{inst.module.namespace.name}.{inst.module.name}'].print_())
                print(inst.module.print_())
                raise ValueError(f"Unknown module {inst.module.name}")

            if not self.nodes.is_stateful(node_name):
                continue
            #Absolutely stateful
            source_node_t, _ = self.nodes.dag_nodes[node_name]
            inputs, outputs = parse_rtype(inst.module.type)
            sink_adt = fields_to_adt(inputs, f"{inst.name}_sink")
            source_adt = fields_to_adt(outputs, f"{inst.name}_source")
            node = source_node_t(iname=inst.name, type=source_adt)
            source_nodes.append(node)
            stateful_instances[inst] = sink_adt
            self.node_map[inst] = node

        #create all the non-register sinks
        sink_nodes = []
        for source, (inst, sink_adt) in zip(source_nodes, stateful_instances.items()):
            sink_t = type(source).sink_t
            sink_node = self.add_node(inst, sink_t=sink_t, sink_adt=sink_adt)

            assert isinstance(sink_node, DagNode)
            sink_nodes.append(sink_node)

        self.dag = Dag(source_nodes, sink_nodes)
        #print_dag(self.dag)

    def add_const(self, inst: coreir.Instance):
        if inst in self.const_cache:
            return self.const_cache[inst]
        mref = inst.module

        if mref.ref_name == "coreir.const":
            width = mref.generator_args["width"].value
            value = inst.config["value"].value
            
            const_node = create_bv_const(width, value)
        elif mref.ref_name == "corebit.const":
            value = inst.config["value"].value
            const_node =  create_bit_const(value)
        else:
            return None

        self.const_cache[inst] = const_node
        return const_node

    #Cases
    # 1) Const: ignore sink_t and sink_adt
    # 2) Reg: ??
    # 3) Comb instance: ??
    # 4) Stateful Module: sink_t and sink_adt valid
    def add_node(self, inst: coreir.Instance, sink_t=None, sink_adt=None):
        if is_const(inst.module):
            return self.add_const(inst)

        #if node already exists
        if sink_t is None and inst in self.node_map:
            return self.node_map[inst]

        #If not a sink
        if sink_t is None:
            node_name = self.nodes.name_from_coreir(inst.module)
            node_t = self.nodes.dag_nodes[node_name]
            assert issubclass(node_t, DagNode)
        else:
            node_t = sink_t

        # Translates Coreir selectpath into node selectpath
        #def csp_to_nsp(node: DagNode, csp: tuple):
        #    cmod = node.nodes.coreir_modules[node.node_name]
        def type_recurse(w):
            children = []
            #Depth first traversal. adding child nodes before self.
            for driver in self.get_drivers(w):
                if isinstance(driver, tuple):
                    (child_inst, sel_path) = driver
                    #Either a driver has a child or not
                    #This should be two distinct cases:
                    #   a) When there literally is nothing connected (None)
                    #   b) When there are things connected at a different level of hierarchy (wireable)
                    #   c) at leaf type with normal connection (other_inst, ports)
                    if (child_inst, sel_path) == (None, None):
                        children.append(Constant(value=Unbound, type=ht.Bit))
                        #pass
                    else:
                        child_node = self.add_node(child_inst)
                        if isinstance(child_node, Constant):
                            children.append(child_node)
                        else:
                            child = child_node
                            #ROSS TODO
                            ##sel_path = child_node._nodes_.csp_to_asp(sel_path)
                            for sel in sel_path:
                                sel = fix_keyword_from_coreir(sel)
                                if sel == "z":
                                    sel = "out"
                                child = child.select(sel)
                            children.append(child)
                else:
                    sub_w: coreir.Wireable = driver
                    if len(sub_w.connected_wireables) > 0:
                        raise NotImplementedError()
                    assert sub_w.type.kind == "Array"
                    children.append(type_recurse(sub_w))

            if isinstance(w, coreir.Select):
                adt = ctype_to_adt(w.type)
                self.unique += 1
                return Combine(*children, iname=f"UC{self.unique}", type=adt)
                

            # inst is named w in this function
            inst = w
            if w is self.cmod.definition.interface:
                node = node_t(*children, iname="self", type=sink_adt)
                return node

            #Definitaly an instance. Need to create a node
            assert isinstance(w, coreir.Instance)
            iname = inst.name
            def get_adt(inst, k):
                vtype = inst.module.params[k]
                if vtype.kind is bool:
                    return ht.Bit
                elif vtype.kind is ht.BitVector:
                    #TODO HACK assuming 16 bit constants always
                    return ht.BitVector[16]
                else:
                    raise NotImplementedError()

            if is_reg(inst.module):
                init = inst.config["init"]
                assert node_t is RegisterSink
                assert sink_adt is not None
                node = RegisterSink(*children, type=sink_adt)

            if inst.module.name == "rom2":
                node = node_t(*children, init=inst.config["init"], iname=iname)
            elif sink_t is None: #Normal instance
                node = node_t(*children, iname=iname)
                self.node_map[inst] = node
            else: #stateful instance
                node = node_t(*children, iname=iname, type=sink_adt)
            return node

        inst_node = type_recurse(inst)
        if isinstance(inst, coreir.Instance):
            md = inst.metadata
            if len(md) > 0:
                inst_node.add_metadata(md)

        return inst_node

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

    #YOu need to write code that traverses the type hierarchy via wires. Add the API to loop through the selects

    #returns a list of either (driver_inst, driver_ports) OR (selected_wireable)
    def get_drivers(self, w: tp.Union[coreir.Instance, coreir.Interface, coreir.Wireable]) -> tp.List[tp.Tuple[coreir.Instance, str]]:

        if w is self.cmod.definition.interface:
            _, inputs = parse_rtype(self.cmod.type)
        elif isinstance(w, coreir.Instance):
            inputs, _ = parse_rtype(w.module.type)
        else:
            #Assume that w is an array type
            t = w.type
            assert t.kind == "Array"
            inputs = {i:t.element_type for i in range(len(t))}


        drivers = []
        def is_bv(t: coreir.Type):
            if t.kind == "Bit" or t.kind == "BitIn":
                return True
            elif t.kind == "Array":
                elem_t = t.element_type
                if elem_t.kind == "Bit" or elem_t.kind == "BitIn":
                    return True
                else:
                    return False
            else:
                raise NotImplementedError(t.kind)
        for port_name, t in inputs.items():
            if port_name == "rnd":
                continue
            bv = is_bv(t)
            port = select(w, port_name)
            if bv: #Leaf
                conns = port.connected_wireables
                if len(conns) == 0:
                    drivers.append((None, None))
                else:
                    assert len(conns) == 1, f"{len(conns)}, {port}"
                    driver = conns[0]
                    dpath = driver.selectpath
                    driver_iname, driver_ports = dpath[0], dpath[1:]
                    driver_inst = self.inst_from_name(driver_iname)
                    if is_reg(driver_inst.module):
                        driver_ports = ()
                    drivers.append((driver_inst, driver_ports))
            else: #Array
                drivers.append(port)
        return drivers


@family_closure
def rom_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    Bit = family.Bit
    class rom(Peak):
        @name_outputs(rdata=Data)
        def __call__(self, raddr: Data, ren: Bit) -> Data:
            return Data(0)
    return rom

def gen_rom(CoreIRNodes):
    class Rom(DagNode):
        def __init__(self, raddr, ren, *, init, iname):
            super().__init__(raddr, ren, init=init, iname=iname)
            self.modparams=()

        @property
        def attributes(self):
            return ("init", "iname")

        #Hack to get correct port name
        def select(self, field, original=None):
            self._selects.add("rdata")
            return Select(self, field="rdata",type=BitVector[16])

        nodes = CoreIRNodes
        static_attributes = {}
        node_name = "memory.rom2"
        num_children = 2
        type = Product.from_fields("Output",{"rdata":BitVector[16]})
    return Rom


#Takes in a coreir module and translates it into a dag
# inline=True means to find instances of modules not defined in 'nodes' and inline them
# If they are not inlineable then raise an error
def coreir_to_dag(nodes: Nodes, cmod: coreir.Module, inline=True, archnodes=None) -> Dag:

    c = cmod.context
    assert cmod.definition
    if inline:
        for _ in range(10):
            to_inline = []
            for inst in cmod.definition.instances:
                if inst.module.name == "rom2":
                    if 'memory.rom2' not in nodes.coreir_modules:
                        CoreIRNodes = nodes
                        depth = inst.module.generator_args['depth'].value
                        width = inst.module.generator_args['width'].value
                        rom2 = c.get_namespace("memory").generators["rom2"](depth=depth, width=width)
                        Rom = gen_rom(CoreIRNodes)
                        CoreIRNodes.add("memory.rom2", rom_fc, rom2, Rom)
                        mr = "memory.rom2"
                        archnodes.add(mr, CoreIRNodes.peak_nodes[mr], CoreIRNodes.coreir_modules[mr], CoreIRNodes.dag_nodes[mr])
                    continue
                if is_const(inst.module) or is_reg(inst.module):
                    continue
                node_name = nodes.name_from_coreir(inst.module)
                
                # print(inst.module.name, node_name)
                if node_name is None:
                    to_inline.append(inst)
            for inst in to_inline:
                coreir.inline_instance(inst)
    return Loader(cmod, nodes, allow_unknown_instances=False).dag

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


class ToCoreir(Visitor):
    def __init__(self, nodes: Nodes, def_: coreir.ModuleDef, convert_unbounds=True):
        self.coreir_const = CoreIRContext().get_namespace("coreir").generators["const"]
        self.coreir_bit_const = CoreIRContext().get_namespace("corebit").modules["const"]
        self.nodes = nodes
        self.def_ = def_
        self.node_to_inst: tp.Mapping[DagNode, coreir.Wireable] = {}  # inst is really the output port of the instance
        self.convert_unbounds=convert_unbounds
        self.unique_name = 0

    def doit(self, dag: Dag):
        #Create all the instances for the Source/Sinks first
        for sink in list(dag.roots())[1:]:
            inst = self.create_instance(sink)
            self.node_to_inst[sink] = inst
            if isinstance(sink, RegisterSink):
                self.node_to_inst[sink.source] = inst.select("out")
            else:
                self.node_to_inst[sink.source] = inst

        self.run(dag)

    def visit_Select(self, node):
        Visitor.generic_visit(self, node)
        child_inst = self.node_to_inst[node.children()[0]]
        self.node_to_inst[node] = select(child_inst, node.field)

    def visit_Input(self, node):
        self.node_to_inst[node] = self.def_.interface

    def visit_Source(self, node):
        if node.sink not in self.node_to_inst:
            raise ValueError()
        self.node_to_inst[node] = self.node_to_inst[node.sink]

    def visit_RegisterSource(self, node):
        if node.sink not in self.node_to_inst:
            raise ValueError()
        self.node_to_inst[node] = self.node_to_inst[node.sink].select("out")


    def visit_Constant(self, node):
        assert isinstance(node, Constant)
        bv_val = node.value
        if bv_val is Unbound:
            self.node_to_inst[node] = None
            return
        is_bool = type(bv_val) is ht.Bit or isinstance(bv_val, bool)
        if is_bool:
            const_mod = self.coreir_bit_const
            bv_val = bool(bv_val)
        else:
            const_mod = self.coreir_const(width=bv_val.size)
        config = CoreIRContext().new_values(fields=dict(value=bv_val))
        iname = "c" + str(self.unique_name)
        self.unique_name += 1
        inst = self.def_.add_module_instance(iname, const_mod, config=config)
        self.node_to_inst[node] = inst.select("out")

    def visit_Combine(self, node: Combine):
        if node.tu_field is not None:
            raise NotImplementedError("Sum types")
        Visitor.generic_visit(self, node)
        child_insts = [self.node_to_inst[child] for child in node.children()]
        assert len(child_insts) == len(node.type.field_dict)
        self.node_to_inst[node] = [(field, child_inst) for field, child_inst in zip(node.type.field_dict.keys(), child_insts)]

    def get_coreir_reg(self, t):
        c = CoreIRContext()
        if t is ht.Bit:
            reg_mod = c.get_namespace("corebit").modules["reg"]
        elif issubclass(t, ht.BitVector):
            width = t.size
            reg_mod = c.get_namespace("coreir").generators["reg"](width=width)
        else:
            raise NotImplementedError(t)
        return reg_mod

    def visit_PipelineRegister(self, node):
        Visitor.generic_visit(self, node)
        reg_mod = self.get_coreir_reg(node.type)
        inst = self.def_.add_module_instance(node.iname, reg_mod)
        self.def_.connect(inst.select("in"), self.node_to_inst[node.child])
        self.node_to_inst[node] = inst.select("out")


    def create_instance(self, node):
        if node in self.node_to_inst:
            return self.node_to_inst[node]

        if isinstance(node, RegisterSink):
            cmod_t = self.get_coreir_reg(node.type)
            config = CoreIRContext().new_values(fields={"init":node.type(0)})
            inst = self.def_.add_module_instance(node.iname, cmod_t, config=config)
        else:
            cmod_t = self.nodes.coreir_modules[type(node).node_name]
            inst = self.def_.add_module_instance(node.iname, cmod_t)
        return inst

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        if type(node).node_name == "memory.rom2":
            rom_mod = self.nodes.coreir_modules["memory.rom2"]
            config = CoreIRContext().new_values(dict(init=node.init))
            inst = self.def_.add_module_instance(node.iname, rom_mod, config=config)
        elif type(node).node_name == "memory.fprom2":
            rom_mod = self.nodes.coreir_modules["memory.fprom2"]
            config = CoreIRContext().new_values(dict(init=node.init))
            inst = self.def_.add_module_instance(node.iname, rom_mod, config=config)
        else:
            inst = self.create_instance(node)
        inst_inputs = list(self.nodes.peak_nodes[node.node_name].Py.input_t.field_dict.keys())
        # Wire all the children (inputs)
        #Get only the non-modparam children
        children = node.children() if len(node.modparams)==0 else list(node.children())[:-len(node.modparams)]
        for port, child in zip(inst_inputs, children):
            child_inst = self.node_to_inst[child]
            if child_inst is not None:
                self.def_.connect(child_inst, select(inst, port))
            elif self.convert_unbounds:
                coreir.connect_const(select(inst, port), 0)

        self.node_to_inst[node] = inst

    #The issue is that output is visited first then the source, then the sink. Depth first vs breadth first.
    def visit_RegisterSink(self, node):
        Visitor.generic_visit(self, node)
        reg_inst = self.node_to_inst[node]
        child_inst = self.node_to_inst[node.child]
        self.def_.connect(reg_inst.select("in"), child_inst)

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)

        _, outputs = parse_rtype(self.def_.module.type)
        io = self.def_.interface
        # Wire all the children (inputs)
        def recurse(input_sel: coreir.Wireable, other):
            if other is None: #Unconnected input
                return
            elif isinstance(other, coreir.Wireable):
                other_inst = self.def_.get_instance(other.selectpath[0])
                self.def_.connect(other, input_sel)
            elif isinstance(other, list):
                for field, sub_other in other:
                    recurse(select(input_sel, field), sub_other)
            else:
                raise ValueError()
        for port, child in zip(outputs.keys(), node.children()):
            input_sel = select(io, port)
            child_inst = self.node_to_inst[child]
            recurse(input_sel, child_inst)


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
            if cmod == None:
                continue
            _, c_outputs = parse_rtype(cmod.type)
            c_output_keys = list(c_outputs.keys())
            if nodes.is_stateful(node_name):
                dag_node = dag_node[0] #Use the source
            assert issubclass(dag_node, DagNode), f"{dag_node}"
            peak_outputs = list(peak_fc(fam().PyFamily()).output_t.field_dict.keys())
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
        replace_field = fix_keyword_from_coreir(self.field_map[type(child)][node.field])
        return child.select(replace_field, original=node.field)
        # Create a map from field to coreir field

#This will construct a new coreir module from the dag with ref_type
def dag_to_coreir_def(nodes: Nodes, dag: Dag, mod: coreir.Module, convert_unbounds=True) -> coreir.ModuleDef:
    dag = Clone().clone(dag)
    VerifyUniqueIname().run(dag)
    FixSelects(nodes).run(dag)
    #remove everything from old definition
    #mod = CoreIRContext(False).global_namespace.new_module(name, ref_mod.type)
    def_ = mod.new_definition()
    ToCoreir(nodes, def_, convert_unbounds=convert_unbounds).doit(dag)
    mod.definition = def_
    return mod

#This will construct a new coreir module from the dag with ref_type
def dag_to_coreir(nodes: Nodes, dag: Dag, name: str, convert_unbounds=True) -> coreir.ModuleDef:
    dag = Clone().clone(dag)
    VerifyUniqueIname().run(dag)
    #print_dag(dag)
    FixSelects(nodes).run(dag)
    c = CoreIRContext()
    #construct coreir type
    inputs = {fix_keyword_to_coreir(field):c.Flip(adt_to_ctype(T)) for field, T in dag.input.type.field_dict.items() if field != "__fake__"}
    outputs = {fix_keyword_to_coreir(field):adt_to_ctype(T) for field, T in dag.output.type.field_dict.items()}
    type = CoreIRContext().Record({**inputs, **outputs})
    mod = CoreIRContext().global_namespace.new_module(name, type)
    def_ = mod.new_definition()
    ToCoreir(nodes, def_, convert_unbounds=convert_unbounds).doit(dag)
    mod.definition = def_
    return mod
