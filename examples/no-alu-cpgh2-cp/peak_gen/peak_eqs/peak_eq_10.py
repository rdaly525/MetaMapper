
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_10_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_10(Peak):
        def __call__(self, in2 : Data, in1 : Data, in3 : Data, in0 : Data, in5 : Data) -> Data:
            sub0 = SData(in1 - in3); 
            return Data(Bit(in0 < Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0)))).ite(in2,in5))
      
    return mapping_function_10
