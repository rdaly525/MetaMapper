
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_0_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_0(Peak):
        def __call__(self, data17 : Data, data19 : Data, data18 : Data) -> Data:
            
            return Data(UInt(data19) + UInt(Data(UInt(data17) + UInt(data18))))
    
    return mapping_function_0
    