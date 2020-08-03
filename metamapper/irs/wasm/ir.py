from peak.ir import IR
from peak import Peak, name_outputs
from hwtypes import BitVector, Bit
from hwtypes.adt import Product
import math

def gen_WASM(include64=False):
    WASM = IR()

    class Output32(Product):
        out=BitVector[32]

    class Input32(Product):
        in0=BitVector[32]

    class Output64(Product):
        out=BitVector[64]

    class Input64(Product):
        in0=BitVector[64]

    def gen_integer(width):
        prefix = f"i{width}"
        logwidth = int(math.log2(width))
        Data = BitVector[width]
        Data32 = BitVector[32]

        #TODO is this a problem declaring a constant outside the scope?
        def shift_amount(x : Data):
            #Need to zero out all but the bottom bits
            mask = Data(width)-Data(1)
            return x & mask

        assert width in (32,64)

        class UnaryInput(Product):
            in0=Data

        class Output(Product):
            out=Data

        class BinaryInput(Product):
            in0=Data
            in1=Data

        #Integer Arithmetic Instructions
        for name, fun in (
            ("add", lambda f, x, y: x+y),
            ("sub", lambda f, x, y: x-y),
            ("mul", lambda f, x, y: x*y),
            ("div_s", lambda f, x, y: x.bvsdiv(y)),
            ("div_u", lambda f, x, y: x.bvudiv(y)),
            ("rem_s", lambda f, x, y: x.bvsrem(y)),
            ("rem_u", lambda f, x, y: x.bvurem(y)),
            ("and_", lambda f, x, y: x & y),
            ("or_", lambda f, x, y: x | y),
            ("xor", lambda f, x, y: x ^ y),
            ("shl", lambda f, x, y: x << shift_amount(y)),
            ("shr_s", lambda f, x, y: x.bvashr(shift_amount(y))),
            ("shr_l", lambda f, x, y: x.bvlshr(shift_amount(y))),
        ):
            WASM.add_peak_instruction(f"{prefix}.{name}",BinaryInput,Output,fun, cls_name=name)

        ##Need to test these
        #def rotl(in0 : Data, in1 : Data):
        #    in1 = shift_amount(in1)
        #    msbs = (in0 << in1)
        #    lsbs = in0.bvlshr(Data(32)-in1)
        #    return msbs | lsbs
        #WASM.add_peak_instruction(f"{prefix}.rotl",BinaryInput,Output,rotl)

        #def rotr(in0 : Data, in1 : Data):
        #    in1 = shift_amount(in1)
        #    msbs = (in0 << (Data32-in1))
        #    lsbs = in0.bvlshr(in1)
        #    return msbs | lsbs
        #WASM.add_peak_instruction(f"{prefix}.rotr",BinaryInput,Output,rotr)

        #def clz(in0 : Data):
        #    #TODO
        #    return Data(0)
        #WASM.add_peak_instruction(f"{prefix}.clz",UnaryInput,Output,clz)

        #def ctz(in0 : Data):
        #    #TODO
        #    return Data(0)
        #WASM.add_peak_instruction(f"{prefix}.ctz",UnaryInput,Output,ctz)

        #def popcnt(in0 : Data):
        #    #TODO
        #    return Data(0)
        #WASM.add_peak_instruction(f"{prefix}.popcnt",UnaryInput,Output,popcnt)

        #WASM.add_peak_instruction(f"{prefix}.eqz",UnaryInput,Output32,lambda x : x==Data(0))

        #def to32(bit : Bit):
        #    assert isinstance(bit,Bit)
        #    return bit.ite(Data32(1),Data32(0))

        ##Integer Comparison Instructions
        #WASM.add_peak_instruction(f"{prefix}.eq",BinaryInput,Output32,lambda x : to32(x==y))
        #WASM.add_peak_instruction(f"{prefix}.ne",BinaryInput,Output32,lambda x : to32(x!=y))
        #WASM.add_peak_instruction(f"{prefix}.lt_s",BinaryInput,Output32,lambda x : to32(x.bvslt(y)))
        #WASM.add_peak_instruction(f"{prefix}.lt_u",BinaryInput,Output32,lambda x : to32(x.bvslt(y)))
        #WASM.add_peak_instruction(f"{prefix}.le_s",BinaryInput,Output32,lambda x : to32(x.bvsle(y)))
        #WASM.add_peak_instruction(f"{prefix}.le_u",BinaryInput,Output32,lambda x : to32(x.bvule(y)))
        #WASM.add_peak_instruction(f"{prefix}.gt_s",BinaryInput,Output32,lambda x : to32(x.bvsgt(y)))
        #WASM.add_peak_instruction(f"{prefix}.gt_u",BinaryInput,Output32,lambda x : to32(x.bvugt(y)))
        #WASM.add_peak_instruction(f"{prefix}.ge_s",BinaryInput,Output32,lambda x : to32(x.bvsge(y)))
        #WASM.add_peak_instruction(f"{prefix}.ge_u",BinaryInput,Output32,lambda x : to32(x.bvuge(y)))


    gen_integer(32)
    if include64:
        gen_integer(64)

        #Conversion ops
        #WASM.add_peak_instruction("i32_wrap", Input64,Output32, lambda x : x[:32])
        #WASM.add_peak_instruction("i64_extend.s", Input32,Output64, lambda x: x.sext(32))
        #WASM.add_peak_instruction("i64_extend.u", Input32,Output64, lambda x: x.zext(32))
    return WASM
