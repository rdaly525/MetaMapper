
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_22_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_22(Peak):
        def __call__(self, data1062 : Data, data1063 : Data) -> Data:
            
            return Data(UInt(data1062) & UInt(data1063))
    
    return mapping_function_22
    