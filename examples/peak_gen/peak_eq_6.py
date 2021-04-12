
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_6_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_6(Peak):
        def __call__(self, data17 : Data, data18 : Data) -> Bit:
            
            return Bit(SInt(data17) <= SInt(data18))
    
    return mapping_function_6
    