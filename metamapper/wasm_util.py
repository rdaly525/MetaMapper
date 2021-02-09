from .node import Dag, Nodes, DagNode, Input, Constant, Select, Output
from .irs.wasm import gen_WasmNodes

import metamapper.wasm.interp.convention as C
import metamapper.wasm.interp as interp
from metamapper.wasm.interp.structure import Instruction
import typing as tp
import delegator

WasmNodes = gen_WasmNodes()

class Stack:
    def __init__(self):
        self.data = []

    def __repr__(self):
        return self.data.__repr__()

    def add(self, e):
        self.data.append(e)

    def ext(self, e: tp.List):
        for i in e:
            self.add(i)

    def pop(self):
        return self.data.pop()

    def len(self):
        return len(self.data)

    def top(self):
        return self.data[-1]


def wasm_to_dag(file, fun_name):
    ilist, num_args = wasm_file_to_ilist(file, fun_name)
    return ilist_to_dag(num_args, ilist)

def wasm_file_to_ilist(file, fun_name):
    vm = interp.load(file)
    func_addr = vm.func_addr(fun_name)
    func = vm.store.funcs[vm.module_instance.funcaddrs[func_addr]]
    expr_list = func.code.expr.data
    num_args = len(func.functype.args)
    return expr_list, num_args

from hwtypes import Product
from .family import fam


def ilist_to_dag(num_args, ilist : tp.List[Instruction]):
    BV32 = fam().PyFamily().BitVector[32]
    def make_const(val):
        return Constant(value=BV32(val), type=BV32)
    input_t = Product.from_fields("Input", {f"in{i}": BV32 for i in range(num_args)})
    output_t = Product.from_fields("Output", {"out": BV32})
    input = Input(type=input_t)
    locals = []
    for i in range(num_args):
        locals.append(input.select(f"in{i}"))
    for _ in range(2):
        locals.append(None)
    stack = Stack()
    for pc, i in enumerate(ilist):
        opcode = i.code
        if opcode == C.drop:
            stack.pop()
        elif opcode == C.select:
            pred = stack.pop()
            in1 = stack.pop()
            in0 = stack.pop()

            gt0 = WasmNodes.dag_nodes["i32.gt_u"](pred, make_const(0)).select("out")
            mask = WasmNodes.dag_nodes["i32.sub"](make_const(0), gt0).select("out")
            mask_n = WasmNodes.dag_nodes["i32.xor"](make_const(-1), mask).select("out")
            in1_mask = WasmNodes.dag_nodes["i32.and_"](mask, in1).select("out")
            in0_mask = WasmNodes.dag_nodes["i32.and_"](mask_n, in0).select("out")
            res = WasmNodes.dag_nodes["i32.or_"](in1_mask, in0_mask).select("out")
            stack.add(res)
        elif opcode == C.get_local:
            if locals[i.immediate_arguments] is None:
                raise ValueError("Need more locals")
            stack.add(locals[i.immediate_arguments])
        elif opcode == C.i32_const:
            stack.add(Constant(value=BV32(i.immediate_arguments), type=BV32))
        elif opcode in UnaryOps:
            node_name = UnaryOps[opcode]
            node = WasmNodes.dag_nodes[node_name]
            in0 = stack.pop()
            stack.add(node(in0).select("out"))
        elif opcode in BinaryOps:
            node_name = BinaryOps[opcode]
            node = WasmNodes.dag_nodes[node_name]
            in1 = stack.pop()
            in0 = stack.pop()
            stack.add(node(in0, in1).select("out"))
        elif opcode in CompOps:
            node_name = CompOps[opcode]
            node = WasmNodes.dag_nodes[node_name]
            in1 = stack.pop()
            in0 = stack.pop()
            stack.add(node(in0, in1).select("out"))
        elif opcode == C.end:
            #Control flow would pop off the label
            pass
        elif opcode == C.tee_local:
            locals[i.immediate_arguments] = stack.top()
            stack.add(node(in0, in1).select(0))
        elif opcode == C.end:
            #Control flow would pop off the label
            pass
        else:
            raise NotImplementedError(C.op_name(opcode))

    ret = stack.pop()
    assert stack.len() == 0
    output = Output(ret, type=output_t)
    return Dag(sources=[input], sinks=[output])

UnaryOps = {
    C.i32_clz: "i32.clz",
    C.i32_ctz: "i32.ctz",
    C.i32_popcnt: "i32.popcnt",
    C.i32_eqz: "i32.eqz",
}

BinaryOps = {
    C.i32_add: "i32.add",
    C.i32_sub: "i32.sub",
    C.i32_mul: "i32.mul",
    C.i32_div_s: "i32.div_s",
    C.i32_div_u: "i32.div_u",
    C.i32_rem_s: "i32.rem_s",
    C.i32_rem_u: "i32.rem_u",
    C.i32_and: "i32.and_",
    C.i32_or: "i32.or_",
    C.i32_xor: "i32.xor",
    C.i32_shl: "i32.shl",
    C.i32_shr_s: "i32.shr_s",
    C.i32_shr_u: "i32.shr_u",
    C.i32_rotl: "i32.rotl",
    C.i32_rotr: "i32.rotr",
}

#These always return i32
CompOps = {
    C.i32_eq: "i32.eq",
    C.i32_ne: "i32.ne",
    C.i32_lt_s: "i32.lt_s",
    C.i32_lt_u: "i32.lt_u",
    C.i32_le_s: "i32.le_s",
    C.i32_le_u: "i32.le_u",
    C.i32_gt_s: "i32.gt_s",
    C.i32_gt_u: "i32.gt_u",
    C.i32_ge_s: "i32.ge_s",
    C.i32_ge_u: "i32.ge_u",
}

def compile_c_to_wasm(file_name, cpath="./examples/wasm/c/", build_path="./examples/wasm/build", fname=None):
    if fname is None:
        fname=f"_{file_name}"
    cfile = f"{cpath}/{file_name}.c"
    wasm_file = f"{build_path}/{file_name}.wasm"
    wat_file = f"{build_path}/{file_name}.wat"

    from sys import platform
    if platform in ("linux", "linux2"):
        sed = 'sed -i'
    elif platform == "darwin":
        sed = 'sed -i \'\''
    else:
        raise NotImplementedError(platform)
    for cmd in (
        f'emcc -Os -s EXPORTED_FUNCTIONS="[\'{fname}\']" -o {wasm_file} {cfile}',
        f'wasm2wat {wasm_file} -o {wat_file}',
        f'{sed} "s/[(]data.*[)]/)/g" {wat_file}',
        f'wat2wasm {wat_file} -o {wasm_file}',
    ):
        res = delegator.run(cmd)
        assert not res.return_code, res.out + res.err
    return wasm_file

#def peak_to_wasm_dag(WasmNodes: Nodes, CoreIRNodes: Nodes, peak_fc) -> Dag:
#    raise NotImplementedError()
#
#
#def rr_from_node(nodes: Nodes, name):
#    node = nodes.dag_nodes[name]
#    peak_fc = nodes.peak_nodes[name]
#    replace = peak_to_wasm_dag(peak_fc)

