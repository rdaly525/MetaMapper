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
    basic = ("mul", "add", "and_", "or_")
    other = ()#("ashr", "eq", "lshr", "mux", "slt", "sge", "sub", "ult")
    #TODO handle const
    #bit_ops = ("const", "or_", "and_", "xor")
    #commonlib_ops = ("abs", "smax", "smin", "umin", "umax")
    for namespace, ops in (
        ("i32", basic + other),
    ):
        for op in ops:
            name = f"{namespace}.{op}"
            peak_fc = wasm_ir.instructions[name]
            name_ = load_from_peak(WasmNodes, peak_fc, name=name, wasm=True)
            assert name_ == name
            print(f"Loaded {name}!")

    return WasmNodes

