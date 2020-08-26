
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_18_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_18(Peak):
        def __call__(self, in5 : Data, in6 : Data) -> Data:
            
            return Data(SData(in5) >> SData(in6))
      
    return mapping_function_18
