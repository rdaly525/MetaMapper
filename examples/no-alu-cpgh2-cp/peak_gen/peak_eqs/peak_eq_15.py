
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
        def __call__(self, in0 : Data, in2 : Data, in1 : Data, in5 : Data) -> Data:
            
            return Data(Bit(in0 < in1).ite(in2,in5))
      
    return mapping_function_15
