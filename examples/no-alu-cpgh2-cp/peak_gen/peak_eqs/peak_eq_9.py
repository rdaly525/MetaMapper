
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_9_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_9(Peak):
        def __call__(self, in1 : Data, in4 : Data, in3 : Data, in0 : Data) -> Bit:
            sub0 = SData(in4 - in0); sub1 = SData(in1 - in3); 
            return Bit(Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))) < Data((sub1 >= SData(0)).ite(sub1, (SData(-1)*sub1))))
      
    return mapping_function_9
