
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_4_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_4(Peak):
        def __call__(self, in3 : Data, in1 : Data, in0 : Data, in2 : Data) -> Data:
            
            return Data(in3 + Data(Data(in0 + in1) + in2))
      
    return mapping_function_4
