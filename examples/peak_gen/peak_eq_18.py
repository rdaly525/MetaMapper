
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_18_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_18(Peak):
        def __call__(self, data5043 : Data, data5045 : Data) -> Data:
            
            return Data(SInt(data5045) >> SInt(data5043))
    
    return mapping_function_18
    