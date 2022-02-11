import peak
from peak.assembler import Assembler
from peak import Const
from .family import fam
from .node import Nodes, DagNode, Dag, Input, Output, Select
from .common_passes import print_dag
import coreir
import magma
from . import CoreIRContext
from .coreir_util import coreir_to_dag
from DagVisitor import  Transformer, AbstractDag
from hwtypes.modifiers import strip_modifiers, is_modified


# A CoreIR Dag is compiled to remove any notion of constant inputs
#This will take in a dag compiled from a peak_fc.
# Will replace any selects of the inputs that should be const with a coreir.const (A little sketch if the constant is not a bitvector)
class FixConsts(Transformer):
    def __init__(self, peak_fc, nodes):
        input_t = peak_fc.Py.input_t
        self.const_fields = {}
        for field, T in input_t.field_dict.items():
            if issubclass(T, Const):
                self.const_fields[field] = strip_modifiers(T)
        self.nodes = nodes

    def visit_Select(self, node : Select):
        Transformer.generic_visit(self, node)
        if isinstance(node.children()[0], Input) and node.field in self.const_fields:

            T = self.const_fields[node.field]
            if T is fam().PyFamily().Bit:
                const_node = self.nodes.dag_nodes["corebit.const"]
            elif T is fam().PyFamily().BitVector[16]:
                const_node = self.nodes.dag_nodes["coreir.const"]
            else:
                raise ValueError(T)
            const = const_node(node)
            return const.select("out")

def flatten(cmod: coreir.Module):
    CoreIRContext().run_passes(["rungenerators"]) 
    d = cmod.definition
    #TODO change this to stop at a fixed point
    for i in range(4):
        for inst in d.instances:
            coreir.inline_instance(inst)



def peak_to_dag(nodes: Nodes, peak_fc, name=None):
    # Two cases:
    # 1) Either peak_fc will already be a single node in nodes, so just need to simply wrap it
    # 2) peak_fc needs to be compiled into a coreir module where each instance within the module should correspond to a node in Nodes
    node_name = nodes.name_from_peak(peak_fc, name)
    #case 2
    if node_name is None:
        cmod = peak_to_coreir(peak_fc)
        flatten(cmod)
        dag = coreir_to_dag(nodes, cmod)
        #print("pre-fix")
        #print_dag(dag)
        FixConsts(peak_fc, nodes).run(dag)
        # print("post-fix")
        # print_dag(dag)
        return dag

    #case 1

    #Get input/output names from peak_cls
    peak_bv = peak_fc(fam().PyFamily())
    input_fields = list(peak_bv.input_t.field_dict.keys())
    output_fields = list(peak_bv.output_t.field_dict.keys())

    input = Input(iname="self", type=strip_modifiers(peak_bv.input_t))
    children = [input.select(field) for field in input_fields]
    node_t = nodes.dag_nodes[node_name]
    assert issubclass(node_t, DagNode)
    node = node_t(*children)
    output_children = [node.select(field) for field in output_fields]
    output = Output(*output_children, type=peak_fc.Py.output_t)
    dag = Dag([input], [output])
    return dag

import tempfile
def magma_to_coreir(mod): 
    cname = mod.coreir_name
    f = tempfile.NamedTemporaryFile()
    magma.compile(f.name, mod, output="coreir")
    crt = magma.backend.coreir.coreir_runtime 

    return crt.module_map()[crt.coreir_context()]['global'][cname]

def peak_to_coreir(peak_fc, wrap=False) -> coreir.Module:
    peak_m = peak_fc(fam().MagmaFamily())

    if wrap:
        class HashableDict(dict):
            def __hash__(self):
                return hash(tuple(sorted(self.keys())))

        #TODO Better way to get the first port name?
        instr_name = list(peak_m.interface.items())[0][0]

        peak_bv = peak_fc(fam().PyFamily())
        instr_type = peak_bv.input_t.field_dict[instr_name]
        asm = Assembler(instr_type)
        instr_magma_type = type(peak_m.interface.ports[instr_name])
        peak_m = peak.wrap_with_disassembler(
            peak_m,
            asm.disassemble,
            asm.width,
            HashableDict(asm.layout),
            instr_magma_type,
            # wrapped_name= "Wrapped"+peak_m.name
            wrapped_name = "WrappedPE"
        )

    #TODO This  compilation is sometimes cached.
    cmod = magma_to_coreir(peak_m)
    return cmod

#TODO I need a way to go from a Dag to a single Peak class
def dag_to_peak(nodes: Nodes, dag: Dag):
    raise NotImplementedError("TODO")
    pass

# Creates a new DagNode based off a peak class.
def peak_to_node(nodes: Nodes, peak_fc, stateful, name=None, modparams=()) -> (DagNode, str):

    #Create DagNode
    peak_bv = peak_fc(fam().PyFamily())

    inputs = list(peak_bv.input_t.field_dict.keys())
    for i, param in enumerate(modparams):
        assert inputs[-len(modparams)+i] == param

    outputs = list(peak_bv.output_t.field_dict.keys())
    if name is None:
        name = peak_bv.__name__
    if stateful:
        static_attrs = dict(
            input_t = strip_modifiers(peak_bv.input_t),
            output_t = strip_modifiers(peak_bv.output_t),
        )
    else:
        static_attrs = dict(type=strip_modifiers(peak_bv.output_t))
    return nodes.create_dag_node(name, len(inputs), stateful=stateful, static_attrs=static_attrs, modparams=modparams), name

def check_ports(node: DagNode, cmod: coreir.Module):
    #TODO implement this function
    return True

def load_from_peak(nodes: Nodes, peak_fc, stateful=False, cmod=None, name=None, modparams=()) -> str:
    # if cmod is None:
    #     cmod = peak_to_coreir(peak_fc, wrap=True)
    dag_node, node_name = peak_to_node(nodes, peak_fc, stateful=stateful, name=name, modparams=modparams)
    check_ports(dag_node, cmod)
    nodes.add(node_name, peak_fc, cmod, dag_node)
    return node_name


#Loads a coreir header file, associates each coreir file with a peak_fc, creates a dag_node in nodes
def load_and_link_peak(nodes: Nodes, header_file: str, peak_dict: dict):
    c = CoreIRContext()
    header_modules = c.load_header(header_file)
    for cmod in header_modules:
        if cmod.ref_name not in peak_dict:
            raise ValueError(f"{cmod.ref_name} does not have an associated peak_dict")
        peak_fc = peak_dict[cmod.ref_name]
        stateful = False
        if isinstance(peak_fc, tuple):
            peak_fc, stateful = peak_fc
        node_name = load_from_peak(nodes, peak_fc, stateful=stateful, cmod=cmod, name=cmod.ref_name)
        assert node_name == cmod.ref_name

