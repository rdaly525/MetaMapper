
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_2_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_2(Peak):
        def __call__(self, in0 : Data, in1 : Data) -> Data:
            
            return Data((in1 >= in0).ite(in1, in0))
      
    return mapping_function_2
