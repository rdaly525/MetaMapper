from metamapper.common_passes import VerifyNodes, print_dag, SimplifyCombines, RemoveSelects, prove_equal, Clone, Uses, Schedule
from metamapper.rewrite_table import RewriteTable
from metamapper.node import Nodes, DagNode
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule
from peak.examples.riscv import asm
import typing as tp

class Compiler:
    def __init__(self, WasmNodes: Nodes, ArchNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None):
        self.WasmNodes = WasmNodes
        self.ArchNodes = ArchNodes
        self.table = RewriteTable(WasmNodes, ArchNodes)
        ops = (
            "i32.add",
        )
        if peak_rules is None:
            for node_name in ArchNodes._node_names:
                #auto discover the rules for CoreIR
                for op in ops:
                    peak_rule = self.table.discover(op, node_name)
                    print(f"Searching for {op} -> {node_name}")
                    if peak_rule is None:
                        print(f"  Not Found :(")
                        pass
                    else:
                        print(f"  Found!")
        else:
            #load the rules
            for peak_rule in peak_rules:
                self.table.add_peak_rule(peak_rule)
        self.inst_sel = alg(self.table)

    def compile(self, dag) -> tp.Any:
        #print("premapped")
        #print_dag(dag)
        original_dag = Clone().clone(dag, iname_prefix=f"original_")
        mapped_dag = self.inst_sel(dag)
        #print("postmapped")
        #print_dag(mapped_dag)
        SimplifyCombines().run(mapped_dag)
        #print("simplifyCombines")
        #print_dag(mapped_dag)
        RemoveSelects().run(mapped_dag)
        print("RemovedSelects")
        print_dag(mapped_dag)
        unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
        if unmapped is not None:
            raise ValueError(f"Following nodes were unmapped: {unmapped}")
        assert VerifyNodes(self.WasmNodes).verify(original_dag) is None
        #counter_example = prove_equal(original_dag, mapped_dag)
        #if counter_example is not None:
        #    raise ValueError(f"Mapped is not the same {counter_example}")


        #Very simple Register Allication
        uses, inputs, outputs, insts = Uses().uses(mapped_dag)
        node_list = list(inputs) + Schedule().schedule(mapped_dag)
        reaching = {i:i for i in range(len(node_list))} #idx to worst idx
        for i, node in enumerate(node_list):
            if not isinstance(node, DagNode):
                continue
            for child in uses[node].values():
                cidx = node_list.index(child)
                reaching[cidx] = max(i, reaching[cidx])

        #Determine rd indices
        node_to_rd = {}
        free = set(range(1, 16))
        to_free = {}
        for node_idx, node in enumerate(node_list):
            if node_idx in to_free:
                freed_reg = to_free.pop(node_idx)
                free.add(freed_reg)
            rd_val = free.pop()
            to_free[reaching[node_idx]] = rd_val
            node_to_rd[node] = rd_val

        #propogate rd indices to rs1 and rs2 indices
        inst_info = {node:{} for node in node_to_rd}
        input_info = {} # name to rd
        for node, rd in node_to_rd.items():
            inst_info[node]["rd"] = rd
            if isinstance(node, DagNode):
                inst_info[node]["inst"] = insts[node]
                for rname, child in uses[node].items():
                    inst_info[node][rname] = node_to_rd[child]
            else:
                input_info[node] = rd



        inst_list = []
        for node in node_list:
            if node not in inputs:
                inst_list.append(set_instr(inst_info[node]))
            #print(node)
            #for k,v in inst_info[node].items():
            #    print(f"  {k}: {v}")

        #assume the last instruction returns the final value
        output_idx = node_to_rd[node_list[-1]]
        return Binary(inst_list, input_info, output_idx)

def aadt_to_adt(val):
    aadt = type(val)
    assembler = aadt.assembler_t(aadt.adt_t)
    adt_val = assembler.disassemble(val._value_)
    return adt_val

def set_instr( info):
    inst = info.pop('inst')
    aadt = type(inst)
    adt_val = aadt_to_adt(inst)
    cur_fields = asm.get_fields(adt_val)
    for k, v in info.items():
        assert k in cur_fields
        cur_fields[k] = v
    adt_val = asm.set_fields(adt_val, **cur_fields)
    return aadt(adt_val)

from peak.examples import riscv
from .family import fam
class Binary:
    def __init__(self, insts: tp.List, input_info: dict, output_idx):
        self.insts = insts
        self.input_info = input_info
        self.output_idx = output_idx

    def run(self, **kwargs):
        if set(kwargs.keys()) != set(self.input_info.keys()):
            raise ValueError(f"Inputs need to be {self.input_info.keys()}")
        cpu = riscv.sim.R32I_fc(fam().PyFamily())()
        isa = riscv.sim.ISA_fc(fam().PyFamily())
        for input, ridx in self.input_info.items():
            val = kwargs[input]
            cpu.register_file.store(isa.Idx(ridx), isa.Word(val))

        for inst in self.insts:
            inst_adt = aadt_to_adt(inst)
            cpu(inst_adt, isa.Word(0))
        return cpu.register_file.load1(isa.Idx(self.output_idx))



