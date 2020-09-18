import metamapper.peak_util as putil
from metamapper.node import Nodes
from metamapper import CoreIRContext
from metamapper.riscv_compiler import Compiler, gen_riscv2
from metamapper.irs.wasm import gen_WasmNodes
from peak.examples import riscv, riscv_m, riscv_ext
from metamapper.family import set_fam, fam
import metamapper.wasm_util as wutil
from metamapper.rewrite_table import RewriteTable
from timeit import default_timer as timer
from peak import Peak, name_outputs, family_closure, Const
from hwtypes.adt import Product

def test_riscv_discovery(i, rname, solver, c):
    if rname == "riscv":
        rv = riscv
        riscv2_fc, Inst2 = gen_riscv2(m=False,e=False)
    elif rname == "riscv_ext":
        rv = riscv_ext
        riscv2_fc, Inst2 = gen_riscv2(m=False,e=True)
    elif rname == "riscv_m":
        rv = riscv_m
        riscv2_fc, Inst2 = gen_riscv2(m=True,e=False)
    else:
        assert 0
    if c:
        rc = {
            ("pc",): 0,
            ("rd",): 0,
        }
    else:
        rc = {}
    print("File", i, rname)
    CoreIRContext(reset=True)
    set_fam(rv.family)
    WasmNodes = gen_WasmNodes()

    arch_fc = rv.sim.R32I_mappable_fc
    ArchNodes = Nodes("RiscV")
    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)
    putil.load_from_peak(ArchNodes, riscv2_fc, stateful=False, wasm=True)
    table = RewriteTable(WasmNodes, ArchNodes)
    map2_set = [
        "const20",
        "i32.eq",
        "i32.ne",
        "i32.le_s",
        "i32.le_u",
        "i32.ge_s",
        "i32.ge_u",
    ]

    cset = [
        "const0",
        "const1",
        "constn1",
        "const12",
    ]
    eset = [
        "i32.popcnt",
        "i32.clz",
        "i32.ctz",
    ]
    mset = [
       "i32.mul",
       "i32.div_s",
       "i32.div_u",
       "i32.rem_s",
       "i32.rem_u",
    ]


    with open(f'results/{rname}/{solver}_c{c}_eTrue_{i}.txt', 'w') as f:
        #for name in map2_set:
        #for name in cset:
        for name in WasmNodes.peak_nodes:
            if name in map2_set:
                continue
            if rname == "riscv":
                if name in eset:
                    continue
                if name in mset:
                    continue
            elif rname == "riscv_ext":
                if name not in eset:
                    continue
            elif rname == "riscv_m":
                if name not in mset:
                    continue
            print("Looking for ", name, flush=True)
            start = timer()
            rr = table.discover(name, "R32I_mappable", solver=solver, path_constraints=rc)
            #rr = table.discover(name, "Riscv2", solver=solver, path_constraints=rc)
            end = timer()
            found = "n" if rr is None else "f"
            print(f"{name}: {end-start}: {found}", file=f, flush=True)
            print(f"{name}: {end-start}: {found}", flush=True)


#First need to discover const + rewrite with btor
for i in range(4,10):
    for rname in ("riscv", "riscv_ext", "riscv_m"):
        test_riscv_discovery(i, rname=rname, solver='btor', c=True)



#def test_riscv_m_discovery(i, solver, c, e=True):
#    assert e
#    if c:
#        rc = {
#            ("pc",): 0,
#            ("rd",): 0,
#        }
#    else:
#      rc = {}
#    print("File", i)
#    CoreIRContext(reset=True)
#    set_fam(riscv_m.family)
#    WasmNodes = gen_WasmNodes()
#
#    arch_fc = riscv_m.sim.R32I_mappable_fc
#    ArchNodes = Nodes("RiscV")
#    putil.load_from_peak(ArchNodes, arch_fc, stateful=False, wasm=True)
#    riscv2_fc, Inst2 = gen_riscv2(m=True)
#    putil.load_from_peak(ArchNodes, riscv2_fc, stateful=False, wasm=True)
#
#    table = RewriteTable(WasmNodes, ArchNodes)
#    with open(f'results/riscv_m/{solver}_c{c}_e{e}_{i}.txt', 'w') as f:
#        for name in WasmNodes.peak_nodes:
#            if name not in [
#                "const20",
#                #"i32.mul",
#                #"i32.div_s",
#                #"i32.div_u",
#                #"i32.rem_s",
#                #"i32.rem_u",
#            ]:
#                continue
#            print("Looking for ", name)
#            start = timer()
#            #rr = table.discover(name, "R32I_mappable", solver=solver, path_constraints=rc)
#            rc = {}
#            rr = table.discover(name, "Riscv2", solver=solver, path_constraints=rc)
#            assert rr is not None
#            end = timer()
#            found = "n" if rr is None else "f"
#            print(f"{name}: {end-start}: {found}", file=f)
#            print(f"{name}: {end-start}: {found}")

