
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_19_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_19(Peak):
        def __call__(self, in5 : Data, in1 : Data) -> Data:
            
            return Data((SData(in1) <= SData(in5)).ite(SData(in1), SData(in5)))
      
    return mapping_function_19
