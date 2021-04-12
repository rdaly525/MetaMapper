
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
        def __call__(self, data1062 : Data, data1063 : Data, data1151 : Bit) -> Data:
            
            return Data(data1151.ite(UInt(data1063),UInt(data1062)))
    
    return mapping_function_17
    