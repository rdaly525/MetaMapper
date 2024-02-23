from peak.ir import IR
from hwtypes import BitVector, Bit
from hwtypes.adt import Product
from peak import Peak, name_outputs, family_closure, Const
from peak.black_box import BlackBox
from peak.family import AbstractFamily, MagmaFamily, SMTFamily
from peak.float import float_lib_gen, RoundingMode
from hwtypes import RoundingMode as RoundingMode_hw
from ...node import Nodes, Constant, DagNode, Select
from hwtypes import SMTFPVector, FPVector
import magma

def gen_custom_ops_peak_CoreIR(width):

    
    float_lib = float_lib_gen(8, 7)

    CoreIR = IR()
    DATAWIDTH = 16
    def BFloat16_fc(family):
        if isinstance(family, MagmaFamily):
            BFloat16 =  magma.BFloat[8, 7, RoundingMode.RNE, False]
            BFloat16.reinterpret_from_bv = lambda bv: BFloat16(bv)
            BFloat16.reinterpret_as_bv = lambda f: magma.Bits[16](f)
            return BFloat16
        elif isinstance(family, SMTFamily):
            FPV = SMTFPVector
        else:
            FPV = FPVector
        BFloat16 = FPV[8, 7, RoundingMode_hw.RNE, False]
        return BFloat16

    @family_closure
    def fp_add_fc(family: AbstractFamily):

        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)
        Data = family.BitVector[16]

        @family.assemble(locals(), globals())
        class fp_add(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                return Data(self.Add(in0, in1))
        
        return fp_add
    
    CoreIR.add_instruction("float_DW.fp_add", fp_add_fc)

    @family_closure
    def fp_sub_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.Unsigned[32]
        SInt = family.Signed[16]
        UInt = family.Unsigned[16]
        Bit = family.Bit
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        @family.assemble(locals(), globals())
        class fp_sub(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                
                in1 = in1 ^ (2 ** (16 - 1))
                return Data(self.Add(in0, in1))
        
        return fp_sub
    
    CoreIR.add_instruction("float.sub", fp_sub_fc)


    @family_closure
    def fp_mul_fc(family: AbstractFamily):

        FPMul = float_lib.const_rm(RoundingMode.RNE).Mul_fc(family)
        Data = family.BitVector[16]

        @family.assemble(locals(), globals())
        class fp_mul(Peak):
            def __init__(self):
                self.Mul: FPMul = FPMul()

            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                return Data(self.Mul(in0, in1))
        
        return fp_mul
    
    CoreIR.add_instruction("float_DW.fp_mul", fp_mul_fc)


    @family_closure
    def fp_getffrac_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_getffrac(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                signa = BitVector[16]((in0 & 0x8000))
                manta = BitVector[16]((in0 & 0x7F)) | 0x80
                expa0 = BitVector[8](in0[7:15])
                biased_exp0 = SInt[9](expa0.zext(1))
                unbiased_exp0 = SInt[9](biased_exp0 - SInt[9](127))

                if (unbiased_exp0 < 0):
                    manta_shift1 = BitVector[16](
                        manta) >> BitVector[16](-unbiased_exp0)
                else:
                    manta_shift1 = BitVector[16](
                        manta) << BitVector[16](unbiased_exp0)
                unsigned_res = BitVector[16]((manta_shift1 & 0x07F))
                if (signa == 0x8000):
                    signed_res = -SInt[16](unsigned_res)
                else:
                    signed_res = SInt[16](unsigned_res)

                # We are not checking for overflow when converting to int
                res = signed_res
                return Data(res)
        return fp_getffrac
    CoreIR.add_instruction("fp_getffrac", fp_getffrac_fc)


    @family_closure
    def fp_getfint_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_getfint(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                signa = BitVector[16]((in0 & 0x8000))
                manta = BitVector[16]((in0 & 0x7F)) | 0x80
                expa0 = UInt(in0)[7:15]
                biased_exp0 = SInt[9](expa0.zext(1))
                unbiased_exp0 = SInt[9](biased_exp0 - SInt[9](127))
                if (unbiased_exp0 < 0):
                    manta_shift0 = BitVector[23](0)
                else:
                    manta_shift0 = BitVector[23](
                        manta) << BitVector[23](unbiased_exp0)
                unsigned_res0 = BitVector[23](manta_shift0 >> BitVector[23](7))
                unsigned_res = BitVector[16](unsigned_res0[0:16])
                if (signa == 0x8000):
                    signed_res = -SInt[16](unsigned_res)
                else:
                    signed_res = SInt[16](unsigned_res)
                # We are not checking for overflow when converting to int
                res = signed_res
                return Data(res)
        return fp_getfint
    
    CoreIR.add_instruction("fp_getfint", fp_getfint_fc)

    @family_closure
    def fp_cnvint2f_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_cnvint2f(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                
                sign = BitVector[16](0)
                if (sign[15] == Bit(1)):
                    abs_input = BitVector[16](-SInt[16](in0))
                else:
                    abs_input = BitVector[16](in0)
                scale = SInt[16](-127)
                # for bit_pos in range(8):
                #   if (abs_exp[bit_pos]==Bit(1)):
                #     scale = bit_pos
                if (abs_input[0] == Bit(1)):
                    scale = SInt[16](0)
                if (abs_input[1] == Bit(1)):
                    scale = SInt[16](1)
                if (abs_input[2] == Bit(1)):
                    scale = SInt[16](2)
                if (abs_input[3] == Bit(1)):
                    scale = SInt[16](3)
                if (abs_input[4] == Bit(1)):
                    scale = SInt[16](4)
                if (abs_input[5] == Bit(1)):
                    scale = SInt[16](5)
                if (abs_input[6] == Bit(1)):
                    scale = SInt[16](6)
                if (abs_input[7] == Bit(1)):
                    scale = SInt[16](7)
                if (abs_input[8] == Bit(1)):
                    scale = SInt[16](8)
                if (abs_input[9] == Bit(1)):
                    scale = SInt[16](9)
                if (abs_input[10] == Bit(1)):
                    scale = SInt[16](10)
                if (abs_input[11] == Bit(1)):
                    scale = SInt[16](11)
                if (abs_input[12] == Bit(1)):
                    scale = SInt[16](12)
                if (abs_input[13] == Bit(1)):
                    scale = SInt[16](13)
                if (abs_input[14] == Bit(1)):
                    scale = SInt[16](14)
                if (abs_input[15] == Bit(1)):
                    scale = SInt[16](15)
                normmant_mul_left = SInt[16](abs_input)
                normmant_mul_right = (SInt[16](15)-scale)
                normmant_mask = SInt[16](0x7f00)

                #if (alu == ALU_t.FCnvInt2F) | (alu == ALU_t.FCnvExp2F):
                if (scale >= 0):
                    normmant = BitVector[16](
                        (normmant_mul_left << normmant_mul_right) & normmant_mask)
                else:
                    normmant = BitVector[16](0)

                
                normmant = BitVector[16](normmant) >> 8

                biased_scale = scale + 127
                to_float_DW_result = (sign | ((BitVector[16](biased_scale) << 7) & (
                        0xFF << 7)) | normmant)

                return Data(to_float_DW_result)
        return fp_cnvint2f
    CoreIR.add_instruction("fp_cnvint2f", fp_cnvint2f_fc)

    @family_closure
    def fp_cnvexp2f_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_cnvexp2f(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                expa0 = BitVector[8](in0[7:15])
                biased_exp0 = SInt[9](expa0.zext(1))
                unbiased_exp0 = SInt[9](biased_exp0 - SInt[9](127))
                if (unbiased_exp0 < 0):
                    sign = BitVector[16](0x8000)
                    abs_exp0 = -unbiased_exp0
                else:
                    sign = BitVector[16](0x0000)
                    abs_exp0 = unbiased_exp0
                abs_exp = BitVector[8](abs_exp0[0:8])
                scale = SInt[16](-127)
                # for bit_pos in range(8):
                #   if (abs_exp[bit_pos]==Bit(1)):
                #     scale = bit_pos
                if (abs_exp[0] == Bit(1)):
                    scale = SInt[16](0)
                if (abs_exp[1] == Bit(1)):
                    scale = SInt[16](1)
                if (abs_exp[2] == Bit(1)):
                    scale = SInt[16](2)
                if (abs_exp[3] == Bit(1)):
                    scale = SInt[16](3)
                if (abs_exp[4] == Bit(1)):
                    scale = SInt[16](4)
                if (abs_exp[5] == Bit(1)):
                    scale = SInt[16](5)
                if (abs_exp[6] == Bit(1)):
                    scale = SInt[16](6)
                if (abs_exp[7] == Bit(1)):
                    scale = SInt[16](7)
                normmant_mul_left = SInt[16](abs_exp)
                normmant_mul_right = (SInt[16](7)-scale)
                normmant_mask = SInt[16](0x7F)

                if (scale >= 0):
                    normmant = BitVector[16](
                        (normmant_mul_left << normmant_mul_right) & normmant_mask)
                else:
                    normmant = BitVector[16](0)

                biased_scale = scale + 127
                to_float_DW_result = (sign | ((BitVector[16](biased_scale) << 7) & (
                        0xFF << 7)) | normmant)
                return Data(to_float_DW_result)
        return fp_cnvexp2f

    CoreIR.add_instruction("fp_cnvexp2f", fp_cnvexp2f_fc)

    @family_closure
    def fp_subexp_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_subexp(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data, in1: Data) -> Data:
                signa = BitVector[16]((in0 & 0x8000))
                expa = UInt(in0)[7:15]
                signb = BitVector[16]((in1 & 0x8000))
                expb = UInt(in1)[7:15]
                expa = expa - expb + 127
                exp_shift = BitVector[16](expa)
                exp_shift = exp_shift << 7
                manta = BitVector[16]((in0 & 0x7F))
                res = (signa | signb) | exp_shift | manta
                return res
        return fp_subexp

    CoreIR.add_instruction("fp_subexp", fp_subexp_fc)


    @family_closure
    def fp_addiexp_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_addiexp(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                
                sign = BitVector[16]((in0 & 0x8000))
                exp = UInt(in0)[7:15]
                exp_check = exp.zext(1)
                exp = exp + UInt(in1)[0:8]
                exp_check = exp_check + UInt(in1)[0:9]
                # Augassign not supported by magma yet
                # exp += SInt[8](in1[0:8])
                # exp_check += SInt[9](in1[0:9])
                exp_shift = BitVector[16](exp)
                exp_shift = exp_shift << 7
                mant = BitVector[16]((in0 & 0x7F))
                res = (sign | exp_shift | mant)
                return Data(res)
        
        return fp_addiexp
    
    CoreIR.add_instruction("fp_addiexp", fp_addiexp_fc)


    @family_closure
    def fp_getmant_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_getmant(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                return Data(in0 & 0x7F)
        return fp_getmant

    CoreIR.add_instruction("fp_getmant", fp_getmant_fc)


    @family_closure
    def fp_mux_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_mux(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data, sel:Bit) -> Data:
                return sel.ite(in0, in1)
        return fp_mux

    CoreIR.add_instruction("float.mux", fp_mux_fc)


    @family_closure
    def fp_ge_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_ge(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Bit)
            def __call__(self, in0 : Data, in1 : Data) -> Bit:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1 = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1))

                Z = fp_is_zero(res)
                if (a_inf & b_inf) & (a_neg == b_neg):
                    Z = family.Bit(1)

                N = res[-1]

                return Bit(~N | Z)
        
        return fp_ge

    CoreIR.add_instruction("float.ge", fp_ge_fc)

    @family_closure
    def fp_gt_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_gt(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Bit)
            def __call__(self, in0 : Data, in1 : Data) -> Bit:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1 = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1))

                Z = fp_is_zero(res)
                if (a_inf & b_inf) & (a_neg == b_neg):
                    Z = family.Bit(1)

                N = res[-1]

                return Bit(~N & ~Z)
        
        return fp_gt

    CoreIR.add_instruction("float.gt", fp_gt_fc)

    @family_closure
    def fp_le_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_le(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Bit)
            def __call__(self, in0 : Data, in1 : Data) -> Bit:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1 = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1))

                Z = fp_is_zero(res)
                if (a_inf & b_inf) & (a_neg == b_neg):
                    Z = family.Bit(1)

                N = res[-1]

                return Bit(N | Z)
        
        return fp_le

    CoreIR.add_instruction("float.le", fp_le_fc)


    @family_closure
    def fp_lt_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_lt(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Bit)
            def __call__(self, in0 : Data, in1 : Data) -> Bit:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1 = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1))

                Z = fp_is_zero(res)
                if (a_inf & b_inf) & (a_neg == b_neg):
                    Z = family.Bit(1)

                N = res[-1]

                return Bit(N & ~Z)
        
        return fp_lt

    CoreIR.add_instruction("float.lt", fp_lt_fc)

    @family_closure
    def fp_eq_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_eq(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Bit)
            def __call__(self, in0 : Data, in1 : Data) -> Bit:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1 = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1))

                Z = fp_is_zero(res)
                if (a_inf & b_inf) & (a_neg == b_neg):
                    Z = family.Bit(1)

                return Z
        
        return fp_eq

    CoreIR.add_instruction("float.eq", fp_eq_fc)

    @family_closure
    def fp_exp_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_exp(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data) -> Data:

                # We replace this
                a_fpadd = in0
               
                return Data(a_fpadd)
        
        return fp_exp

    CoreIR.add_instruction("float.exp", fp_exp_fc)

    @family_closure
    def fp_div_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_div(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                a_fpadd = bv2float(in0)
                b_fpadd = bv2float(in1)
                gt = Bit(a_fpadd < b_fpadd)
                return Data(gt.ite(in0, in1))
        
        return fp_div
    
    CoreIR.add_instruction("float.div", fp_div_fc)

    @family_closure
    def fp_max_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_max(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1_neg = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1_neg))
                N = res[-1]

                if N:
                    ret = in1
                else:
                    ret = in0

                return ret

        return fp_max

    CoreIR.add_instruction("float.max", fp_max_fc)

    @family_closure
    def fp_min_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
       
        def fp_get_exp(val: Data):
            return val[7:15]

        def fp_get_frac(val: Data):
            return val[:7]

        def fp_is_zero(val: Data):
            return (fp_get_exp(val) == 0) & (fp_get_frac(val) == 0)

        def fp_is_inf(val: Data):
            return (fp_get_exp(val) == -1) & (fp_get_frac(val) == 0)

        def fp_is_neg(val: Data):
            return family.Bit(val[-1])
        FPAdd = float_lib.const_rm(RoundingMode.RNE).Add_fc(family)

        def bv2float(bv):
            return BFloat.reinterpret_from_bv(bv)

        @family.assemble(locals(), globals())
        class fp_min(Peak):
            def __init__(self):
                self.Add: FPAdd = FPAdd()

            @name_outputs(out=Data)
            def __call__(self, in0 : Data, in1 : Data) -> Data:
                a_inf = fp_is_inf(in0)
                b_inf = fp_is_inf(in1)
                a_neg = fp_is_neg(in0)
                b_neg = fp_is_neg(in1)

                in1_neg = in1 ^ (2 ** (16 - 1))
                res = Data(self.Add(in0, in1_neg))
                N = res[-1]

                if N:
                    ret = in0
                else:
                    ret = in1

                return ret
        
        return fp_min

    CoreIR.add_instruction("float.min", fp_min_fc)


    @family_closure
    def fp_cmp_fc(family: AbstractFamily):
        BitVector = family.BitVector
        BFloat = BFloat16_fc(family)
        Data = family.BitVector[16]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[16]
        UInt = family.Unsigned
        UData = UInt[16]
        UData32 = UInt[32]

        float_lib = float_lib.const_rm(RoundingMode.RNE)

        is_inf = float_lib.Is_infinite_fc(family)
        is_neg = float_lib.Is_negative_fc(family)
        is_zero = float_lib.Is_zero_fc(family)

        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        @family.assemble(locals(), globals())
        class fp_cmp(Peak):
            def __init__(self):
                self.is_inf: is_inf = is_inf()
                self.is_neg: is_neg = is_neg()
                self.is_zero: is_zero = is_zero()

            @name_outputs(out=Bit)
            def __call__(self, in0 : Data, in1 : Data) -> Bit:
                
                a_fpadd = BFloat(in0)
                b_fpadd = BFloat(in1)
                a_inf = self.is_inf(in0)
                b_inf = self.is_inf(in1)
                a_neg = self.is_neg(in0)
                b_neg = self.is_neg(in1)

                res = Data((a_fpadd - b_fpadd))
                Z = self.is_zero(res)
                if (a_inf & b_inf) & (a_neg == b_neg):
                    Z = Bit(1)

                return Z
    
        return fp_cmp
    
    CoreIR.add_instruction("float_DW.cmp", fp_cmp_fc)

    @family_closure
    def mult_middle_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.BitVector[32]
        class mult_middle(Peak):
            @name_outputs(out=Data)
            def __call__(self, in1: Data, in0: Data) -> Data:
                mul = Data32(in0.sext(16)) * Data32(in1.sext(16))
                return Data(mul[8:24])
        return mult_middle

    CoreIR.add_instruction("commonlib.mult_middle", mult_middle_fc)


    @family_closure
    def sext_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.BitVector[32]
        class sext(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data) -> Data32:
                res = Data32(in0)
                return res
        return sext

    CoreIR.add_instruction("coreir.sext", sext_fc)

    @family_closure
    def slice_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.BitVector[32]
        class slice(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data32) -> Data:
                res = Data(in0[8:24])
                return res
        return slice

    CoreIR.add_instruction("coreir.slice", slice_fc)

    @family_closure
    def mul32_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.BitVector[32]
        class mul32(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data32, in1: Data32) -> Data32:
                res = Data32(in0) * Data32(in1)
                return Data32(res)
        return mul32

    CoreIR.add_instruction("coreir.mul32", mul32_fc)


    @family_closure
    def ashr32_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.Signed[32]
        class ashr32(Peak):
            @name_outputs(out=Data)
            def __call__(self, in0: Data32, in1: Data32) -> Data32:
                res = Data32(in0) >> Data32(in1)
                return Data32(res)
        return ashr32

    CoreIR.add_instruction("coreir.ashr32", ashr32_fc)

    return CoreIR
