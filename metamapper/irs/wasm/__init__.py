from functools import lru_cache

from .ir import gen_WASM
from ...node import Nodes, Constant
from ...peak_util import load_from_peak

def strip_trailing(op):
    if op[-1] == "_":
        return op[:-1]
    return op

@lru_cache(None)
def gen_WasmNodes(inlcude64=False):
    WasmNodes = Nodes("Wasm")
    wasm_ir = gen_WASM(include64=inlcude64)
    basic = wasm_ir.instructions.keys()
    #basic = ("mul", "add", "and_", "or_", "shr_s")
    #other = ()#("ashr", "eq", "lshr", "mux", "slt", "sge", "sub", "ult")
    #TODO handle const
    #bit_ops = ("const", "or_", "and_", "xor")
    #commonlib_ops = ("abs", "smax", "smin", "umin", "umax")
    for namespace, ops in (
        #("i32", basic + other),
        ("i32", basic),
    ):
        for op in ops:
            #name = f"{namespace}.{op}"
            name = op
            peak_fc = wasm_ir.instructions[name]
            name_ = load_from_peak(WasmNodes, peak_fc, name=name, wasm=True)
            assert name_ == name
            print(f"Loaded {name}!")

    #Const1 = WasmNodes.create_dag_node("Const1", 1, stateful=False, attrs=())

    #rom2 = CoreIRContext().get_namespace("memory").generators["rom2"](depth=255, width=width)

    #CoreIRNodes.add("memory.rom2", peak_ir.instructions["memory.rom2"], rom2, Rom)
    #assert "memory.rom2" in CoreIRNodes.dag_nodes
    #assert CoreIRNodes.dag_nodes["memory.rom2"] is not None
    #return CoreIRNodes


    return WasmNodes

