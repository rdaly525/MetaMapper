
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_7_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_7(Peak):
        def __call__(self, data52 : Data, data53 : Data) -> Bit:
            
            return Bit(UInt(data53) < UInt(data52))
    
    return mapping_function_7
    