
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_28_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_28(Peak):
        def __call__(self, data1065 : Data, data1070 : Data) -> Data:
            
            return Data(UInt(data1065) >> UInt(data1070))
    
    return mapping_function_28
    