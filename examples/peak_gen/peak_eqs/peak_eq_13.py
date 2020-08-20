
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_13_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_13(Peak):
        def __call__(self, in5 : Data, in2 : Data, in0 : Data) -> Bit:
            sub0 = SData(in2 - in0); 
            return Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < in5)
      
    return mapping_function_13
