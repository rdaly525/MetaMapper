import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv_ext
from metamapper.family import set_fam
import metamapper.wasm_util as wutil
from metamapper.rewrite_table import RewriteTable
from timeit import default_timer as timer

def test_riscv_discovery(i, solver, c):
    if c:
        rc = {
            ("pc",): 0,
            ("rd",): 0,
        }
    else:
      rc = {}
    print("File", i)
    riscv = riscv_ext
    CoreIRContext(reset=True)
    set_fam(riscv.family)
    WasmNodes = gen_WasmNodes()

    arch_fc = riscv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)

    table = RewriteTable(WasmNodes, ArchNodes)
    with open(f'results/riscv_ext/{solver}_{c}_{i}.txt', 'w') as f:
        for name in WasmNodes.peak_nodes:
            print("Looking for ", name)
            start = timer()
            rr = table.discover(name, "R32I_mappable", solver=solver, path_constraints=rc)
            end = timer()
            found = "n" if rr is None else "f"
            print(f"{name}: {end-start}: {found}", file=f)
            print(f"{name}: {end-start}: {found}")


for i in range(3):
    test_riscv_discovery(i, solver="cvc4", c=True)
