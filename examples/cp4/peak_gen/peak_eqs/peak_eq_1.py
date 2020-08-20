
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
        def __call__(self, in4 : Data, in3 : Data, in2 : Data, in0 : Data, in1 : Data) -> Data:
            sub0 = SData(in0 - in1); 
            return Data(Bit(in2 < Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0)))).ite(in3,in4))
      
    return mapping_function_1
