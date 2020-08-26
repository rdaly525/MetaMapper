
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_1_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_1(Peak):
        def __call__(self, in5 : Data, in3 : Data, in4 : Data, in2 : Data, in1 : Data) -> Data:
            sub0 = SData(in4 - in5); 
            return Data(Bit(in1 < Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0)))).ite(in3,in2))
      
    return mapping_function_1
