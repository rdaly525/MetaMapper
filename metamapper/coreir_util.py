import coreir
from .visitor import Visitor
from .node import DagNode, Dag
from functools import wraps
import abc
from collections import OrderedDict
from .node import Nodes, Input, Output
from . import CoreIRContext
import typing as tp

#returns input objects and output objects
def parse_rtype(rtype) -> tp.Mapping[str, coreir.Type]:
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


#TODO this is really just coreir module to a dag where the instances in the coreir are nodes in nodes
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

        source_nodes = [Input(iname="self")]
        stateful_instances = [cmod.definition.interface]
        # load up node_map with source nodes
        for source, inst in zip(source_nodes, stateful_instances):
            self.node_map[inst] = source

        #for n, t in inputs.items():
        #    inode = Input(idx=n)
        #    self.node_map[("self", n)] = inode
        #    input_nodes.append(inode)

        #for n, t in outputs.items():
        #    onode = self.add_output(n)
        #    self.node_map[("self", n)] = onode
        #    output_nodes.append(onode)

        #create all the sinks
        sink_nodes = []
        for source, inst in zip(source_nodes, stateful_instances):
            sink_t = type(source).sink_t
            sink_node = self.add_node(inst, sink_t=sink_t)
            assert isinstance(sink_node, DagNode)
            sink_nodes.append(sink_node)
        print(1,sink_nodes)
        self.dag = Dag(source_nodes, sink_nodes)

    def add_node(self, inst: coreir.Instance, sink_t=None):
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

        #interface has no modparams
        if inst is self.cmod.definition.interface:
            modparams = {}
            iname = "self"
        else:
            modparams = {k: v.value for k, v in inst.config.items()}
            iname = inst.name
        node = node_t(*children, iname=iname, **modparams)
        if sink_t is None:
            self.node_map[inst] = node
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
def load_from_json(file, libraries=[]):
    c = CoreIRContext()
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
