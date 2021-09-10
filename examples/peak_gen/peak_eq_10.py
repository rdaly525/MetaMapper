
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_10_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_10(Peak):
        def __call__(self, data52 : Data, data53 : Data, data106 : Bit) -> Data:
            
            return Data(data106.ite(UInt(data52),UInt(data53)))
    
    return mapping_function_10
    