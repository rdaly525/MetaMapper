import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler, gen_riscv2
from metamapper.irs.wasm import gen_WasmNodes
#from peak.examples import riscv
from peak.examples import riscv_m
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
            if name != "i32.add":
                continue
            print("Looking for ", name)
            start = timer()
            rr = table.discover(name, "R32I_mappable", solver=solver, path_constraints=rc)
            assert rr is None
            end = timer()
            found = "n" if rr is None else "f"
            print(f"{name}: {end-start}: {found}", file=f)
            print(f"{name}: {end-start}: {found}")

def test_riscv_m_discovery(i, solver, c, e=True):
    assert e
    if c:
        rc = {
            ("pc",): 0,
            ("rd",): 0,
        }
    else:
      rc = {}
    print("File", i)
    CoreIRContext(reset=True)
    set_fam(riscv_m.family)
    WasmNodes = gen_WasmNodes()

    arch_fc = riscv_m.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)
    riscv2_fc, Inst2 = gen_riscv2(m=True)
    putil.load_from_peak(ArchNodes, riscv2_fc, stateful=False, wasm=True)

    table = RewriteTable(WasmNodes, ArchNodes)
    with open(f'results/riscv_m/{solver}_c{c}_e{e}_{i}.txt', 'w') as f:
        for name in WasmNodes.peak_nodes:
            if name not in [
                "const20",
                #"i32.mul",
                #"i32.div_s",
                #"i32.div_u",
                #"i32.rem_s",
                #"i32.rem_u",
            ]:
                continue
            print("Looking for ", name)
            start = timer()
            #rr = table.discover(name, "R32I_mappable", solver=solver, path_constraints=rc)
            rc = {}
            rr = table.discover(name, "Riscv2", solver=solver, path_constraints=rc)
            assert rr is not None
            end = timer()
            found = "n" if rr is None else "f"
            print(f"{name}: {end-start}: {found}", file=f)
            print(f"{name}: {end-start}: {found}")

test_riscv_m_discovery(0, 'btor', True)
