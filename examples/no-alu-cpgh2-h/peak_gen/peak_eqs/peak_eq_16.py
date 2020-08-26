
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_16_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_16(Peak):
        def __call__(self, in4 : Data, in5 : Data, in2 : Data) -> Data:
            
            return Data(Data(in4 + in2) >> in5)
      
    return mapping_function_16
