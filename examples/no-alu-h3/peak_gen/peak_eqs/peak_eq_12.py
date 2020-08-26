
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_12_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_12(Peak):
        def __call__(self, in3 : Data, in1 : Data, bit_in3 : Bit) -> Data:
            
            return Data(bit_in3.ite(in1,in3))
      
    return mapping_function_12
