import peak
from peak.assembler import Assembler
from peak import family
from peak.mapper import RewriteRule as PeakRule
from hwtypes import Bit
from .node import Nodes, DagNode, Input
from .visitor import Dag
import coreir
import magma

#I basically have the cross product of translating between (dag, node, peak, coreir)

#Wraps this node as a Dag.
def node_to_dag(node: DagNode):

    inputs = [Input(idx=i) for i, name in enumerate(node.input_names())]
    #TODO what if node has multiple outputs?
    output = node(*inputs, iname=0)
    dag = Dag([output], inputs)
    return dag

def peak_to_dag(nodes: Nodes, peak_fc):
    # Two cases:
    # 1) Either peak_fc will already be a single node in nodes, so just need to simply wrap it
    # 2) peak_fc needs to be compiled into a coreir module where each instance within the module should correspond to a node in Nodes

    #case 1
    node_name = nodes.name_from_peak(peak_fc)
    if node_name is not None:
        return node_to_dag(nodes.dag_nodes[node_name])
    assert 0

    #case 2
    cmod = peak_to_coreir(peak_fc)
    return coreir_module_to_dag(cmod, nodes)

def magma_to_coreir(mod):
    backend = magma.frontend.coreir_.GetCoreIRBackend()
    backend.compile(mod)
    cname = mod.coreir_name
    return backend.modules[cname]

def peak_to_coreir(peak_fc, wrap=False) -> coreir.Module:
    peak_m = peak_fc(family.MagmaFamily())
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
            instr_magma_type
        )

    cmod = magma_to_coreir(peak_m)
    return cmod

#TODO I need a way to go from a Dag to a single Peak class
def dag_to_peak(nodes: Nodes, dag: Dag):
    raise NotImplementedError("TODO")
    pass

#Creates a new DagNode based off a peak class. returns the name of the node
def peak_to_node(nodes: Nodes, peak_fc) -> "node_name":

    #Create CoreIR node
    cmod = peak_to_coreir(peak_fc)

    #Create DagNode
    inputs = []
    outputs = []
    for p, T in cmod.type.items():
        if p in ("CLK", "ASYNCRESET"):
            continue
        if T.is_input():
            inputs.append(p)
        elif T.is_output():
            outputs.append(p)
        else:
            assert 0
    node_name = peak_fc(family.PyFamily()).__name__
    dag_node = nodes.create_dag_node(node_name, inputs, outputs, ('iname',))
    nodes.add(node_name, dag_node, peak_fc, cmod)
    return node_name
