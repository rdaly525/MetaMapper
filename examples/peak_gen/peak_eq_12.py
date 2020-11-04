
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_12_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_12(Peak):
        def __call__(self, bit_in1 : Bit, bit_in0 : Bit) -> Bit:
            
            return Bit(bit_in0 & bit_in1)
      
    return mapping_function_12
