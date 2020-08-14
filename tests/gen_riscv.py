import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv
from metamapper.family import set_fam, fam
import metamapper.wasm_util as wutil
from metamapper.rewrite_table import RewriteTable
from timeit import default_timer as timer
from peak import Peak, name_outputs, family_closure, Const
from hwtypes.adt import Product

def test_riscv_discovery(i, solver, c):
    if c:
        rc = {
            ("pc",): 0,
            ("rd",): 0,
        }
    else:
      rc = {}
    print("File", i)
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    table = RewriteTable(WasmNodes, ArchNodes)
    with open(f'results/riscv/{solver}_{c}_{i}.txt', 'w') as f:
        for name in WasmNodes.peak_nodes:
            print("Looking for ", name)
            start = timer()
            rr = table.discover(name, "R32I_mappable", solver=solver, path_constraints=rc)
            end = timer()
            found = "n" if rr is None else "f"
            print(f"{name}: {end-start}: {found}", file=f)
            print(f"{name}: {end-start}: {found}")



def test_riscv_discovery_multi():
    rc = {
        ("pc0",): 0,
        ("rd0",): 0,
        ("pc1",): 0,
        ("rd1",): 0,
    }

    CoreIRContext(reset=True)
    set_fam(riscv.family)
    ISA_fc = riscv.isa.ISA_fc
    @family_closure(riscv.family)
    def Riscv2_fc(family):
        print("calling with", family)
        Word = family.Word
        isa = ISA_fc(family)
        RMap = riscv.sim.R32I_mappable_fc(family)

        class Inst2(Product):
            i0 = isa.Inst
            i1 = isa.Inst
            opt =  family.BitVector[2]

        @family.assemble(locals(), globals())
        class Riscv2(Peak):
            def __init__(self):
                self.i0 = RMap()
                self.i1_0 = RMap()
                self.i1_1 = RMap()
                self.i1_2 = RMap()

            def __call__(self,
                inst: Const(Inst2),
                rs1: Word,
                rs2: Word,
                rs3: Word,
            ) -> Word:
                i0_rd = self.i0(inst.i0, Word(0), rs1, rs2, Word(0))

                i1_0_rd = self.i1_0(inst.i1, Word(0), i0_rd, rs3, Word(0))
                i1_1_rd = self.i1_1(inst.i1, Word(0), rs3, i0_rd, Word(0))
                i1_2_rd = self.i1_2(inst.i1, Word(0), i0_rd, i0_rd, Word(0))
                if inst.opt == 0:
                    return i1_0_rd
                elif inst.opt == 1:
                    return i1_1_rd
                elif inst.opt == 1:
                    return i1_2_rd
                else:
                    return Word(0)
        return Riscv2


    WasmNodes = gen_WasmNodes()
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, Riscv2_fc, stateful=False, wasm=True)

    table = RewriteTable(WasmNodes, ArchNodes)
    for name in ("i32.ne", "i32.eq"):
        print("Looking for ", name)
        start = timer()
        rr = table.discover(name, "Riscv2", solver='z3', path_constraints=rc)
        end = timer()
        found = "n" if rr is None else "f"
        print(f"{name}: {end-start}: {found}")

test_riscv_discovery_multi()

