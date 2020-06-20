import peak
from peak.assembler import Assembler
from peak import family
from .node import Nodes, DagNode, Dag, Input, Output
import coreir
import magma

def peak_to_dag(nodes: Nodes, peak_fc):
    # Two cases:
    # 1) Either peak_fc will already be a single node in nodes, so just need to simply wrap it
    # 2) peak_fc needs to be compiled into a coreir module where each instance within the module should correspond to a node in Nodes
    node_name = nodes.name_from_peak(peak_fc)

    #case 2
    if node_name is None:
        raise NotImplementedError
        cmod = peak_to_coreir(peak_fc)
        return coreir_to_dag(cmod, nodes)

    #case 1

    #Get input/output names from peak_cls
    peak_bv = peak_fc(family.PyFamily())
    input_fields = list(peak_bv.input_t.field_dict.keys())
    output_fields = list(peak_bv.output_t.field_dict.keys())

    input = Input(iname="self")
    children = [input.select(field) for field in input_fields]
    node_t = nodes.dag_nodes[node_name]
    assert issubclass(node_t, DagNode)
    node = node_t(*children)
    output_children = [node.select(field) for field in output_fields]
    output = Output(*output_children)
    dag = Dag([input], [output])
    return dag

import tempfile
def magma_to_coreir(mod):
    f = tempfile.NamedTemporaryFile(delete=False)
    magma.compile(f.name, mod, output="coreir")
    cname = mod.coreir_name
    backend = magma.frontend.coreir_.GetCoreIRBackend()
    #backend.compile(mod)
    return backend.modules[cname]

def peak_to_coreir(peak_fc, wrap=False) -> coreir.Module:
    peak_m = peak_fc(family.MagmaFamily())
    assert wrap
    if wrap:
        class HashableDict(dict):
            def __hash__(self):
                return hash(tuple(sorted(self.keys())))

        #TODO Better way to get the first port name?
        instr_name = list(peak_m.interface.items())[0][0]

        peak_bv = peak_fc(family.PyFamily())
        instr_type = peak_bv.input_t.field_dict[instr_name]
        asm = Assembler(instr_type)
        instr_magma_type = type(peak_m.interface.ports[instr_name])
        peak_m = peak.wrap_with_disassembler(
            peak_m,
            asm.disassemble,
            asm.width,
            HashableDict(asm.layout),
            instr_magma_type,
            wrapped_name= "Wrapped"+peak_m.name
            #wrapped_name = "WrappedPE"
        )

    #TODO This  compilation is sometimes cached.
    cmod = magma_to_coreir(peak_m)
    return cmod

#TODO I need a way to go from a Dag to a single Peak class
def dag_to_peak(nodes: Nodes, dag: Dag):
    raise NotImplementedError("TODO")
    pass

# Creates a new DagNode based off a peak class.
def peak_to_node(nodes: Nodes, peak_fc, stateful, name=None) -> (DagNode, str):
    if stateful:
        raise NotImplementedError("TODO")

    #Create DagNode
    peak_bv = peak_fc(family.PyFamily())

    inputs = list(peak_bv.input_t.field_dict.keys())

    outputs = list(peak_bv.output_t.field_dict.keys())
    if name is None:
        name = peak_bv.__name__
    return nodes.create_dag_node(name, len(inputs), stateful=False), name

def load_from_peak(nodes: Nodes, peak_fc, stateful=False, cmod=None, name=None) -> str:
    if cmod is None:
        cmod = peak_to_coreir(peak_fc, wrap=True)
    dag_node, node_name = peak_to_node(nodes, peak_fc, stateful=stateful, name=name)
    nodes.add(node_name, peak_fc, cmod, dag_node)
    return node_name
