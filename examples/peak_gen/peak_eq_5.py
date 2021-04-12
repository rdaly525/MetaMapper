
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_5_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_5(Peak):
        def __call__(self, data63 : Bit, data61 : Bit) -> Bit:
            
            return Bit(Bit(data61) & Bit(data63))
    
    return mapping_function_5
    