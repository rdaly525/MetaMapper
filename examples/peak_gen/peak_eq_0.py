
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
        def __call__(self, data52 : Data, data53 : Data) -> Data:
            sub0 = SInt(data52 - data53); 
            return Data((sub0 >= SInt(0)).ite(sub0, (SInt(-1)*sub0)))
    
    return mapping_function_0
    