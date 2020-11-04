
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_1_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_1(Peak):
        def __call__(self, const0 : Const(Data), in0 : Data) -> Data:
            
            return Data(in0 * const0)
      
    return mapping_function_1
