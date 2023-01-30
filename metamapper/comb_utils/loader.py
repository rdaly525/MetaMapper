from pathlib import Path

import comb.compiler
import comb.ir
import coreir
import typing as tp
from collections import OrderedDict, deque
import hwtypes as ht
from comb.ast import QSym, InDecl, OutDecl, Type, Sym, BoolType, BVType, IntType, TypeCall, IntValue
from comb.ir import CombProgram, CallExpr, AssignStmt
#returns input objects and output objects
#removes clk and reset


def ctype_to_hwtype(ctype: coreir.Type) -> tp.Union[ht.Bit, ht.BitVector]:
    if ctype.kind in ("Bit", "BitIn"):
        return ht.Bit
    assert ctype.kind == "Array"
    etype = ctype.element_type
    if etype.kind not in ("Bit", "BitIn"):
        raise ValueError("CoreIR modules must have flattened types")
    N = len(ctype)
    return ht.BitVector[N]


def get_coreir_io(rtype):
    assert isinstance(rtype, coreir.Record)
    inputs = OrderedDict()
    outputs = OrderedDict()
    for n, t in rtype.items():
        if t.kind == "Named": #Clocks and Resets
            continue
        if t.kind not in ("Array", "Bit", "BitIn"):
            raise ValueError("CoreIR moudles must have flattened types")
        if t.is_input():
            inputs[n] = ctype_to_hwtype(t)
        elif t.is_output():
            outputs[n] = ctype_to_hwtype(t)
        else:
            raise NotImplementedError("mixed io type not supported!")

    #Filter out "ASYNCRESET" and "CLK"
    for d in (inputs, outputs):
        for name in ("ASYNCRESET", "CLK"):
            if name in d:
                del d[name]
    return inputs, outputs

def ht_to_comb_type(ht_type):
    if ht_type is ht.Bit:
        return BoolType()
    elif issubclass(ht_type, ht.BitVector):
        N = ht_type.size
        return TypeCall(BVType(), [IntValue(N)])
    else:
        raise ValueError(str(ht_type))

    # returns a list of either (driver_inst, driver_ports) OR (selected_wireable)

coreir_gen_translate = {
    "coreir.add": "halide.add",
    "coreir.sub": "halide.sub",
    "coreir.mul": "halide.mul",
}

def get_comb(cmod: coreir.Module) -> CallExpr:
    cname = cmod.ref_name
    hname = coreir_gen_translate.get(cname, None)
    if hname is not None:
        assert cmod.generated
        vals = cmod.generator_args
        N = vals['width'].value
        assert isinstance(N,int)
        comb = halide_obj.comb_dict[hname][N]
        print(comb)
    else:
        raise NotImplementedError(f"Missing translation for {cname}")
    return comb

halide_obj = None
halide_file = (Path(__file__).parent / './halide.comb').resolve()

def coreir_to_comb(cmod: coreir.Module):
    global halide_obj
    if halide_obj is None:
        with open(halide_file, 'r') as f:
            halide_obj = comb.compiler.compile_program(f.read())
    assert isinstance(halide_obj, comb.ir.Obj)
    inputs, outputs = get_coreir_io(cmod.type)
    stmts = []
    selpath_to_sym = {}
    for i_name, i_type in inputs.items():
        in_decl = InDecl(sym=Sym(i_name), type=ht_to_comb_type(i_type))
        stmts.append(in_decl)
        selpath_to_sym[('self', i_name)] = Sym(i_name)
    for o_name, o_type in outputs.items():
        out_decl = OutDecl(sym=Sym(o_name), type=ht_to_comb_type(o_type))
        stmts.append(out_decl)
        selpath_to_sym[('self', o_name)] = Sym(o_name)

    cdef: coreir.ModuleDef = cmod.definition
    cinst_to_comb = {}
    cinst_to_io = {'self': (outputs, inputs)}

    for cinst in cdef.instances:
        cinst: coreir.Instance = cinst
        inst_name = cinst.name
        inst_cmod: coreir.Module = cinst.module
        cinst_to_comb[inst_name] = get_comb(inst_cmod)
        cinst_to_io[inst_name] = get_coreir_io(inst_cmod.type)

    ordered_insts = OrderedDict()
    #Tasks: Get a depth-first ordered list of instances.
    def get_iports(iname):
        inst: coreir.Instance = cdef.get_instance(iname)
        if iname=="self":
            return inst, outputs.keys()
        inst_inputs = cinst_to_io[inst.name][0]
        return inst, inst_inputs.keys()

    q = deque()
    q.append("self")
    while len(q) != 0:
        iname = q.popleft()
        if iname in ordered_insts:
            continue
        inst, iports = get_iports(iname)
        inst_info = {}
        for iport in iports:
            port = inst.select(iport)
            conns = port.connected_wireables
            assert len(conns) == 1
            sp = conns[0].selectpath
            if len(sp) != 2:
                raise ValueError(f"Connection: {sp} cannot have more than one select")
            other_iname, oport = sp
            inst_info[iport] = (other_iname, oport)
            q.append(other_iname)
        ordered_insts[iname] = inst_info
    symidx = 0
    for iname, inst_info in reversed(ordered_insts.items()):
        if iname=='self':
            # Create a custom simple assign
            for oport in outputs.keys():
                assert oport in inst_info
                selpath = inst_info[oport]
                assert selpath in selpath_to_sym
                lhs = selpath_to_sym[('self', oport)]
                rhs = selpath_to_sym[selpath]
                stmt = AssignStmt([lhs], [rhs])
                stmts.append(stmt)
            continue
        inst_inputs, inst_outputs = cinst_to_io[iname]
        lhss = []
        for oport in inst_outputs.keys():
            k = (iname, oport)
            if k in selpath_to_sym:
                raise ValueError(f"oport: {k}")
            sym = Sym(f"t{symidx}")
            symidx +=1
            selpath_to_sym[k] = sym
            lhss.append(sym)
        iargs = []
        for iport in inst_inputs.keys():
            assert iport in inst_info
            driver = inst_info[iport]
            assert driver in selpath_to_sym
            iargs.append(selpath_to_sym[driver])
        call = CallExpr(cinst_to_comb[iname], [], iargs)
        stmt = AssignStmt(lhss, [call])
        stmts.append(stmt)
    comb_name = QSym(cmod.namespace.name, cmod.name)
    cp = CombProgram(comb_name, stmts)
    return cp

def coreir_to_obj(file):
