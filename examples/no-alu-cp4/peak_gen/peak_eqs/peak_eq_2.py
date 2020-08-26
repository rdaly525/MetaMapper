
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
        def __call__(self, in2 : Data, in1 : Data, in4 : Data, in3 : Data, in0 : Data) -> Data:
            sub0 = SData(in2 - in1); 
            return Data(Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < in3).ite(in0,in4))
      
    return mapping_function_2
