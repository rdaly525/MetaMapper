
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_6_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_6(Peak):
        def __call__(self, in3 : Data, in2 : Data, bit_in0 : Bit) -> Bit:
            
            return Bit(bit_in0 & Bit(SData(in3) < SData(in2)))
      
    return mapping_function_6
