
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_27_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_27(Peak):
        def __call__(self, in2 : Data, in4 : Data, bit_in1 : Bit) -> Data:
            
            return Data(bit_in1.ite(in4,in2))
      
    return mapping_function_27
