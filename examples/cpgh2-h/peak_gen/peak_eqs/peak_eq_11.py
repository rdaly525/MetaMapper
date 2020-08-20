
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_11_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_11(Peak):
        def __call__(self, in5 : Data, in2 : Data, in3 : Data, in1 : Data, in0 : Data) -> Data:
            sub0 = SData(in3 - in2); 
            return Data(Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < in5).ite(in1,in0))
      
    return mapping_function_11
