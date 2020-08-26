
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_11_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_11(Peak):
        def __call__(self, in5 : Data, in6 : Data) -> Bit:
            
            return Bit(in5 < in6)
      
    return mapping_function_11
