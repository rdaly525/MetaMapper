
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_12_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_12(Peak):
        def __call__(self, in0 : Data, in3 : Data, in1 : Data) -> Bit:
            sub0 = SData(in1 - in3); 
            return Bit(in0 < Data((sub0 >= SData(0)).ite(sub0, (SData(-1)*sub0))))
      
    return mapping_function_12
