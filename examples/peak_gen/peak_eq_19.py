
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_19_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_19(Peak):
        def __call__(self, data91 : Data, data92 : Data, data197 : Bit) -> Data:
            
            return Data(data197.ite(UInt(data92),UInt(data91)))
    
    return mapping_function_19
    