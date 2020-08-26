
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
        def __call__(self, in1 : Data, in3 : Data, in4 : Data, in5 : Data, in0 : Data, in2 : Data) -> Data:
            sub0 = SData(in1 - in2); sub1 = SData(in3 - in4); 
            return Data(Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < Data((sub1 >= SData(0)).ite(sub1, (SData(-1)*sub1)))).ite(in0,in5))
      
    return mapping_function_1
