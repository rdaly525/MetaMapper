
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_6_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    Data32 = family.Unsigned[32]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_6(Peak):
        def __call__(self, data9 : Data, data28 : Data) -> Data:
            
            return Data(UInt(data9) * UInt(data28))
    
    return mapping_function_6
    