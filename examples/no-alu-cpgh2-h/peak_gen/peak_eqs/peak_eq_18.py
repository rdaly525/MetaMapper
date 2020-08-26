
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_18_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_18(Peak):
        def __call__(self, in0 : Data, in4 : Data) -> Data:
            sub0 = SData(in4 - in0); 
            return Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0)))
      
    return mapping_function_18
