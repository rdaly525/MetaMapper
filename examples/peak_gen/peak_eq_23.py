
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_23_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_23(Peak):
        def __call__(self, data197 : Bit, data199 : Bit) -> Bit:
            
            return Bit(Bit(data197) & Bit(data199))
    
    return mapping_function_23
    