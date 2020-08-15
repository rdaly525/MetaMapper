from metamapper.common_passes import VerifyNodes, print_dag, SimplifyCombines, RemoveSelects, prove_equal, Clone, Uses, Schedule, TypeLegalize, Riscv2_Riscv
from metamapper.rewrite_table import RewriteTable, RewriteRule
from metamapper.node import Nodes, DagNode
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule
import metamapper.peak_util as putil
from peak.examples import riscv, riscv_m, riscv_hack
from .family import fam
import typing as tp


#Defining the custom rewrite rules

#i32.const




#RewriteRule
#def __init__(self,
#             tile: Dag,
#             replace: tp.Callable,
#             cost: tp.Callable,
#             checker: tp.Callable = None,
#             name=None
#             ):

#Rewrite Rule for
#    le_u


# Load rule for -1

#input_type = Product.from_fields("Input", {"in0": BV16, "in1": BV16, "in2": BV16})
#output_type = Product.from_fields("Output", {"out": BV16})
#input_node = Input(type=input_type)
#in0 = input_node.select("in0")
#in1 = input_node.select("in1")
#in2 = input_node.select("in2")
#fma1 = FMANode(Constant(value=BV16(5), type=BV16), in0, in1)
#fma2 = FMANode(Constant(value=BV16(2), type=BV16), in2, fma1.select("out"))
#output_node = Output(fma2.select("out"), type=output_type)
#dag = Dag(sources=[input_node], sinks=[output_node])

class Compiler:
    def __init__(self, WasmNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None, ops=None, solver='z3', m=False):
        assert ops is not None
        self.WasmNodes = WasmNodes
        ArchNodes = Nodes("RiscV")
        self.ArchNodes = ArchNodes
        if m:
            riscv_fc = riscv_m.sim.R32I_mappable_fc
        else:
            riscv_fc = riscv.sim.R32I_mappable_fc
        putil.load_from_peak(ArchNodes, riscv_fc, stateful=False, wasm=True)
        riscv2_fc, Inst2 = gen_riscv2(m)
        self.Inst2 = Inst2
        putil.load_from_peak(ArchNodes, riscv2_fc, stateful=False, wasm=True)
        self.table = RewriteTable(WasmNodes, ArchNodes)
        map2_set = [
            "i32.eq",
            "i32.neq",
            "i32.le_s",
            "i32.le_u",
            "i32.ge_s",
            "i32.ge_u",
        ]

        map2_set = set(map2_set)
        if peak_rules is None:
            #auto discover the rules for CoreIR
            print("Discovering", ops)
            for op in ops:
                if op in map2_set:
                    assert 0
                    node_name = "Riscv2"
                else:
                    node_name = "R32I_mappable"
                print(f"Searching for {op} -> {node_name}", flush=True)
                peak_rule = self.table.discover(op, node_name, solver=solver)
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

    def compile(self, dag, prove=True) -> tp.Any:
        print("premapped")
        print_dag(dag)
        original_dag = Clone().clone(dag, iname_prefix=f"original_")

        mapped_dag = self.inst_sel(dag)
        #print("postmapped")
        #print_dag(mapped_dag)
        SimplifyCombines().run(mapped_dag)
        #print("simplifyCombines")
        #print_dag(mapped_dag)
        RemoveSelects().run(mapped_dag)

        #Riscv2_Riscv(self.ArchNodes).run(mapped_dag)

        print("RemovedSelects")
        print_dag(mapped_dag)
        unmapped = VerifyNodes(self.ArchNodes).verify(mapped_dag)
        if unmapped is not None:
            raise ValueError(f"Following nodes were unmapped: {unmapped}")
        assert VerifyNodes(self.WasmNodes).verify(original_dag) is None
        if prove:
            counter_example = prove_equal(original_dag, mapped_dag)
            if counter_example is not None:
                raise ValueError(f"Mapped is not the same {counter_example}")


        #Very simple Register Allication
        uses, inputs, outputs, insts = Uses().uses(mapped_dag)
        #print("u")
        #for k, v in uses.items():
        #    print("  ", k, v)
        node_list = list(inputs) + Schedule().schedule(mapped_dag)
        #print("nl")
        #for n in node_list:
        #    print("  ", n)
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
            print(node)
            for k,v in inst_info[node].items():
                print(f"  {k}: {v}")

        #assume the last instruction returns the final value
        output_idx = node_to_rd[node_list[-1]]
        return Binary(inst_list, input_info, output_idx)

def aadt_to_adt(val):
    aadt = type(val)
    assembler = aadt.assembler_t(aadt.adt_t)
    adt_val = assembler.disassemble(val._value_)
    return adt_val

def set_instr( info):
    from peak.examples.riscv import asm
    inst = info.pop('inst')
    aadt = type(inst)
    adt_val = aadt_to_adt(inst)
    cur_fields = asm.get_fields(adt_val)
    for k, v in info.items():
        assert k in cur_fields
        cur_fields[k] = v
    adt_val = asm.set_fields(adt_val, **cur_fields)
    return aadt(adt_val)


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

        def pr():
            print("RF")
            for k, v in cpu.register_file.rf.items():
                print ("  ",k, v)
        #pr()
        for inst in self.insts:
            inst_adt = aadt_to_adt(inst)
            cpu(inst_adt, isa.Word(0))
            #pr()
        return cpu.register_file.load1(isa.Idx(self.output_idx))


from peak import family_closure, Peak, Const, name_outputs
from hwtypes.adt import Product
def gen_riscv2(m):

    if m:
        r = riscv_m
    else:
        r = riscv

    ISA_fc = r.isa.ISA_fc

    isa = ISA_fc.Py
    class Inst2(Product):
        i0 = isa.Inst
        i1 = isa.Inst

    @family_closure(r.family)
    def Riscv2_fc(family):
        Word = family.Word
        RMap = r.sim.R32I_mappable_fc(family)
        PyWord = fam().PyFamily().Word


        @family.assemble(locals(), globals())
        class Riscv2(Peak):
            print("Creating Peak class with fam", family)
            def __init__(self):
                self.i0: RMap = RMap()
                self.i1: RMap = RMap()

            @name_outputs(out=PyWord)
            def __call__(self,
                inst: Const(Inst2),
                rs1: PyWord,
                rs2: PyWord,
            ) -> PyWord:
                _, i0_rd = self.i0(inst.i0, Word(0), rs1, rs2, Word(0))

                _, i1_rd = self.i1(inst.i1, Word(0), i0_rd, i0_rd, Word(0))
                return i1_rd
        return Riscv2
    return Riscv2_fc, Inst2
