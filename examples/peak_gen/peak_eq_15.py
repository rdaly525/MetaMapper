
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_15_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_15(Peak):
        def __call__(self, data5042 : Data, data5047 : Data) -> Data:
            
            return Data(UInt(data5042) & UInt(data5047))
    
    return mapping_function_15
    