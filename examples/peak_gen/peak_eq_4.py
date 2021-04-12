
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_4_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_4(Peak):
        def __call__(self, data17 : Data, data18 : Data, data61 : Bit) -> Data:
            
            return Data(data61.ite(UInt(data18),UInt(data17)))
    
    return mapping_function_4
    