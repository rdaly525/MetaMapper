
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_9_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_9(Peak):
        def __call__(self, in0 : Data, in1 : Data, bit_in0 : Bit) -> Data:
            
            return Data(bit_in0.ite(in0,in1))
      
    return mapping_function_9
