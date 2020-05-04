import peak
from peak.assembler import Assembler
from peak import family
from peak.mapper import RewriteRule as PeakRule
from hwtypes import Bit
from .node import Nodes, DagNode
from .visitor import Dag
import coreir

#I basically have the cross product of translating between (dag, node, peak, coreir)

#Wraps this node as a Dag.
def node_to_dag(node: DagNode, rr=None):
    if rr is None:
        raise NotImplementedError("Just want a pure wrapping")
    tile_inputs = [None for _ in range(from_node.num_inputs())]
    rep_inputs = [None for _ in range(to_node.num_inputs())]
    rep_dag_inputs = []
    for ib, ab in peak_rr.ibinding:
        assert isinstance(ab, tuple), "NYI"
        assert len(ab) == 1, "NYI"
        ab_idx = to_node.input_names().index(ab[0])
        if isinstance(ib, tuple):
            assert len(ib)==1, "NYI"
            ib_idx = from_node.input_names().index(ib[0])
            node = Input(idx=ib_idx)
            tile_inputs[ib_idx] = node
            rep_inputs[ab_idx] = node
        else:
            rep_inputs[ab_idx] = Constant(value=ib)

    assert all(node is not None and node.idx == i for (i, node) in enumerate(tile_inputs))
    assert all(node is not None for (i, node) in enumerate(rep_inputs))

    #create tile dag:
    tile_out = from_node(*tile_inputs, iname=0)
    tile_dag = Dag([tile_out], tile_inputs)
    rep_out = to_node(*rep_inputs)
    #the inputs are the same for both dags
    rep_dag = Dag([rep_out], tile_inputs)


def peak_to_dag(nodes: Nodes, peak_fc, **kwargs):
    if len(kwargs) > 0:
        raise NotImplementedError("Develop API for pasing in desired interfae + binding")
    # Two cases:
    # 1) Either peak_fc will already be a single node in nodes, so just need to simply wrap it
    # 2) peak_fc needs to be compiled into a coreir module where each instance within the module should correspond to a node in Nodes


    #case 1
    node_name = nodes.get_from_peak(peak_fc)
    if node_name is not None:
        return node_to_dag(nodes.dag_nodes[node_name])

    #case 2
    cmod = peak_to_coreir(peak_fc)
    return coreir_module_to_dag(cmod, nodes)



def magma_to_coreir(mod):
    backend = m.frontend.coreir_.GetCoreIRBackend(c)
    backend.compile(mod)
    cname = mod.coreir_name
    return backend.modules[cname]


def peak_to_coreir(peak_fc) -> coreir.Module:
    raise NotImplementedError("TODO")
    class HashableDict(dict):
        def __hash__(self):
            return hash(tuple(sorted(self.keys())))

    peak_m = peak_fc(family.MagmaFamily())

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



#TODO I need a way to go from a Dag to a single Peak class
def dag_to_peak(nodes: Nodes, dag: Dag):
    raise NotImplementedError("TODO")
    pass

#Creates a new DagNode based off a peak class. returns the name of the node
def peak_to_node(nodes: Nodes, peak_fc) -> "node_name":

    #Create CoreIR node
    cmod = peak_to_coreir(peak_fc)

    #Create DagNode
    io = peak_m.interface
    inputs = []
    outputs = []
    for p, T in io.items():
        if p in ("CLK", "ASYNCRESET"):
            continue
        if T.is_input():
            inputs.append(p)
        elif T.is_output():
            outputs.append(p)
        else:
            assert 0
    node_name = peak_bv.__name__
    dag_node = nodes.create_dag_node(node_name, inputs, outputs)
    nodes.add(node_name, dag_node, peak_fc, cmod)
    return node_name
