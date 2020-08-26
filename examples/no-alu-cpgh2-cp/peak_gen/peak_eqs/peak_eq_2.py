
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_2_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_2(Peak):
        def __call__(self, in0 : Data, in3 : Data, in1 : Data, in5 : Data, bit_in0 : Bit) -> Bit:
            
            return Bit(Bit(bit_in0 & Bit(SData(in0) < SData(in5))) & Bit(SData(in1) < SData(in3)))
      
    return mapping_function_2
