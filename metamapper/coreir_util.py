import coreir
from .visitor import Visited, Dag, Visitor
from .node import DagNode
from functools import wraps
import abc
from enum import Enum
from collections import OrderedDict
from .irs.coreir import gen_CoreIRNodes
from .node import Nodes, Input, Output
from . import CoreIRContext
import typing as tp

#returns input objects and output objects
def parse_rtype(rtype):
    assert isinstance(rtype, coreir.Record)
    inputs = OrderedDict()
    outputs = OrderedDict()
    for n, t in rtype.items():
        if t.is_input():
            inputs[n] = t
        elif t.is_output():
            outputs[n] = t
        else:
            raise ValueError("Bad io type!")

    return inputs, outputs

def get_driver(port) -> ("iname", "port"):
    conns = port.connected_wireables
    assert len(conns) == 1, f"{len(conns)}, {port}"
    driver = conns[0]
    dpath = driver.selectpath
    assert len(dpath) == 2
    return dpath[0], dpath[1]

#TODO this is really just coreir module to a dag where the instances in the coreir are nodes in nodes
class Loader:
    def __init__(self, mod, nodes: Nodes):
        self.mod = mod
        self.nodes = nodes
        self.c = mod.context
        self.node_map: tp.Mapping["inst", DagNode] = {}
        inputs, outputs = parse_rtype(mod.type)

        #Create all input nodes first
        input_nodes = []
        for n, t in inputs.items():
            #TODO verify t is a good type
            inode = Input(idx=n)
            self.node_map[("self", n)] = inode
            input_nodes.append(inode)

        output_nodes = []
        for n, t in outputs.items():
            onode = self.add_output(n)
            self.node_map[("self", n)] = onode
            output_nodes.append(onode)
        self.dag = Dag(output_nodes, input_nodes)

    def add_output(self, port_name):
        io = self.mod.definition.interface
        iname, iport = get_driver(io.select(port_name))
        driver = self.add_node(iname, iport)
        return Output(driver, idx=port_name)

    def add_node(self, iname, iport):
        if iname == "self":
            key = (iname, iport)
            assert key in self.node_map
            return self.node_map[key]
        if iname in self.node_map:
            return self.node_map[iname]
        inst = self.mod.definition.get_instance(iname)
        inputs, outputs = parse_rtype(inst.module.type)
        #iport should be the first and only output (for now)
        assert len(outputs)==1
        assert iport in outputs
        children = []
        for port, t in inputs.items():
            dname, dport = get_driver(inst.select(port))
            driver = self.add_node(dname, dport)
            children.append(driver)

        node_name = self.nodes.name_from_coreir(inst.module)
        if node_name is None:
            raise ValueError(f"coreir module {inst.module.name} missing from {self.nodes}")
        NodeKind = self.nodes.dag_nodes[node_name]
        node = NodeKind(*children, iname=iname)

        self.node_map[iname] = node
        return node

def coreir_to_dag(nodes: Nodes, cmod):
    return Loader(cmod, nodes).dag

#returns module, and map from instances to dags
def load_from_json(c, file, libraries=[]):
    for lib in libraries:
        c.load_library("lib")
    cmod = c.load_from_file(file)
    return cmod

def preprocess(CoreIRNodes: Nodes, cmod: coreir.Module) -> tp.Mapping[coreir.Instance, Dag]:
    #First inline all commonlib instances (rungenerators for commonlib first)
    #TODO

    c = cmod.context
    #Run isolate_primitives pass
    c.run_passes(["isolate_primitives"])
    #Find all instances of modules which need to be mapped (All the _.*primitives) modules
    primitive_blocks = []
    assert cmod.definition
    for inst in cmod.definition.instances:
        ns_name = inst.module.namespace.name
        if ns_name == "_":
            primitive_blocks.append(inst)

    #dagify all the primitive_blocks
    pb_dags = {inst:coreir_to_dag(CoreIRNodes, inst.module) for inst in primitive_blocks}
    return pb_dags

class ToCoreir(Visitor):
    def __init__(self, nodes: Nodes, def_: coreir.ModuleDef, dag: Dag):
        self.coreir_const = CoreIRContext().get_namespace("coreir").generators["const"]
        self.nodes = nodes
        self.def_ = def_
        self.node_to_inst = {}  # inst is really the output port of the instance
        super().__init__(dag)

    def visit_Input(self, node):
        self.node_to_inst[node] = self.def_.interface.select(node.idx)

    def visit_Constant(self, node):
        bv_val = node.value
        iname ="c"+str(id(node))
        const_mod = self.coreir_const(width=bv_val.size)
        config = CoreIRContext().new_values(fields=dict(value=bv_val))
        inst = self.def_.add_module_instance(iname, const_mod, config=config)
        self.node_to_inst[node] = inst.select("out")

    def generic_visit(self, node):
        Visitor.generic_visit(self, node)
        # create new instance
        node_kind = type(node).__name__
        Module = self.nodes.coreir_modules[node_kind]

        #TODO what if this has modparams?
        inst = self.def_.add_module_instance(node.iname, Module)

        # Wire all the children (inputs)
        for port, child in zip(node.input_names(), node.children()):
            child_inst = self.node_to_inst[child]
            self.def_.connect(child_inst, inst.select(port))

        # TODO assuming single output
        oport = node.coreir_output_name(0)
        self.node_to_inst[node] = inst.select(oport)

        # CLK and ASYNC?
        #inst.ASYNCRESET @= self.io.RESET

    def visit_Output(self, node):
        Visitor.generic_visit(self, node)
        child_inst = self.node_to_inst[node.inputs()[0]]
        output_port = node.idx
        self.def_.connect(child_inst, self.def_.interface.select(output_port))

#This will construct a coreir module from the dag with ref_type
def dag_to_coreir_def(nodes: Nodes, dag: Dag, ref_mod: coreir.Module) -> coreir.ModuleDef:
    inputs, outputs = parse_rtype(ref_mod.type)

    #Verify that the dag nodes match the reference type
    for i, (p, T) in enumerate(inputs.items()):
        assert dag.inputs[i].idx == p

    for i, (p, T) in enumerate(outputs.items()):
        assert dag.outputs[i].idx == p
    def_ = ref_mod.new_definition()
    ToCoreir(nodes, def_, dag)
    return def_
