
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_25_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_25(Peak):
        def __call__(self, in0 : Data, in5 : Data) -> Data:
            
            return Data(in0 >> in5)
      
    return mapping_function_25
