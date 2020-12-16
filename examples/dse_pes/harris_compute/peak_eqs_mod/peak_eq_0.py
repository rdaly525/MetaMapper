
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_0_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_0(Peak):
        def __call__(self, in2 : Data, in1 : Data, in0 : Data) -> Data:
            
            return Data(in2 + Data(in0 + in1))
      
    return mapping_function_0
