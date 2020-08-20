
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_15_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_15(Peak):
        def __call__(self, in1 : Data, in0 : Data, in5 : Data, in4 : Data) -> Data:
            
            return Data(Bit(in4 < in5).ite(in1,in0))
      
    return mapping_function_15
