from peak.ir import IR
from hwtypes import BitVector, Bit
from hwtypes.adt import Product
from peak import Peak, name_outputs, family_closure, Const

def gen_peak_CoreIR(width):
    CoreIR = IR()

    @family_closure
    def const_fc(family):
        Data = family.BitVector[width]
        class ConstModParams(Product):
            value=Data
        class const(Peak):
            @name_outputs(out=Data)
            def __call__(self, value: Const(Data)):
                return value

            #def __call__(self, modparams : ConstModParams):
            #    return modparams.value
        return const

    CoreIR.add_instruction("const", const_fc)

    class UnaryInput(Product):
        in0=BitVector[width]

    class BinaryInput(Product):
        in0=BitVector[width]
        in1=BitVector[width]

    class TernaryInput(Product):
        in0=BitVector[width]
        in1=BitVector[width]
        sel=Bit

    class OutputBV(Product):
        out=BitVector[width]

    class OutputBit(Product):
        out=Bit

    for name, fun in (
        ("add",  lambda f, x, y: x+y),
        ("sub",  lambda f, x, y: x-y),
        ("and_", lambda f, x, y: x&y),
        ("or_",  lambda f, x, y: x|y),
        ("xor",  lambda f, x, y: x^y),
        ("shl",  lambda f, x, y: x<<y),
        ("lshr", lambda f, x, y: x.bvlshr(y)),
        ("ashr", lambda f, x, y: x.bvashr(y)),
        ("mul",  lambda f, x, y: x*y),
        #("udiv", lambda x, y: x.bvudiv(y)),
        #("urem", lambda x, y: x.bvurem(y)),
        #("sdiv", lambda x, y: x.bvsdiv(y)),
        #("srem", lambda x, y: x.bvsrem(y)),
        #("smod", lambda x, y: x.bvsmod(y)),
    ):
        CoreIR.add_peak_instruction(name, BinaryInput, OutputBV, fun)

    for name, fun in (
        ("wire", lambda f, x: x),
        ("not_", lambda f, x: ~x),
        ("neg", lambda f, x: -x)
    ):
        CoreIR.add_peak_instruction(name, UnaryInput, OutputBV, fun)

    def reduce(fun):
        def _reduce(val):
            ret = val[0]
            for i in range(1, len(val)):
                ret = fun(ret, val[i])
            return ret
        return _reduce

    for name, fun in (
        ("andr", lambda x: reduce(lambda a, b : a&b)(x)),
        ("orr", lambda x: reduce(lambda a, b : a|b)(x)),
        ("xorr", lambda x: reduce(lambda a, b : a^b)(x)),
    ):
        CoreIR.add_peak_instruction(name, UnaryInput, OutputBit, fun)

    for name, fun in (
        ("eq" , lambda x, y: x==y),
        ("neq", lambda x, y: x!=y),
        ("slt", lambda x, y: x.bvslt(y)),
        ("sle", lambda x, y: x.bvsle(y)),
        ("sgt", lambda x, y: x.bvsgt(y)),
        ("sge", lambda x, y: x.bvsge(y)),
        ("ult", lambda x, y: x.bvult(y)),
        ("ule", lambda x, y: x.bvule(y)),
        ("ugt", lambda x, y: x.bvugt(y)),
        ("uge", lambda x, y: x.bvuge(y)),
    ):
        CoreIR.add_peak_instruction(name, BinaryInput, OutputBit, fun)

    #add mux
    CoreIR.add_peak_instruction("mux", TernaryInput, OutputBV, lambda in0, in1, sel: sel.ite(in1, in0))

    return CoreIR

#TODO missing:
# slice, concat, sext, zext
