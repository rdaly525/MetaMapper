import coreir
import typing as tp
from collections import OrderedDict
import hwtypes as ht
from comb.ast import QSym, InDecl, OutDecl, Type, Sym, BoolType, BVType, IntType, TypeCall, IntValue
from comb.ir import CombProgram, CallExpr
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

def get_comb_call(cmod: coreir.Module) -> CallExpr:
    comb: Comb
    pargs : tp.Tuple[Expr]
    args : tp.Tuple[Expr]
    return CallExpr()

def coreir_to_comb(cmod: coreir.Module):
    inputs, outputs = get_coreir_io(cmod.type)
    stmts = []
    for i_name, i_type in inputs.items():
        in_decl = InDecl(sym=Sym(i_name), type=ht_to_comb_type(i_type))
        stmts.append(in_decl)
    for o_name, o_type in outputs.items():
        out_decl = OutDecl(sym=Sym(o_name), type=ht_to_comb_type(o_type))
        stmts.append(out_decl)

    cdef: coreir.ModuleDef = cmod.definition
    for cinst in cdef.instances:
        cinst: coreir.Instance = cinst
        inst_name = cinst.name
        inst_cmod: coreir.Module = cinst.module
        inst_call = get_comb_call(inst_cmod)



    #How do I get a simple list of sorted statments?
    #I need a map between instance and output variable name
    cdef = cmod.definition
    cdef.interface
    # Task
    comb_name = QSym(cmod.namespace.name, cmod.name)
    cp = CombProgram(comb_name, stmts)
    return cp