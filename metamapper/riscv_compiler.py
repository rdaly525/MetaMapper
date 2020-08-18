from metamapper.common_passes import VerifyNodes, print_dag, SimplifyCombines, RemoveSelects, prove_equal, Clone, Uses, Schedule, TypeLegalize, Riscv2_Riscv, SMT, prove_formula
from metamapper.rewrite_table import RewriteTable, RewriteRule
from metamapper.node import Nodes, DagNode
from metamapper.instruction_selection import GreedyCovering
from peak.mapper import RewriteRule as PeakRule
import metamapper.peak_util as putil
from peak.examples import riscv, riscv_m, riscv_hack, riscv_m_hack, riscv_ext
from .family import fam
import typing as tp

class Compiler:
    def __init__(self, WasmNodes: Nodes, alg=GreedyCovering, peak_rules: tp.List[PeakRule]=None, ops=None, solver='z3', m=False, e=False):
        assert ops is not None
        self.WasmNodes = WasmNodes
        ArchNodes = Nodes("RiscV")
        self.ArchNodes = ArchNodes
        if m:
            self.rv = riscv_m
            self.rv_hack = riscv_m_hack
            riscv_fc = riscv_m.sim.R32I_mappable_fc
        elif e:
            self.rv = riscv_ext
            self.rv_hack = riscv_hack
            riscv_fc = riscv_ext.sim.R32I_mappable_fc
        else:
            self.rv = riscv
            self.rv_hack = riscv_hack
            riscv_fc = riscv.sim.R32I_mappable_fc
        
        putil.load_from_peak(ArchNodes, riscv_fc, stateful=False, wasm=True)
        riscv2_fc, Inst2 = gen_riscv2(m)
        self.Inst2 = Inst2
        putil.load_from_peak(ArchNodes, riscv2_fc, stateful=False, wasm=True)
        self.table = RewriteTable(WasmNodes, ArchNodes)
        map2_set = [
            "i32.eq",
            "i32.ne",
            "i32.le_s",
            "i32.le_u",
            "i32.ge_s",
            "i32.ge_u",
            "const20",
        ]

        map2_set = set(map2_set)
        if peak_rules is None:
            #auto discover the rules for CoreIR
            print("Discovering", ops)
            for op in ops:
                if op in map2_set:
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

    def set_instr(self, info):
        asm = self.rv.asm
        inst = info.pop('inst')
        aadt = type(inst)
        adt_val = aadt_to_adt(inst)
        cur_fields = asm.get_fields(adt_val)
        #print("Trying to set instr {")
        #print("  info", info)
        #print("  cf", cur_fields)
        #print(cur_fields)
        for idx in ("rd", "rs1", "rs2"):
            assert idx in cur_fields
            if cur_fields[idx] is not None:
                cur_fields[idx] = 0
            else: # only happens for multi-case
                info[idx] = None
        #print("  mf", cur_fields)
        for k, v in info.items():
            assert k in cur_fields
            cur_fields[k] = v

        #print("  nf", cur_fields)
        adt_val = asm.set_fields(adt_val, **cur_fields)

        #Verify
        check_fields = asm.get_fields(adt_val)
        for k, v in cur_fields.items():
            if check_fields[k] != v:
                raise ValueError(f"{k} should be {v}, but is {check_fields[k]}")


        return aadt(adt_val)

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
        print("RemovedSelects")
        print_dag(mapped_dag)

        Riscv2_Riscv(self.ArchNodes, self.rv, self.Inst2).run(mapped_dag)
        print("After Riscv2_conversion")
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
        free = set(range(1, 32))
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
                inst_list.append(self.set_instr(inst_info[node]))
            if "inst" in inst_info[node]:
                print(inst_info[node]["inst"])
            else:
                print(node)
            for k,v in inst_info[node].items():
                print(f"  {k}: {v}")

        #assume the last instruction returns the final value
        output_idx = node_to_rd[node_list[-1]]
        print("out", output_idx)
        return Binary(inst_list, input_info, output_idx, orig_dag=original_dag, rv=self.rv, rv_hack=self.rv_hack)

def aadt_to_adt(val):
    aadt = type(val)
    assembler = aadt.assembler_t(aadt.adt_t)
    adt_val = assembler.disassemble(val._value_)
    return adt_val


from peak.assembler import Assembler
class Binary:
    def __init__(self, insts: tp.List, input_info: dict, output_idx, orig_dag, rv, rv_hack):
        self.insts = insts
        self.input_info = input_info
        self.output_idx = output_idx
        self.orig_dag = orig_dag
        self.rv = rv
        self.rv_hack = rv_hack

    def run(self, **kwargs):
        if set(kwargs.keys()) != set(self.input_info.keys()):
            raise ValueError(f"Inputs need to be {self.input_info.keys()}")
        cpu = self.rv.sim.R32I_fc(fam().PyFamily())()
        isa = self.rv.sim.ISA_fc(fam().PyFamily())
        for input, ridx in self.input_info.items():
            val = kwargs[input]
            cpu.register_file.store(isa.Idx(ridx), isa.Word(val))

        def pr():
            print("RF")
            for k, v in cpu.register_file.rf.items():
                print ("  ",k, v)
        pr()
        for inst in self.insts:
            inst_adt = aadt_to_adt(inst)
            cpu(inst_adt, isa.Word(0))
            pr()
        return cpu.register_file.load1(isa.Idx(self.output_idx))

    #returns None if Proven
    def prove(self, solver="z3"):
        i0, o0 = SMT().get(self.orig_dag)
        oval = o0["out"]

        isa = self.rv_hack.isa.ISA_fc.Py
        smt_isa = self.rv_hack.isa.ISA_fc.SMT
        R32I = self.rv_hack.sim.R32I_fc.Py
        cpu = R32I()
        initial_values = [smt_isa.Word(name=f'r{i}') for i in range(32)]
        for i in range(5):
            cpu.register_file.store(isa.Idx(i), initial_values[i])
        for input, ridx in self.input_info.items():
            cpu.register_file.store(isa.Idx(ridx), i0[input])

        asmh = Assembler(self.rv_hack.isa.ISA_fc.Py.Inst)
        def inst_to_hack(inst):
            return asmh.disassemble(inst._value_)

        def pr():
            print("RF")
            for k, v in cpu.register_file.rf.items():
                print ("  ",k, v)
        #Execute the instructions
        pr()
        for i, inst in enumerate(self.insts):
            inst_hack = inst_to_hack(inst)
            cpu(inst_hack, smt_isa.Word(i))
            pr()
        cpu_out = cpu.register_file.load1(isa.Idx(self.output_idx))
        return prove_formula(cpu_out != oval, solver, i0)


from peak import family_closure, Peak, Const, name_outputs
from hwtypes.adt import Product
def gen_riscv2(m, e=False):

    if m:
        r = riscv_m
    elif e:
        r = riscv_ext
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

            @name_outputs(rd=PyWord)
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
