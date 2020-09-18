import metamapper.wasm.interp.convention as C
from metamapper.wasm.interp.structure import Instruction

import metamapper.wasm_util as wutil
from metamapper.common_passes import print_dag


def test_file_load():
    file = './examples/wasm/add.wasm'
    name = "add"
    ilist, num_args = wutil.wasm_file_to_ilist(file, "add")
    print(num_args)
    print(ilist)


def test_sym():
    I = Instruction
    expr = [
        I(C.get_local, 0),
        I(C.get_local, 1),
        I(C.i32_add),
        I(C.get_local, 1),
        I(C.i32_mul)
    ]
    dag = wutil.ilist_to_dag(2, expr)
    print_dag(dag)


def test_dag():
    wasm_file = './examples/wasm/add.wasm'
    dag = wutil.wasm_to_dag(wasm_file, "add")
    print_dag(dag)

