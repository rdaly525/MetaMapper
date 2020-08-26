
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_7_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_7(Peak):
        def __call__(self, in4 : Data, in1 : Data, in0 : Data, in2 : Data, in6 : Data, in5 : Data) -> Data:
            sub0 = SData(in5 - in6); sub1 = SData(in1 - in0); 
            return Data(Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < Data((sub1 >= SData(0)).ite(sub1, (SData(-1)*sub1)))).ite(in4,in2))
      
    return mapping_function_7
