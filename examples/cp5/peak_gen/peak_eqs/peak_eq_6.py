
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_6_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_6(Peak):
        def __call__(self, in6 : Data, in7 : Data, in3 : Data) -> Bit:
            sub0 = SData(in7 - in3); 
            return Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < in6)
      
    return mapping_function_6
