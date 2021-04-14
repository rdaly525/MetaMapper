
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_17_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_17(Peak):
        def __call__(self, data5043 : Data, data5048 : Data) -> Bit:
            
            return Bit(UInt(data5048) == UInt(data5043))
    
    return mapping_function_17
    