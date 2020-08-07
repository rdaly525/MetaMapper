from .node import Dag, Nodes, DagNode, Input, Constant, Select, Output
from .irs.wasm import gen_WasmNodes

import metamapper.wasm.interp.convention as C
import metamapper.wasm.interp as interp
from metamapper.wasm.interp.structure import Instruction
import typing as tp

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
    input_t = Product.from_fields("Input", {f"in{i}": BV32 for i in range(num_args)})
    output_t = Product.from_fields("Output", {"out": BV32})
    input = Input(type=input_t)
    args = []
    for i in range(num_args):
        args.append(input.select(f"in{i}"))
    stack = Stack()
    exec_expr(args, stack, ilist)

    ret = stack.pop()
    assert stack.len() == 0
    output = Output(ret, type=output_t)
    return Dag(sources=[input], sinks=[output])


def exec_expr(
    locals_ : tp.List[DagNode],
    stack: Stack,
    expr_list: tp.List[Instruction],
):
    for pc, i in enumerate(expr_list):
        opcode = i.code
        if opcode == C.drop:
            stack.pop()
        elif opcode == C.select:
            cond = stack.pop()
            in1 = stack.pop()
            in0 = stack.pop()
            raise NotImplementedError()
            #stack.add(SelectNode(cond,in0,in1))
        elif opcode == C.get_local:
            stack.add(locals_[i.immediate_arguments])
        elif opcode == C.i32_const:
            stack.add(Constant(i.immediate_arguments))
        elif opcode in UnaryOps:
            node_name = UnaryOps[opcode]
            node = WasmNodes.dag_nodes[node_name]
            in0 = stack.pop()
            stack.add(node(in0).select(0))
        elif opcode in BinaryOps:
            node_name = BinaryOps[opcode]
            node = WasmNodes.dag_nodes[node_name]
            in1 = stack.pop()
            in0 = stack.pop()
            stack.add(node(in0, in1).select(0))
        elif opcode in CompOps:
            node_name = CompOps[opcode]
            node = WasmNodes.dag_nodes[node_name]
            in1 = stack.pop()
            in0 = stack.pop()
            stack.add(node(in0, in1).select(0))
        elif opcode == C.end:
            #Control flow would pop off the label
            pass
        else:
            raise NotImplementedError(C.op_name(opcode))


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
    C.i32_and: "i32.and",
    C.i32_or: "i32.or",
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

#def peak_to_wasm_dag(WasmNodes: Nodes, CoreIRNodes: Nodes, peak_fc) -> Dag:
#    raise NotImplementedError()
#
#
#def rr_from_node(nodes: Nodes, name):
#    node = nodes.dag_nodes[name]
#    peak_fc = nodes.peak_nodes[name]
#    replace = peak_to_wasm_dag(peak_fc)

